"""
Unit tests for the add_task function
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from src.mcp.tools.task_operations import add_task
from src.mcp.schemas.task_schemas import AddTaskRequest
from sqlmodel import select
from src.models.task import Task


@pytest.mark.asyncio
async def test_add_task_success():
    """Test successful task creation"""
    # Mock request data
    request = AddTaskRequest(
        user_id="user123",
        title="Test Task",
        description="Test Description",
        priority="medium"
    )

    # Mock the database session
    mock_session = AsyncMock()
    mock_session.add = MagicMock()
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()

    # Mock the task object that gets created
    mock_task = MagicMock()
    mock_task.id = 1
    mock_task.user_id = "user123"
    mock_task.title = "Test Task"
    mock_task.description = "Test Description"
    mock_task.completed = False
    mock_task.priority = "medium"
    mock_task.created_at = "2023-01-01T00:00:00"
    mock_task.updated_at = "2023-01-01T00:00:00"

    # Patch the async session factory
    with patch('src.mcp.tools.task_operations.async_session_factory') as mock_factory:
        mock_factory.return_value.__aenter__.return_value = mock_session
        result = await add_task(request)

    # Assert the response is successful
    assert result.status == "success"
    assert result.message == "Task created successfully"
    assert result.task.title == "Test Task"


@pytest.mark.asyncio
async def test_add_task_invalid_user_id():
    """Test adding task with invalid user ID"""
    request = AddTaskRequest(
        user_id="",  # Invalid user ID
        title="Test Task",
        description="Test Description",
        priority="medium"
    )

    result = await add_task(request)

    # Assert the response is an error
    assert result.status == "error"
    assert result.error_code == "INVALID_USER_ID"


@pytest.mark.asyncio
async def test_add_task_invalid_title():
    """Test adding task with invalid title"""
    request = AddTaskRequest(
        user_id="user123",
        title="",  # Invalid title
        description="Test Description",
        priority="medium"
    )

    result = await add_task(request)

    # Assert the response is an error
    assert result.status == "error"
    assert result.error_code == "INVALID_TITLE"


@pytest.mark.asyncio
async def test_add_task_empty_title():
    """Test adding task with empty title after stripping"""
    request = AddTaskRequest(
        user_id="user123",
        title="   ",  # Whitespace only title
        description="Test Description",
        priority="medium"
    )

    result = await add_task(request)

    # Assert the response is an error
    assert result.status == "error"
    assert result.error_code == "INVALID_TITLE"


@pytest.mark.asyncio
async def test_add_task_long_title():
    """Test adding task with title that's too long"""
    request = AddTaskRequest(
        user_id="user123",
        title="x" * 201,  # Too long title
        description="Test Description",
        priority="medium"
    )

    result = await add_task(request)

    # Assert the response is an error
    assert result.status == "error"
    assert result.error_code == "INVALID_TITLE"


@pytest.mark.asyncio
async def test_add_task_database_error():
    """Test handling of database errors during task creation"""
    from sqlalchemy.exc import SQLAlchemyError

    request = AddTaskRequest(
        user_id="user123",
        title="Test Task",
        description="Test Description",
        priority="medium"
    )

    # Mock a database error
    mock_session = AsyncMock()
    mock_session.add = MagicMock()
    mock_session.commit.side_effect = SQLAlchemyError("Database error")
    mock_session.rollback = AsyncMock()

    with patch('src.mcp.tools.task_operations.async_session_factory') as mock_factory:
        mock_factory.return_value.__aenter__.return_value = mock_session
        result = await add_task(request)

    # Assert the response is an error
    assert result.status == "error"
    assert result.error_code == "DATABASE_ERROR"


@pytest.mark.asyncio
async def test_add_task_unexpected_error():
    """Test handling of unexpected errors during task creation"""
    request = AddTaskRequest(
        user_id="user123",
        title="Test Task",
        description="Test Description",
        priority="medium"
    )

    # Force an unexpected error
    with patch('src.mcp.tools.task_operations.validate_user_id', side_effect=Exception("Unexpected error")):
        result = await add_task(request)

    # Assert the response is an error
    assert result.status == "error"
    assert result.error_code == "UNEXPECTED_ERROR"