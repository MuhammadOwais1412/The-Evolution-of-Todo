"""
Unit tests for the list_tasks function
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from src.mcp.tools.task_operations import list_tasks
from src.models.task import Task


@pytest.mark.asyncio
async def test_list_tasks_success():
    """Test successful retrieval of tasks for a user"""
    user_id = "user123"

    # Create mock tasks
    mock_task1 = MagicMock()
    mock_task1.id = 1
    mock_task1.user_id = "user123"
    mock_task1.title = "Task 1"
    mock_task1.description = "Description 1"
    mock_task1.completed = False
    mock_task1.created_at = "2023-01-01T00:00:00"
    mock_task1.updated_at = "2023-01-01T00:00:00"
    mock_task1.priority = "medium"

    mock_task2 = MagicMock()
    mock_task2.id = 2
    mock_task2.user_id = "user123"
    mock_task2.title = "Task 2"
    mock_task2.description = "Description 2"
    mock_task2.completed = True
    mock_task2.created_at = "2023-01-01T00:00:00"
    mock_task2.updated_at = "2023-01-01T00:00:00"
    mock_task2.priority = "high"

    # Mock the database session
    async def mock_execute(query):
        mock_result = AsyncMock()
        mock_result.scalars.return_value.all.return_value = [mock_task1, mock_task2]
        return mock_result

    mock_session = AsyncMock()
    mock_session.execute = mock_execute

    with patch('src.mcp.tools.task_operations.async_session_factory') as mock_factory:
        mock_factory.return_value.__aenter__.return_value = mock_session
        result = await list_tasks(user_id)

    # Assert the response is successful
    assert result["status"] == "success"
    assert len(result["tasks"]) == 2
    assert result["tasks"][0].user_id == "user123"
    assert result["tasks"][1].user_id == "user123"


@pytest.mark.asyncio
async def test_list_tasks_no_tasks():
    """Test listing tasks when user has no tasks"""
    user_id = "user456"

    # Mock the database session to return no tasks
    async def mock_execute(query):
        mock_result = AsyncMock()
        mock_result.scalars.return_value.all.return_value = []
        return mock_result

    mock_session = AsyncMock()
    mock_session.execute = mock_execute

    with patch('src.mcp.tools.task_operations.async_session_factory') as mock_factory:
        mock_factory.return_value.__aenter__.return_value = mock_session
        result = await list_tasks(user_id)

    # Assert the response shows no tasks
    assert result["status"] == "success"
    assert len(result["tasks"]) == 0
    assert "0 tasks" in result["message"]


@pytest.mark.asyncio
async def test_list_tasks_pending_status():
    """Test listing tasks with 'pending' status filter"""
    user_id = "user789"

    # Create mock pending tasks
    mock_task = MagicMock()
    mock_task.id = 3
    mock_task.user_id = "user789"
    mock_task.title = "Pending Task"
    mock_task.description = "Description 3"
    mock_task.completed = False  # Pending task
    mock_task.created_at = "2023-01-01T00:00:00"
    mock_task.updated_at = "2023-01-01T00:00:00"
    mock_task.priority = "low"

    # Mock the database session
    async def mock_execute(query):
        mock_result = AsyncMock()
        # Only return tasks that match the query conditions for pending tasks
        if "completed" in str(query) and "False" in str(query):
            mock_result.scalars.return_value.all.return_value = [mock_task]
        else:
            mock_result.scalars.return_value.all.return_value = [mock_task]
        return mock_result

    mock_session = AsyncMock()
    mock_session.execute = mock_execute

    with patch('src.mcp.tools.task_operations.async_session_factory') as mock_factory:
        mock_factory.return_value.__aenter__.return_value = mock_session
        result = await list_tasks(user_id, status="pending")

    # Assert the response contains only pending tasks
    assert result["status"] == "success"
    assert len(result["tasks"]) == 1
    assert result["tasks"][0].completed == False


@pytest.mark.asyncio
async def test_list_tasks_completed_status():
    """Test listing tasks with 'completed' status filter"""
    user_id = "user101"

    # Create mock completed tasks
    mock_task = MagicMock()
    mock_task.id = 4
    mock_task.user_id = "user101"
    mock_task.title = "Completed Task"
    mock_task.description = "Description 4"
    mock_task.completed = True  # Completed task
    mock_task.created_at = "2023-01-01T00:00:00"
    mock_task.updated_at = "2023-01-01T00:00:00"
    mock_task.priority = "high"

    # Mock the database session
    async def mock_execute(query):
        mock_result = AsyncMock()
        # Only return tasks that match the query conditions for completed tasks
        if "completed" in str(query) and "True" in str(query):
            mock_result.scalars.return_value.all.return_value = [mock_task]
        else:
            mock_result.scalars.return_value.all.return_value = [mock_task]
        return mock_result

    mock_session = AsyncMock()
    mock_session.execute = mock_execute

    with patch('src.mcp.tools.task_operations.async_session_factory') as mock_factory:
        mock_factory.return_value.__aenter__.return_value = mock_session
        result = await list_tasks(user_id, status="completed")

    # Assert the response contains only completed tasks
    assert result["status"] == "success"
    assert len(result["tasks"]) == 1
    assert result["tasks"][0].completed == True


@pytest.mark.asyncio
async def test_list_tasks_invalid_user_id():
    """Test listing tasks with invalid user ID"""
    result = await list_tasks("")  # Invalid user ID

    # Assert the response is an error
    assert result["status"] == "error"
    assert result["error_code"] == "INVALID_USER_ID"


@pytest.mark.asyncio
async def test_list_tasks_database_error():
    """Test handling of database errors during task listing"""
    from sqlalchemy.exc import SQLAlchemyError

    user_id = "user112"

    # Mock the database session to raise an error
    mock_session = AsyncMock()
    mock_session.execute.side_effect = SQLAlchemyError("Database error")

    with patch('src.mcp.tools.task_operations.async_session_factory') as mock_factory:
        mock_factory.return_value.__aenter__.return_value = mock_session
        result = await list_tasks(user_id)

    # Assert the response is an error
    assert result["status"] == "error"
    assert result["error_code"] == "DATABASE_ERROR"


@pytest.mark.asyncio
async def test_list_tasks_unexpected_error():
    """Test handling of unexpected errors during task listing"""
    user_id = "user113"

    # Force an unexpected error by mocking validate_user_id
    with patch('src.mcp.tools.task_operations.validate_user_id', side_effect=Exception("Unexpected error")):
        result = await list_tasks(user_id)

    # Assert the response is an error
    assert result["status"] == "error"
    assert result["error_code"] == "UNEXPECTED_ERROR"