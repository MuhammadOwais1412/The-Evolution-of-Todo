"""Configuration for AI provider settings."""
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from openai import AsyncOpenAI
try:
    from agents import OpenAIChatCompletionsModel, set_tracing_disabled
except ImportError:
    # Fallback import if agents module is not available
    from openai import OpenAIChatCompletionsModel, set_tracing_disabled


# Load environment variables from .env file
load_dotenv()


class AIProviderSettings(BaseSettings):
    """AI provider settings loaded from environment variables."""

    # Google Gemini API configuration for OpenAI-compatible endpoint
    gemini_api_key: str = Field(..., alias="GEMINI_API_KEY")
    gemini_base_url: str = Field(default="https://generativelanguage.googleapis.com/v1beta/openai/", alias="GEMINI_BASE_URL")
    gemini_model_name: str = Field(default="gemini-2.5-flash", alias="GEMINI_MODEL_NAME")

    # AI Agent configuration
    ai_agent_name: str = Field(default="Todo Assistant", alias="AI_AGENT_NAME")
    ai_agent_instructions: str = Field(
        default="You are a helpful todo management assistant. Help users manage their tasks using the available tools. "
                "Always confirm destructive actions like deletions before proceeding.",
        alias="AI_AGENT_INSTRUCTIONS"
    )

    # Timeout and retry settings
    request_timeout: int = Field(default=30, alias="REQUEST_TIMEOUT")
    max_retries: int = Field(default=3, alias="MAX_RETRIES")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore"


def get_ai_settings() -> AIProviderSettings:
    """Get AI provider settings."""
    return AIProviderSettings()


# Initialize the OpenAI client for Gemini
def initialize_gemini_client() -> AsyncOpenAI:
    """Initialize and return the AsyncOpenAI client configured for Gemini."""
    settings = get_ai_settings()

    # Disable tracing if needed
    set_tracing_disabled(disabled=True)

    client = AsyncOpenAI(
        api_key=settings.gemini_api_key,
        base_url=settings.gemini_base_url
    )

    return client


def initialize_gemini_model():
    """Initialize and return the OpenAIChatCompletionsModel for Gemini."""
    client = initialize_gemini_client()
    settings = get_ai_settings()

    model = OpenAIChatCompletionsModel(
        openai_client=client,
        model=settings.gemini_model_name
    )

    return model