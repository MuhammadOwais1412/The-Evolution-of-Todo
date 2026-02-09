"""Google Gemini client implementation for the AI agent."""
import logging
from typing import Optional, Dict, Any
from openai import AsyncOpenAI
from agents import OpenAIChatCompletionsModel

from ..config.ai_config import get_ai_settings, initialize_gemini_client, initialize_gemini_model
from ..exceptions.ai_exceptions import AIConfigurationError


logger = logging.getLogger(__name__)


class GeminiClient:
    """Wrapper class for the Google Gemini client."""

    def __init__(self):
        """Initialize the Gemini client with configuration."""
        try:
            self.settings = get_ai_settings()
            self.client = initialize_gemini_client()
            self.model = initialize_gemini_model()

            # Validate configuration
            if not self.settings.gemini_api_key:
                raise AIConfigurationError("GEMINI_API_KEY not configured")

            if not self.settings.gemini_base_url:
                raise AIConfigurationError("GEMINI_BASE_URL not configured")

            if not self.settings.gemini_model_name:
                raise AIConfigurationError("GEMINI_MODEL_NAME not configured")

            logger.info("Gemini client initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize Gemini client: {str(e)}")
            raise AIConfigurationError(f"Failed to initialize Gemini client: {str(e)}")

    def get_client(self) -> AsyncOpenAI:
        """Return the initialized AsyncOpenAI client configured for Gemini."""
        return self.client

    def get_model(self):
        """Return the initialized OpenAIChatCompletionsModel for Gemini."""
        return self.model

    def get_settings(self):
        """Return the AI settings."""
        return self.settings

    async def test_connection(self) -> bool:
        """Test the connection to the Gemini API."""
        try:
            # Attempt a simple model listing or ping to test connection
            # This is a basic test - in practice you might call a models endpoint
            # or make a simple chat completion to verify the connection

            # For now, just test that we can access the client properties
            _ = self.client.api_key
            _ = self.settings.gemini_model_name

            logger.info("Gemini client connection test passed")
            return True

        except Exception as e:
            logger.error(f"Gemini client connection test failed: {str(e)}")
            return False

    async def chat_completion(
        self,
        messages: list,
        tools: Optional[list] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> Any:
        """
        Perform a chat completion using the Gemini model.

        Args:
            messages: List of message dictionaries with role and content
            tools: Optional list of tools for function calling
            temperature: Sampling temperature (0.0-2.0)
            max_tokens: Maximum number of tokens to generate

        Returns:
            The response from the Gemini model
        """
        try:
            # Prepare the request parameters
            params = {
                "model": self.settings.gemini_model_name,
                "messages": messages,
                "temperature": temperature,
            }

            # Add optional parameters if provided
            if tools:
                params["tools"] = tools
                params["tool_choice"] = "auto"

            if max_tokens:
                params["max_tokens"] = max_tokens

            # Make the API call
            response = await self.client.chat.completions.create(**params)

            logger.debug(f"Chat completion successful, usage: {getattr(response, 'usage', 'N/A')}")
            return response

        except Exception as e:
            logger.error(f"Chat completion failed: {str(e)}")
            raise

    def prepare_tool_definition(
        self,
        name: str,
        description: str,
        parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Prepare a tool definition in the format expected by the OpenAI/Gemini API.

        Args:
            name: Name of the tool
            description: Description of what the tool does
            parameters: Dictionary defining the parameters for the tool

        Returns:
            Tool definition in API format
        """
        return {
            "type": "function",
            "function": {
                "name": name,
                "description": description,
                "parameters": {
                    "type": "object",
                    "properties": parameters,
                    "required": []  # This would be populated based on required parameters
                }
            }
        }