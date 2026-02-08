"""
Unit tests for the delete_task function
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from src.mcp.tools.task_operations import delete_task
from src.models.task import Task


@pytest.mark.asyncio
async def test_delete_task_success():
    """Test successful task deletion"""
    user_id = "user123"
    task_id = 1

    # Create mock task object
    mock_task = MagicMock()
    mock_task.id = task_id
    mock_task.user_id = user_id
    mock_task.title = "Test Task"
    mock_task.description = "Test Description"
    mock_task.completed = False
    mock_task.created_at = "2023-01-01T00:00:00"
    mock_task.updated_at = "2023-01-02T00:00:00"
    mock_task.priority = "medium"

    # Mock the database session
    async def mock_execute(query):
        mock_result = AsyncMock()
        mock_result.scalar_one_or_none.return_value = mock_task
        return mock_result

    mock_session = AsyncMock()
    mock_session.execute = mock_execute
    mock_session.delete = MagicMock()
    mock_session.commit = AsyncMock()

    # Mock the verify_user_owns_task function to return True
    with patch('src.mcp.tools.task_operations.verify_user_owns_task', return_value=True), \
         patch('src.mcp.tools.task_operations.async_session_factory') as mock_factory:
        mock_factory.return_value.__aenter__.return_value = mock_session
        result = await delete_task(user_id, task_id)

    # Assert the response is successful
    assert result["status"] == "success"
    assert result["task_id"] == task_id
    assert "deleted successfully" in result["message"]


@pytest.mark.asyncio
async def test_delete_task_invalid_user_id():
    """Test deleting task with invalid user ID"""
    result = await delete_task("", 1)  # Invalid user ID

    # Assert the response is an error
    assert result["status"] == "error"
    assert result["error_code"] == "INVALID_USER_ID"


@pytest.mark.asyncio
async def test_delete_task_not_authorized():
    """Test deleting task when user doesn't own the task"""
    # Mock the verify_user_owns_task function to return False
    with patch('src.mcp.tools.task_operations.verify_user_owns_task', return_value=False):
        result = await delete_task("other_user", 1)

    # Assert the response is an error
    assert result["status"] == "error"
    assert result["error_code"] == "TASK_NOT_FOUND_OR_UNAUTHORIZED"


@pytest.mark.asyncio
async def test_delete_task_not_found():
    """Test deleting task that doesn't exist"""
    # Mock the database session to return None
    async def mock_execute(query):
        mock_result = AsyncMock()
        mock_result.scalar_one_or_none.return_value = None
        return mock_result

    mock_session = AsyncMock()
    mock_session.execute = mock_execute

    # Mock the verify_user_owns_task function to return True
    with patch('src.mcp.tools.task_operations.verify_user_owns_task', return_value=True), \
         patch('src.mcp.tools.task_operations.async_session_factory') as mock_factory:
        mock_factory.return_value.__aenter__.return_value = mock_session
        result = await delete_task("user123", 999)  # Non-existent task

    # Assert the response is an error
    assert result["status"] == "error"
    assert result["error_code"] == "TASK_NOT_FOUND"


@pytest.mark.asyncio
async def test_delete_task_database_error():
    """Test handling of database errors during task deletion"""
    from sqlalchemy.exc import SQLAlchemyError

    # Mock the verify_user_owns_task function to return True
    with patch('src.mcp.tools.task_operations.verify_user_owns_task', return_value=True), \
         patch('src.mcp.tools.task_operations.async_session_factory') as mock_factory:
        mock_session = AsyncMock()
        mock_session.execute.side_effect = SQLAlchemyError("Database error")
        mock_factory.return_value.__aenter__.return_value = mock_session

        result = await delete_task("user123", 1)

    # Assert the response is an error
    assert result["status"] == "error"
    assert result["error_code"] == "DATABASE_ERROR"


@pytest.mark.asyncio
async def test_delete_task_unexpected_error():
    """Test handling of unexpected errors during task deletion"""
    user_id = "user123"

    # Force an unexpected error by mocking validate_user_id
    with patch('src.mcp.tools.task_operations.validate_user_id', side_effect=Exception("Unexpected error")):
        result = await delete_task(user_id, 1)

    # Assert the response is an error
    assert result["status"] == "error"
    assert result["error_code"] == "UNEXPECTED_ERROR"