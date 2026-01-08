"""Environment configuration for the backend."""
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    # Database connection
    database_url: str = "postgresql+asyncpg://localhost/todo"

    # JWT secret for Better Auth token verification
    better_auth_secret: str = "change-me-in-production"

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
