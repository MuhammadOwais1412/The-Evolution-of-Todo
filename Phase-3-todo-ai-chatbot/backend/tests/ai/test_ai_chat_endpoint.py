"""Integration tests for AI chat endpoint."""
import pytest
from httpx import AsyncClient
from unittest.mock import patch, AsyncMock

from src.main import app


@pytest.fixture
async def async_client():
    """Create an async HTTP client for testing."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture
def mock_auth_token():
    """Mock authentication token."""
    return "Bearer test-token-123"


@pytest.fixture
def mock_user():
    """Mock authenticated user."""
    return {
        "user_id": "test-user-123",
        "email": "test@example.com"
    }


class TestAIChatEndpoint:
    """Integration tests for AI chat endpoint."""

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_chat_endpoint_requires_auth(self, async_client):
        """Test that chat endpoint requires authentication."""
        response = await async_client.post(
            "/api/ai/chat",
            json={"message": "test message"}
        )
        assert response.status_code == 403  # Unauthorized

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_chat_endpoint_with_valid_request(self, async_client, mock_auth_token, mock_user):
        """Test chat endpoint with valid authenticated request."""
        with patch('src.api.routes.ai_chat.get_current_user_from_token', return_value=mock_user), \
             patch('src.api.routes.ai_chat.get_ai_agent_service') as mock_service:

            # Mock the agent service response
            mock_agent = AsyncMock()
            mock_agent.process_command.return_value = {
                "response": "Task added successfully",
                "tool_calls": [],
                "requires_confirmation": False
            }
            mock_service.return_value = mock_agent

            response = await async_client.post(
                "/api/ai/chat",
                json={"message": "Add a task to buy groceries"},
                headers={"Authorization": mock_auth_token}
            )

            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert "response" in data

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_chat_endpoint_with_empty_message(self, async_client, mock_auth_token, mock_user):
        """Test chat endpoint rejects empty messages."""
        with patch('src.api.routes.ai_chat.get_current_user_from_token', return_value=mock_user):
            response = await async_client.post(
                "/api/ai/chat",
                json={"message": ""},
                headers={"Authorization": mock_auth_token}
            )

            assert response.status_code == 422  # Validation error

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_health_endpoint(self, async_client):
        """Test AI health check endpoint."""
        with patch('src.api.routes.ai_chat.get_ai_agent_service') as mock_service:
            mock_agent = AsyncMock()
            mock_agent.client = True  # Mock client exists
            mock_service.return_value = mock_agent

            response = await async_client.get("/api/ai/health")

            assert response.status_code == 200
            data = response.json()
            assert "status" in data
            assert "checks" in data


class TestConfirmationEndpoints:
    """Integration tests for confirmation endpoints."""

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_get_pending_confirmations(self, async_client, mock_auth_token, mock_user):
        """Test retrieving pending confirmations."""
        with patch('src.api.routes.ai_chat.get_current_user_from_token', return_value=mock_user), \
             patch('src.api.routes.ai_chat.get_confirmation_handler') as mock_handler:

            mock_conf = AsyncMock()
            mock_conf.get_pending_confirmations.return_value = []
            mock_handler.return_value = mock_conf

            response = await async_client.get(
                "/api/ai/pending-confirmations",
                headers={"Authorization": mock_auth_token}
            )

            assert response.status_code == 200
            data = response.json()
            assert "pending_confirmations" in data


class TestAuditLogEndpoints:
    """Integration tests for audit log endpoints."""

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_get_tool_call_logs(self, async_client, mock_auth_token, mock_user):
        """Test retrieving tool call logs."""
        with patch('src.api.routes.ai_chat.get_current_user_from_token', return_value=mock_user), \
             patch('src.ai.audit_logger.AuditLogger') as mock_logger:

            mock_audit = AsyncMock()
            mock_audit.get_tool_call_history.return_value = []
            mock_logger.return_value = mock_audit

            response = await async_client.get(
                "/api/ai/tool-call-log",
                headers={"Authorization": mock_auth_token}
            )

            assert response.status_code == 200
            data = response.json()
            assert "logs" in data
            assert "pagination" in data
