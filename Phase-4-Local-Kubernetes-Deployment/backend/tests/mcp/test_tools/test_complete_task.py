"""
Unit tests for the complete_task function
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from src.mcp.tools.task_operations import complete_task
from src.models.task import Task


@pytest.mark.asyncio
async def test_complete_task_success():
    """Test successful task completion"""
    user_id = "user123"
    task_id = 1
    completed = True

    # Create mock task object
    mock_task = MagicMock()
    mock_task.id = task_id
    mock_task.user_id = user_id
    mock_task.title = "Test Task"
    mock_task.description = "Test Description"
    mock_task.completed = completed
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
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()

    # Mock the verify_user_owns_task function to return True
    with patch('src.mcp.tools.task_operations.verify_user_owns_task', return_value=True), \
         patch('src.mcp.tools.task_operations.async_session_factory') as mock_factory:
        mock_factory.return_value.__aenter__.return_value = mock_session
        result = await complete_task(user_id, task_id, completed)

    # Assert the response is successful
    assert result["status"] == "success"
    assert result["task"].completed == completed


@pytest.mark.asyncio
async def test_complete_task_mark_incomplete():
    """Test successful task marking as incomplete"""
    user_id = "user123"
    task_id = 1
    completed = False

    # Create mock task object
    mock_task = MagicMock()
    mock_task.id = task_id
    mock_task.user_id = user_id
    mock_task.title = "Test Task"
    mock_task.description = "Test Description"
    mock_task.completed = completed
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
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()

    # Mock the verify_user_owns_task function to return True
    with patch('src.mcp.tools.task_operations.verify_user_owns_task', return_value=True), \
         patch('src.mcp.tools.task_operations.async_session_factory') as mock_factory:
        mock_factory.return_value.__aenter__.return_value = mock_session
        result = await complete_task(user_id, task_id, completed)

    # Assert the response is successful
    assert result["status"] == "success"
    assert result["task"].completed == completed


@pytest.mark.asyncio
async def test_complete_task_invalid_user_id():
    """Test completing task with invalid user ID"""
    result = await complete_task("", 1, True)  # Invalid user ID

    # Assert the response is an error
    assert result["status"] == "error"
    assert result["error_code"] == "INVALID_USER_ID"


@pytest.mark.asyncio
async def test_complete_task_not_authorized():
    """Test completing task when user doesn't own the task"""
    # Mock the verify_user_owns_task function to return False
    with patch('src.mcp.tools.task_operations.verify_user_owns_task', return_value=False):
        result = await complete_task("other_user", 1, True)

    # Assert the response is an error
    assert result["status"] == "error"
    assert result["error_code"] == "TASK_NOT_FOUND_OR_UNAUTHORIZED"


@pytest.mark.asyncio
async def test_complete_task_unexpected_error():
    """Test handling of unexpected errors during task completion"""
    user_id = "user123"

    # Force an unexpected error by mocking validate_user_id
    with patch('src.mcp.tools.task_operations.validate_user_id', side_effect=Exception("Unexpected error")):
        result = await complete_task(user_id, 1, True)

    # Assert the response is an error
    assert result["status"] == "error"
    assert result["error_code"] == "UNEXPECTED_ERROR"


@pytest.mark.asyncio
async def test_complete_task_database_error():
    """Test handling of database errors during task completion"""
    from sqlalchemy.exc import SQLAlchemyError

    # Mock the verify_user_owns_task function to return True
    with patch('src.mcp.tools.task_operations.verify_user_owns_task', return_value=True), \
         patch('src.mcp.tools.task_operations.async_session_factory') as mock_factory:
        mock_session = AsyncMock()
        mock_session.execute.side_effect = SQLAlchemyError("Database error")
        mock_factory.return_value.__aenter__.return_value = mock_session

        result = await complete_task("user123", 1, True)

    # Assert the response is an error
    assert result["status"] == "error"
    assert result["error_code"] == "DATABASE_ERROR"