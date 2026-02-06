"""Pytest fixtures for task tests."""
import pytest
import asyncio
import time
from httpx import AsyncClient, ASGITransport
from jose import jwt
from sqlalchemy import text

from src.main import app
from src.db import async_session_factory, engine
from src.config import get_settings

settings = get_settings()


def create_test_token(user_id: str, expires_in: int = 3600) -> str:
    """
    Create a test JWT token for a user.

    Args:
        user_id: The user ID to encode in the token
        expires_in: Token expiration time in seconds

    Returns:
        Encoded JWT token string
    """
    payload = {
        "sub": user_id,
        "exp": time.time() + expires_in
    }
    return jwt.encode(payload, settings.better_auth_secret, algorithm="HS256")


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def auth_headers() -> dict:
    """Return authorization headers with a valid test token."""
    token = create_test_token("test-user-123")
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def other_user_auth_headers() -> dict:
    """Return authorization headers for a different user."""
    token = create_test_token("other-user-456")
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def expired_auth_headers() -> dict:
    """Return authorization headers with an expired token."""
    token = create_test_token("test-user-123", expires_in=-3600)
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
async def client():
    """Create an async HTTP client for testing."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.fixture
async def clean_db():
    """Clean up the database before and after each test."""
    async with async_session_factory() as session:
        await session.execute(text("DELETE FROM task"))
        await session.commit()
    yield
    async with async_session_factory() as session:
        await session.execute(text("DELETE FROM task"))
        await session.commit()
