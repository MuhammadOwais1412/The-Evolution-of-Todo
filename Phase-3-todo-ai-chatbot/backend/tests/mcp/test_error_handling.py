"""
Comprehensive error handling tests for all MCP tools
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from src.mcp.tools.task_operations import (
    add_task, list_tasks, update_task, complete_task, delete_task
)
from src.mcp.schemas.task_schemas import AddTaskRequest, ErrorResponse


@pytest.mark.asyncio
async def test_error_responses_structure():
    """Test that all error responses follow the defined structure"""
    # Test invalid user_id error
    result = await add_task(AddTaskRequest(user_id="", title="Test"))

    assert result.status == "error"
    assert hasattr(result, 'error_code')
    assert hasattr(result, 'message')
    assert isinstance(result.error_code, str)
    assert isinstance(result.message, str)


@pytest.mark.asyncio
async def test_authentication_failure_errors():
    """Test that authentication failures return appropriate error codes"""
    # Test with invalid user ID (empty string)
    result = await add_task(AddTaskRequest(user_id="", title="Test Title"))

    assert result.status == "error"
    assert result.error_code == "INVALID_USER_ID"

    # Test list_tasks with invalid user ID
    result = await list_tasks("")
    assert result["status"] == "error"
    assert result["error_code"] == "INVALID_USER_ID"


@pytest.mark.asyncio
async def test_validation_error_responses():
    """Test that validation errors return clear indication of which parameters were invalid"""
    # Test add_task with invalid title (empty)
    result = await add_task(AddTaskRequest(user_id="user123", title=""))

    assert result.status == "error"
    assert result.error_code == "INVALID_TITLE"
    assert "required" in result.message.lower()


@pytest.mark.asyncio
async def test_database_operation_errors():
    """Test that database operation failures return structured error responses"""
    from sqlalchemy.exc import SQLAlchemyError

    # Mock a database error for add_task
    mock_session = AsyncMock()
    mock_session.add = MagicMock()
    mock_session.commit.side_effect = SQLAlchemyError("Database error")

    with patch('src.mcp.tools.task_operations.async_session_factory') as mock_factory:
        mock_factory.return_value.__aenter__.return_value = mock_session

        result = await add_task(AddTaskRequest(user_id="user123", title="Test"))

        assert result.status == "error"
        assert result.error_code == "DATABASE_ERROR"
        assert "database" in result.message.lower()


@pytest.mark.asyncio
async def test_task_not_found_errors():
    """Test error responses for operations on non-existent tasks"""
    # Mock the database session to return no task for update_task
    async def mock_execute(query):
        mock_result = AsyncMock()
        mock_result.scalar_one_or_none.return_value = None
        return mock_result

    mock_session = AsyncMock()
    mock_session.execute = mock_execute

    with patch('src.mcp.tools.task_operations.verify_user_owns_task', return_value=True), \
         patch('src.mcp.tools.task_operations.async_session_factory') as mock_factory:
        mock_factory.return_value.__aenter__.return_value = mock_session

        result = await update_task("user123", 999, title="New Title")

        assert result["status"] == "error"
        assert result["error_code"] == "TASK_NOT_FOUND"


@pytest.mark.asyncio
async def test_unauthorized_access_errors():
    """Test error responses for unauthorized task access"""
    # Test update_task when user doesn't own the task
    with patch('src.mcp.tools.task_operations.verify_user_owns_task', return_value=False):
        result = await update_task("other_user", 1, title="New Title")

        assert result["status"] == "error"
        assert result["error_code"] == "TASK_NOT_FOUND_OR_UNAUTHORIZED"

    # Test delete_task when user doesn't own the task
    with patch('src.mcp.tools.task_operations.verify_user_owns_task', return_value=False):
        result = await delete_task("other_user", 1)

        assert result["status"] == "error"
        assert result["error_code"] == "TASK_NOT_FOUND_OR_UNAUTHORIZED"


@pytest.mark.asyncio
async def test_error_response_consistency():
    """Test that all error responses follow consistent structure"""
    # Test various error scenarios and ensure consistent response structure
    errors_to_test = []

    # Invalid user ID error
    result = await add_task(AddTaskRequest(user_id="", title="Test"))
    errors_to_test.append(result)

    # Invalid title error
    result = await add_task(AddTaskRequest(user_id="user123", title=""))
    errors_to_test.append(result)

    # Check that all error responses have consistent structure
    for error_response in errors_to_test:
        assert hasattr(error_response, 'status')
        assert error_response.status == "error"
        assert hasattr(error_response, 'error_code')
        assert hasattr(error_response, 'message')
        assert isinstance(error_response.error_code, str)
        assert isinstance(error_response.message, str)


def test_error_schema_structure():
    """Test that ErrorResponse schema has correct structure"""
    from src.mcp.schemas.task_schemas import ErrorResponse

    # Create an error response
    error_resp = ErrorResponse(
        error_code="TEST_ERROR",
        message="This is a test error message"
    )

    # Verify the structure
    assert error_resp.status == "error"  # Default value
    assert error_resp.error_code == "TEST_ERROR"
    assert error_resp.message == "This is a test error message"
    assert error_resp.details is None  # Default value