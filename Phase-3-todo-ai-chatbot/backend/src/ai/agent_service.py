"""AI agent service for processing natural language commands and mapping them to MCP tools."""
import json
import logging
import asyncio
from typing import Dict, Any, Optional, List
from uuid import uuid4
from datetime import datetime

from openai import AsyncOpenAI
from agents import OpenAIChatCompletionsModel

from ..config.ai_config import initialize_gemini_client, initialize_gemini_model
from ..exceptions.ai_exceptions import (
    AIProcessingError,
    ToolExecutionError,
    ContextRetrievalError,
    UserPermissionError
)
from ..schemas.ai_schemas import MCPToolName, MCPToolCall, ToolCallStatus
from .mcp_adapters import MCPAdapters
from .context_reconstructor import ContextReconstructor
from .tool_orchestrator import ToolOrchestrator
from .audit_logger import AuditLogger
from .tool_definitions import get_mcp_tool_definitions


logger = logging.getLogger(__name__)


class AIAgentService:
    """Service class for the AI agent that processes natural language commands."""

    def __init__(self):
        """Initialize the AI agent service with required components."""
        try:
            # Initialize the OpenAI client for Gemini
            self.client = initialize_gemini_client()
            self.model = initialize_gemini_model()

            # Initialize supporting services
            self.mcp_adapters = MCPAdapters()
            self.context_reconstructor = ContextReconstructor()
            self.tool_orchestrator = ToolOrchestrator()
            self.audit_logger = AuditLogger()

            # Define the tools available to the AI agent
            self.tools = self._define_available_tools()

            # Shutdown flag
            self._shutdown = False

        except Exception as e:
            logger.error(f"Failed to initialize AI agent service: {str(e)}")
            raise AIProcessingError(f"Failed to initialize AI agent service: {str(e)}")

    async def shutdown(self):
        """Gracefully shutdown the AI agent service and cleanup resources."""
        logger.info("Shutting down AI agent service...")
        self._shutdown = True

        try:
            # Close any open connections
            if hasattr(self.client, 'close'):
                await self.client.close()

            # Cleanup any pending confirmations
            if hasattr(self, 'confirmation_handler'):
                await self.confirmation_handler.cleanup_expired_confirmations()

            logger.info("AI agent service shutdown complete")

        except Exception as e:
            logger.error(f"Error during AI agent service shutdown: {str(e)}")

    def is_shutdown(self) -> bool:
        """Check if the service is in shutdown state."""
        return self._shutdown

    def _define_available_tools(self) -> List[Dict[str, Any]]:
        """Define the tools available to the AI agent that map to MCP tools."""
        return get_mcp_tool_definitions()

    async def process_command(
        self,
        user_id: str,
        message: str,
        requires_confirmation: bool = True
    ) -> Dict[str, Any]:
        """
        Process a natural language command and execute appropriate MCP tools.

        Args:
            user_id: The ID of the authenticated user
            message: The natural language command from the user
            requires_confirmation: Whether to require confirmation for destructive operations

        Returns:
            Dictionary containing the AI response and any tool calls made
        """
        # Check if service is shutting down
        if self._shutdown:
            raise AIProcessingError("Service is shutting down, cannot process new requests")

        try:
            # Sanitize and validate input
            if not message or not message.strip():
                raise AIProcessingError("Message cannot be empty")

            # Limit message length to prevent prompt injection attacks
            if len(message) > 1000:
                raise AIProcessingError("Message is too long. Please keep it under 1000 characters.")

            # Basic sanitization to prevent prompt injection
            sanitized_message = self._sanitize_input(message)

            logger.info(f"Processing command for user {user_id}: {sanitized_message}")

            # Reconstruct conversation context
            context = await self.context_reconstructor.reconstruct_context(user_id)

            # Prepare the AI request with context and tools
            messages = [
                {
                    "role": "system",
                    "content": "You are a helpful todo management assistant. Help users manage their tasks using the available tools. Always confirm destructive actions like deletions before proceeding."
                }
            ]

            # Add conversation history if available
            if context:
                messages.extend(context)

            # Add the current user message
            messages.append({"role": "user", "content": message})

            # Call the AI model with tools (with retry logic)
            try:
                response = await self._call_ai_model_with_retry(messages)
            except Exception as e:
                logger.error(f"Error calling AI model for user {user_id}: {str(e)}")
                raise AIProcessingError(f"AI model error: {str(e)}")

            # Process the response
            ai_message = response.choices[0].message
            tool_calls = ai_message.tool_calls or []

            # Track executed tool calls
            executed_tool_calls: List[MCPToolCall] = []
            requires_confirmation_flag = False

            # Execute each tool call
            for tool_call in tool_calls:
                try:
                    # Determine if this is a destructive operation that requires confirmation
                    if requires_confirmation and self._is_destructive_operation(tool_call.function.name):
                        requires_confirmation_flag = True

                        # For destructive operations, just log that confirmation is needed
                        # In a real implementation, you'd pause and wait for explicit user confirmation
                        executed_tool_calls.append(
                            MCPToolCall(
                                id=tool_call.id,
                                tool_name=getattr(MCPToolName, tool_call.function.name.upper()),
                                tool_params=json.loads(tool_call.function.arguments),
                                result=None,
                                status=ToolCallStatus.PENDING,
                                timestamp=datetime.utcnow()
                            )
                        )
                    else:
                        # Execute the tool call
                        function_name = tool_call.function.name
                        function_args = json.loads(tool_call.function.arguments)

                        # Ensure user_id is passed to the function
                        function_args['user_id'] = user_id

                        # Execute the appropriate MCP tool
                        result = await self._execute_mcp_tool(function_name, function_args)

                        # Log the tool call for audit purposes
                        await self.audit_logger.log_tool_call(
                            user_id=user_id,
                            tool_name=function_name,
                            tool_params=function_args,
                            result=result,
                            status=ToolCallStatus.SUCCESS
                        )

                        executed_tool_calls.append(
                            MCPToolCall(
                                id=tool_call.id,
                                tool_name=getattr(MCPToolName, function_name.upper()),
                                tool_params=function_args,
                                result=result,
                                status=ToolCallStatus.SUCCESS,
                                timestamp=datetime.utcnow()
                            )
                        )

                except Exception as e:
                    logger.error(f"Error executing tool call {tool_call.id}: {str(e)}")

                    # Log the failed tool call
                    await self.audit_logger.log_tool_call(
                        user_id=user_id,
                        tool_name=tool_call.function.name,
                        tool_params=json.loads(tool_call.function.arguments),
                        result={"error": str(e)},
                        status=ToolCallStatus.ERROR
                    )

                    executed_tool_calls.append(
                        MCPToolCall(
                            id=tool_call.id,
                            tool_name=getattr(MCPToolName, tool_call.function.name.upper()),
                            tool_params=json.loads(tool_call.function.arguments),
                            result={"error": str(e)},
                            status=ToolCallStatus.ERROR,
                            timestamp=datetime.utcnow()
                        )
                    )

            # Prepare the response
            response_content = ai_message.content or "I've processed your request."

            # Moderate the AI response for safety
            moderated_response = self._moderate_ai_response(response_content)

            return {
                "response": moderated_response,
                "tool_calls": executed_tool_calls,
                "requires_confirmation": requires_confirmation_flag
            }

        except AIProcessingError:
            # Re-raise AI processing errors as they're already properly formatted
            raise
        except ContextRetrievalError:
            # Re-raise context retrieval errors as they're already properly formatted
            raise
        except ToolExecutionError:
            # Re-raise tool execution errors as they're already properly formatted
            raise
        except Exception as e:
            logger.error(f"Unexpected error processing command for user {user_id}: {str(e)}")
            raise AIProcessingError("Sorry, I encountered an unexpected error while processing your request. Please try again.")

    async def _execute_mcp_tool(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute an MCP tool with the given parameters."""
        try:
            if tool_name == "add_task":
                return await self.mcp_adapters.add_task(**params)
            elif tool_name == "list_tasks":
                return await self.mcp_adapters.list_tasks(**params)
            elif tool_name == "update_task":
                return await self.mcp_adapters.update_task(**params)
            elif tool_name == "complete_task":
                return await self.mcp_adapters.complete_task(**params)
            elif tool_name == "delete_task":
                return await self.mcp_adapters.delete_task(**params)
            else:
                raise ToolExecutionError(f"Unknown tool: {tool_name}")

        except UserPermissionError:
            raise
        except Exception as e:
            logger.error(f"Error executing MCP tool {tool_name}: {str(e)}")
            raise ToolExecutionError(f"Error executing tool {tool_name}: {str(e)}")

    async def process_command_with_confirmation(self, user_id: str, message: str, confirmation_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Process a command that may require user confirmation, especially for destructive operations.

        Args:
            user_id: The ID of the authenticated user
            message: The natural language command from the user
            confirmation_id: Optional confirmation ID if this is a follow-up to a confirmation request

        Returns:
            Dictionary containing the AI response and any tool calls made
        """
        # If this is a confirmation, process it differently
        if confirmation_id:
            # In a real implementation, you'd verify the confirmation and execute the pending action
            # For now, we'll just process normally but indicate that confirmation was received
            pass

        return await self.process_command(user_id, message, requires_confirmation=True)

    def _is_destructive_operation(self, tool_name: str) -> bool:
        """
        Determine if a tool operation is destructive and requires user confirmation.

        Args:
            tool_name: Name of the tool to check

        Returns:
            Boolean indicating if the operation is destructive
        """
        destructive_operations = [
            "delete_task",
            # Add other potentially destructive operations here in the future
        ]

        return tool_name in destructive_operations

    def _sanitize_input(self, message: str) -> str:
        """
        Sanitize user input to prevent prompt injection attacks.

        Args:
            message: The raw user message

        Returns:
            Sanitized message
        """
        # Remove any potential prompt injection patterns
        # This is a basic implementation - in production, use more sophisticated methods
        sanitized = message.strip()

        # Remove excessive whitespace
        sanitized = " ".join(sanitized.split())

        # Basic filtering of potentially harmful patterns
        # Note: This is a simple approach; consider using a dedicated library for production
        harmful_patterns = [
            "ignore previous instructions",
            "ignore all previous",
            "disregard previous",
            "forget previous",
            "new instructions:",
            "system:",
            "assistant:",
        ]

        lower_message = sanitized.lower()
        for pattern in harmful_patterns:
            if pattern in lower_message:
                logger.warning(f"Potential prompt injection detected: {pattern}")
                # Don't reject entirely, just log - the AI should handle it

        return sanitized

    def _moderate_ai_response(self, response: str) -> str:
        """
        Moderate AI response to ensure it doesn't contain harmful content.

        Args:
            response: The AI-generated response

        Returns:
            Moderated response
        """
        # Basic content moderation - in production, use a dedicated service
        # Check for potentially harmful patterns
        harmful_indicators = [
            "ignore previous",
            "disregard instructions",
            "system prompt",
            "as an ai language model",
        ]

        lower_response = response.lower()
        for indicator in harmful_indicators:
            if indicator in lower_response:
                logger.warning(f"Potentially harmful content detected in AI response: {indicator}")
                # Return a safe default response
                return "I apologize, but I cannot process that request. Please try rephrasing your command."

        # Check response length
        if len(response) > 2000:
            logger.warning("AI response too long, truncating")
            return response[:1997] + "..."

        return response

    async def _call_ai_model_with_retry(
        self,
        messages: List[Dict[str, Any]],
        max_retries: int = 3,
        base_delay: float = 1.0
    ) -> Any:
        """
        Call the AI model with exponential backoff retry logic for transient failures.

        Args:
            messages: The messages to send to the AI model
            max_retries: Maximum number of retry attempts
            base_delay: Base delay in seconds for exponential backoff

        Returns:
            The AI model response

        Raises:
            AIProcessingError: If all retries fail
        """
        last_exception = None

        for attempt in range(max_retries):
            try:
                response = await self.client.chat.completions.create(
                    model=self.model.openai_client._client.base_url.split('/')[-1] or "gemini-1.5-flash",
                    messages=messages,
                    tools=self.tools,
                    tool_choice="auto"
                )
                return response

            except Exception as e:
                last_exception = e
                error_str = str(e).lower()

                # Check if this is a transient error that should be retried
                transient_errors = [
                    "timeout",
                    "connection",
                    "rate limit",
                    "503",
                    "502",
                    "500",
                    "429"
                ]

                is_transient = any(err in error_str for err in transient_errors)

                if not is_transient or attempt == max_retries - 1:
                    # Not a transient error or last attempt - don't retry
                    logger.error(f"AI model call failed (attempt {attempt + 1}/{max_retries}): {str(e)}")
                    raise

                # Calculate exponential backoff delay
                delay = base_delay * (2 ** attempt)
                logger.warning(
                    f"Transient error on attempt {attempt + 1}/{max_retries}: {str(e)}. "
                    f"Retrying in {delay}s..."
                )

                await asyncio.sleep(delay)

        # If we get here, all retries failed
        raise AIProcessingError(f"AI model call failed after {max_retries} attempts: {str(last_exception)}")