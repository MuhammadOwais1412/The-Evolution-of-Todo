"""Environment configuration for the backend."""
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    # Database connection
    database_url: str = Field(..., alias="DATABASE_URL")

    # JWT secret for Better Auth token verification
    better_auth_secret: str = Field(..., alias="BETTER_AUTH_SECRET")

    # Better Auth base URL for fetching JWKS (required in production)
    better_auth_base_url: str = Field(default="", alias="BETTER_AUTH_URL")

    # API server configuration
    api_host: str = "localhost"
    api_port: int = 8000

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore"


def get_settings() -> Settings:
    """Get application settings."""
    return Settings()
