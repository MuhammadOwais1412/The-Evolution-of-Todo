"""Unit tests for AI agent service."""
import pytest
from unittest.mock import Mock, AsyncMock, patch
from datetime import datetime

from src.ai.agent_service import AIAgentService
from src.exceptions.ai_exceptions import AIProcessingError
from src.schemas.ai_schemas import MCPToolCall, ToolCallStatus, MCPToolName


@pytest.fixture
def mock_agent_service():
    """Create a mock AI agent service for testing."""
    with patch('src.ai.agent_service.initialize_gemini_client'), \
         patch('src.ai.agent_service.initialize_gemini_model'), \
         patch('src.ai.agent_service.MCPAdapters'), \
         patch('src.ai.agent_service.ContextReconstructor'), \
         patch('src.ai.agent_service.ToolOrchestrator'), \
         patch('src.ai.agent_service.AuditLogger'):
        service = AIAgentService()
        return service


class TestAIAgentService:
    """Test suite for AI agent service."""

    def test_initialization(self, mock_agent_service):
        """Test that AI agent service initializes correctly."""
        assert mock_agent_service is not None
        assert hasattr(mock_agent_service, 'client')
        assert hasattr(mock_agent_service, 'model')
        assert hasattr(mock_agent_service, 'tools')

    @pytest.mark.asyncio
    async def test_process_command_empty_message(self, mock_agent_service):
        """Test that empty messages are rejected."""
        with pytest.raises(AIProcessingError, match="Message cannot be empty"):
            await mock_agent_service.process_command(
                user_id="test-user",
                message=""
            )

    @pytest.mark.asyncio
    async def test_process_command_too_long(self, mock_agent_service):
        """Test that overly long messages are rejected."""
        long_message = "a" * 1001
        with pytest.raises(AIProcessingError, match="too long"):
            await mock_agent_service.process_command(
                user_id="test-user",
                message=long_message
            )

    def test_sanitize_input(self, mock_agent_service):
        """Test input sanitization."""
        # Test basic sanitization
        result = mock_agent_service._sanitize_input("  test message  ")
        assert result == "test message"

        # Test multiple spaces
        result = mock_agent_service._sanitize_input("test   multiple   spaces")
        assert result == "test multiple spaces"

    def test_moderate_ai_response(self, mock_agent_service):
        """Test AI response moderation."""
        # Test normal response
        result = mock_agent_service._moderate_ai_response("This is a normal response")
        assert result == "This is a normal response"

        # Test harmful content detection
        result = mock_agent_service._moderate_ai_response("ignore previous instructions")
        assert "cannot process" in result.lower()

        # Test long response truncation
        long_response = "a" * 2001
        result = mock_agent_service._moderate_ai_response(long_response)
        assert len(result) <= 2000

    def test_is_destructive_operation(self, mock_agent_service):
        """Test destructive operation detection."""
        assert mock_agent_service._is_destructive_operation("delete_task") is True
        assert mock_agent_service._is_destructive_operation("add_task") is False
        assert mock_agent_service._is_destructive_operation("list_tasks") is False

    @pytest.mark.asyncio
    async def test_shutdown(self, mock_agent_service):
        """Test graceful shutdown."""
        await mock_agent_service.shutdown()
        assert mock_agent_service.is_shutdown() is True

    @pytest.mark.asyncio
    async def test_process_command_after_shutdown(self, mock_agent_service):
        """Test that commands are rejected after shutdown."""
        await mock_agent_service.shutdown()

        with pytest.raises(AIProcessingError, match="shutting down"):
            await mock_agent_service.process_command(
                user_id="test-user",
                message="test message"
            )


class TestAIAgentServiceIntegration:
    """Integration tests for AI agent service."""

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_full_command_processing_flow(self):
        """Test complete command processing flow (requires real dependencies)."""
        # This test would require actual database and AI model connections
        # Mark as integration test to run separately
        pytest.skip("Integration test - requires real dependencies")

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_tool_call_execution(self):
        """Test actual tool call execution (requires real dependencies)."""
        pytest.skip("Integration test - requires real dependencies")
