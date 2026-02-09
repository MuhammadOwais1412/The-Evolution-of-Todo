"""AI agent service for processing natural language commands and mapping them to MCP tools."""
import json
import logging
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

        except Exception as e:
            logger.error(f"Failed to initialize AI agent service: {str(e)}")
            raise AIProcessingError(f"Failed to initialize AI agent service: {str(e)}")

    def _define_available_tools(self) -> List[Dict[str, Any]]:
        """Define the tools available to the AI agent that map to MCP tools."""
        return [
            {
                "type": "function",
                "function": {
                    "name": "add_task",
                    "description": "Add a new task to the user's todo list",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "The ID of the user"},
                            "title": {"type": "string", "description": "The title of the task"},
                            "description": {"type": "string", "description": "The description of the task"},
                            "priority": {
                                "type": "string",
                                "enum": ["low", "medium", "high"],
                                "description": "Priority of the task, defaults to medium"
                            }
                        },
                        "required": ["user_id", "title"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_tasks",
                    "description": "List tasks for the user, optionally filtered by status",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "The ID of the user"},
                            "status": {
                                "type": "string",
                                "enum": ["all", "pending", "completed"],
                                "description": "Status filter for tasks, defaults to all"
                            }
                        },
                        "required": ["user_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "update_task",
                    "description": "Update an existing task for the user",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "The ID of the user"},
                            "task_id": {"type": "integer", "description": "The ID of the task to update"},
                            "title": {"type": "string", "description": "The new title of the task (optional)"},
                            "description": {"type": "string", "description": "The new description of the task (optional)"},
                            "priority": {
                                "type": "string",
                                "enum": ["low", "medium", "high"],
                                "description": "New priority of the task (optional)"
                            }
                        },
                        "required": ["user_id", "task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "complete_task",
                    "description": "Mark a task as completed",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "The ID of the user"},
                            "task_id": {"type": "integer", "description": "The ID of the task to complete"}
                        },
                        "required": ["user_id", "task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_task",
                    "description": "Delete a task from the user's todo list",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "The ID of the user"},
                            "task_id": {"type": "integer", "description": "The ID of the task to delete"}
                        },
                        "required": ["user_id", "task_id"]
                    }
                }
            }
        ]

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
        try:
            logger.info(f"Processing command for user {user_id}: {message}")

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

            # Call the AI model with tools
            response = await self.client.chat.completions.create(
                model=self.model.openai_client._client.base_url.split('/')[-1] or "gemini-1.5-flash",
                messages=messages,
                tools=self.tools,
                tool_choice="auto"
            )

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
                    if requires_confirmation and tool_call.function.name in ["delete_task"]:
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

            return {
                "response": response_content,
                "tool_calls": executed_tool_calls,
                "requires_confirmation": requires_confirmation_flag
            }

        except Exception as e:
            logger.error(f"Error processing command for user {user_id}: {str(e)}")
            raise AIProcessingError(f"Error processing command: {str(e)}")

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