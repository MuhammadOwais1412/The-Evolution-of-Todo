"""Unit tests for tool orchestrator service."""
import pytest
from unittest.mock import Mock, AsyncMock, patch

from src.ai.tool_orchestrator import ToolOrchestrator
from src.exceptions.ai_exceptions import UserPermissionError, ToolExecutionError


@pytest.fixture
def tool_orchestrator():
    """Create a tool orchestrator instance for testing."""
    return ToolOrchestrator()


class TestToolOrchestrator:
    """Test suite for tool orchestration service."""

    def test_initialization(self, tool_orchestrator):
        """Test that tool orchestrator initializes correctly."""
        assert tool_orchestrator is not None

    @pytest.mark.asyncio
    async def test_validate_user_permission_valid(self, tool_orchestrator):
        """Test user permission validation with valid user."""
        # Should not raise exception
        await tool_orchestrator.validate_user_permission("test-user", "add_task")

    @pytest.mark.asyncio
    async def test_validate_user_permission_invalid(self, tool_orchestrator):
        """Test user permission validation with invalid user."""
        with pytest.raises(UserPermissionError):
            await tool_orchestrator.validate_user_permission("", "add_task")

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_execute_tool_with_real_mcp(self):
        """Test tool execution with real MCP tools (integration test)."""
        pytest.skip("Integration test - requires real MCP tools")
