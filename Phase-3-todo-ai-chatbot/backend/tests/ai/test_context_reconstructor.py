"""Unit tests for context reconstruction service."""
import pytest
from unittest.mock import Mock, AsyncMock, patch
from datetime import datetime

from src.ai.context_reconstructor import ContextReconstructor
from src.exceptions.ai_exceptions import ContextRetrievalError


@pytest.fixture
def context_reconstructor():
    """Create a context reconstructor instance for testing."""
    return ContextReconstructor()


class TestContextReconstructor:
    """Test suite for context reconstruction service."""

    def test_initialization(self, context_reconstructor):
        """Test that context reconstructor initializes correctly."""
        assert context_reconstructor is not None

    def test_format_task_info_empty(self, context_reconstructor):
        """Test formatting empty task list."""
        result = context_reconstructor._format_task_info([])
        assert "No recent tasks" in result

    def test_format_tool_call_info_empty(self, context_reconstructor):
        """Test formatting empty tool call list."""
        result = context_reconstructor._format_tool_call_info([])
        assert "No recent tool calls" in result

    @pytest.mark.asyncio
    async def test_limit_context_size(self, context_reconstructor):
        """Test context size limiting."""
        # Create large context
        large_context = [
            {"role": "user", "content": "a" * 1000},
            {"role": "assistant", "content": "b" * 1000},
            {"role": "user", "content": "c" * 1000},
            {"role": "assistant", "content": "d" * 1000},
        ]

        # Limit to small size
        limited = await context_reconstructor.limit_context_size(large_context, max_tokens=500)

        # Should have fewer messages
        assert len(limited) < len(large_context)

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_reconstruct_context_with_db(self):
        """Test context reconstruction with real database (integration test)."""
        pytest.skip("Integration test - requires real database")
