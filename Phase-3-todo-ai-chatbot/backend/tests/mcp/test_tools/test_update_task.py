"""
Unit tests for the update_task function
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from src.mcp.tools.task_operations import update_task
from src.models.task import Task


@pytest.mark.asyncio
async def test_update_task_success():
    """Test successful task update"""
    user_id = "user123"
    task_id = 1
    new_title = "Updated Title"

    # Create mock task object
    mock_task = MagicMock()
    mock_task.id = task_id
    mock_task.user_id = user_id
    mock_task.title = new_title
    mock_task.description = "Updated Description"
    mock_task.completed = True
    mock_task.created_at = "2023-01-01T00:00:00"
    mock_task.updated_at = "2023-01-02T00:00:00"
    mock_task.priority = "high"

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
        result = await update_task(user_id, task_id, title=new_title)

    # Assert the response is successful
    assert result["status"] == "success"
    assert result["task"].title == new_title


@pytest.mark.asyncio
async def test_update_task_invalid_user_id():
    """Test updating task with invalid user ID"""
    result = await update_task("", 1, title="New Title")  # Invalid user ID

    # Assert the response is an error
    assert result["status"] == "error"
    assert result["error_code"] == "INVALID_USER_ID"


@pytest.mark.asyncio
async def test_update_task_not_authorized():
    """Test updating task when user doesn't own the task"""
    # Mock the verify_user_owns_task function to return False
    with patch('src.mcp.tools.task_operations.verify_user_owns_task', return_value=False):
        result = await update_task("other_user", 1, title="New Title")

    # Assert the response is an error
    assert result["status"] == "error"
    assert result["error_code"] == "TASK_NOT_FOUND_OR_UNAUTHORIZED"


@pytest.mark.asyncio
async def test_update_task_not_found():
    """Test updating task that doesn't exist"""
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
        result = await update_task("user123", 999, title="New Title")  # Non-existent task

    # Assert the response is an error
    assert result["status"] == "error"
    assert result["error_code"] == "TASK_NOT_FOUND"


@pytest.mark.asyncio
async def test_update_task_with_description():
    """Test updating task with description"""
    user_id = "user123"
    task_id = 1
    new_description = "Updated Description"

    # Create mock task object
    mock_task = MagicMock()
    mock_task.id = task_id
    mock_task.user_id = user_id
    mock_task.title = "Original Title"
    mock_task.description = new_description
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
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()

    # Mock the verify_user_owns_task function to return True
    with patch('src.mcp.tools.task_operations.verify_user_owns_task', return_value=True), \
         patch('src.mcp.tools.task_operations.async_session_factory') as mock_factory:
        mock_factory.return_value.__aenter__.return_value = mock_session
        result = await update_task(user_id, task_id, description=new_description)

    # Assert the response is successful and description was updated
    assert result["status"] == "success"
    assert result["task"].description == new_description


@pytest.mark.asyncio
async def test_update_task_with_priority():
    """Test updating task with priority"""
    user_id = "user123"
    task_id = 1
    new_priority = "high"

    # Create mock task object
    mock_task = MagicMock()
    mock_task.id = task_id
    mock_task.user_id = user_id
    mock_task.title = "Original Title"
    mock_task.description = "Original Description"
    mock_task.completed = False
    mock_task.created_at = "2023-01-01T00:00:00"
    mock_task.updated_at = "2023-01-02T00:00:00"
    mock_task.priority = new_priority

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
        result = await update_task(user_id, task_id, priority=new_priority)

    # Assert the response is successful and priority was updated
    assert result["status"] == "success"
    assert result["task"].priority == new_priority


@pytest.mark.asyncio
async def test_update_task_with_completion_status():
    """Test updating task with completion status"""
    user_id = "user123"
    task_id = 1
    new_completed = True

    # Create mock task object
    mock_task = MagicMock()
    mock_task.id = task_id
    mock_task.user_id = user_id
    mock_task.title = "Original Title"
    mock_task.description = "Original Description"
    mock_task.completed = new_completed  # Updated status
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
        result = await update_task(user_id, task_id, completed=new_completed)

    # Assert the response is successful and completion status was updated
    assert result["status"] == "success"
    assert result["task"].completed == new_completed


@pytest.mark.asyncio
async def test_update_task_database_error():
    """Test handling of database errors during task update"""
    from sqlalchemy.exc import SQLAlchemyError

    # Mock the verify_user_owns_task function to return True
    with patch('src.mcp.tools.task_operations.verify_user_owns_task', return_value=True), \
         patch('src.mcp.tools.task_operations.async_session_factory') as mock_factory:
        mock_session = AsyncMock()
        mock_session.execute.side_effect = SQLAlchemyError("Database error")
        mock_factory.return_value.__aenter__.return_value = mock_session

        result = await update_task("user123", 1, title="New Title")

    # Assert the response is an error
    assert result["status"] == "error"
    assert result["error_code"] == "DATABASE_ERROR"


@pytest.mark.asyncio
async def test_update_task_invalid_title():
    """Test updating task with invalid title"""
    # Mock the verify_user_owns_task function to return True
    with patch('src.mcp.tools.task_operations.verify_user_owns_task', return_value=True):
        # Try to update with empty title
        result = await update_task("user123", 1, title="")

    # Assert the response is an error
    assert result["status"] == "error"
    assert result["error_code"] == "INVALID_TITLE"