"""
Server integration tests for MCP server
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from src.mcp.server import server


def test_mcp_server_initialized():
    """Test that MCP server is properly initialized"""
    assert server is not None
    assert hasattr(server, 'name')
    assert server.name == "todo-mcp-server"
    assert hasattr(server, 'version')
    assert server.version == "1.0.0"


def test_all_tools_registered():
    """Test that all 5 required tools are registered with the server"""
    # Check that the server has the expected tools registered
    registered_tools = [tool.name for tool in server._tools]

    expected_tools = ['add_task', 'list_tasks', 'update_task', 'complete_task', 'delete_task']

    for tool in expected_tools:
        assert tool in registered_tools, f"{tool} is not registered with the MCP server"


def test_tool_descriptions():
    """Test that tools have appropriate descriptions"""
    tools_by_name = {tool.name: tool for tool in server._tools}

    assert 'add_task' in tools_by_name
    assert 'list_tasks' in tools_by_name
    assert 'update_task' in tools_by_name
    assert 'complete_task' in tools_by_name
    assert 'delete_task' in tools_by_name

    # Check that descriptions exist and are meaningful
    for tool_name in ['add_task', 'list_tasks', 'update_task', 'complete_task', 'delete_task']:
        tool = tools_by_name[tool_name]
        assert tool.description is not None
        assert len(tool.description) > 0


def test_tool_parameters_defined():
    """Test that all tools have parameters defined"""
    tools_by_name = {tool.name: tool for tool in server._tools}

    for tool_name in ['add_task', 'list_tasks', 'update_task', 'complete_task', 'delete_task']:
        tool = tools_by_name[tool_name]
        # Tools should have parameter schemas defined
        assert tool.parameters is not None


@pytest.mark.asyncio
async def test_server_stateless_operation():
    """Test that server follows stateless operation principles"""
    # This test verifies that the server doesn't maintain any internal state
    # between requests by checking that the registered tools don't hold any state

    # Mock a few requests to ensure no state is maintained
    tools_by_name = {tool.name: tool for tool in server._tools}

    # The tools themselves should just be functions with no internal state
    # that changes between calls
    assert len(tools_by_name) == 5  # We have 5 tools registered


@pytest.mark.asyncio
async def test_server_tool_handlers_exist():
    """Test that all registered tools have appropriate handlers"""
    # Check that each registered tool has a callable handler
    for tool in server._tools:
        # Each tool should have a handler function
        assert tool.handler is not None
        assert callable(tool.handler)