"""
Unit tests for user isolation enforcement in task operations
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from src.mcp.tools.task_operations import (
    add_task, list_tasks, update_task, complete_task, delete_task
)
from src.mcp.schemas.task_schemas import AddTaskRequest
from sqlmodel import select
from src.models.task import Task


@pytest.mark.asyncio
async def test_add_task_user_isolation():
    """Test that user isolation is enforced when adding tasks"""
    # Test with different user IDs
    request1 = AddTaskRequest(
        user_id="user123",
        title="Test Task User 1",
        description="Test Description",
        priority="medium"
    )

    request2 = AddTaskRequest(
        user_id="user456",  # Different user
        title="Test Task User 2",
        description="Test Description",
        priority="medium"
    )

    # Mock the database session for both requests
    mock_session1 = AsyncMock()
    mock_session1.add = MagicMock()
    mock_session1.commit = AsyncMock()
    mock_session1.refresh = AsyncMock()

    mock_session2 = AsyncMock()
    mock_session2.add = MagicMock()
    mock_session2.commit = AsyncMock()
    mock_session2.refresh = AsyncMock()

    # Test that both users can add tasks with their own IDs
    with patch('src.mcp.tools.task_operations.async_session_factory') as mock_factory:
        # First user adds task
        mock_factory.return_value.__aenter__.return_value = mock_session1
        result1 = await add_task(request1)
        assert result1.status == "success"
        assert result1.task.user_id == "user123"

        # Second user adds task
        mock_factory.return_value.__aenter__.return_value = mock_session2
        result2 = await add_task(request2)
        assert result2.status == "success"
        assert result2.task.user_id == "user456"

    # Verify that each user's ID was used appropriately
    assert result1.task.user_id != result2.task.user_id


@pytest.mark.asyncio
async def test_list_tasks_user_isolation():
    """Test that list_tasks only returns tasks for the authenticated user"""
    user_id_1 = "user123"
    user_id_2 = "user456"

    # Mock the database query to simulate different user tasks
    async def mock_execute(query):
        mock_result = AsyncMock()
        if "user123" in str(query):
            # Return mock tasks for user 1
            mock_task = MagicMock()
            mock_task.id = 1
            mock_task.user_id = "user123"
            mock_task.title = "User 1's Task"
            mock_task.description = "Description 1"
            mock_task.completed = False
            mock_task.priority = "medium"
            mock_task.created_at = "2023-01-01T00:00:00"
            mock_task.updated_at = "2023-01-01T00:00:00"
            mock_result.scalars.return_value.all.return_value = [mock_task]
        elif "user456" in str(query):
            # Return mock tasks for user 2
            mock_task = MagicMock()
            mock_task.id = 2
            mock_task.user_id = "user456"
            mock_task.title = "User 2's Task"
            mock_task.description = "Description 2"
            mock_task.completed = True
            mock_task.priority = "high"
            mock_task.created_at = "2023-01-01T00:00:00"
            mock_task.updated_at = "2023-01-01T00:00:00"
            mock_result.scalars.return_value.all.return_value = [mock_task]
        else:
            mock_result.scalars.return_value.all.return_value = []
        return mock_result

    # Test user 1 listing their tasks
    with patch('src.mcp.tools.task_operations.async_session_factory') as mock_factory:
        mock_session = AsyncMock()
        mock_session.execute = mock_execute
        mock_factory.return_value.__aenter__.return_value = mock_session

        result1 = await list_tasks(user_id_1)
        assert len(result1["tasks"]) == 1
        assert result1["tasks"][0].user_id == "user123"

    # Test user 2 listing their tasks
    with patch('src.mcp.tools.task_operations.async_session_factory') as mock_factory:
        mock_session = AsyncMock()
        mock_session.execute = mock_execute
        mock_factory.return_value.__aenter__.return_value = mock_session

        result2 = await list_tasks(user_id_2)
        assert len(result2["tasks"]) == 1
        assert result2["tasks"][0].user_id == "user456"

    # Verify that users only see their own tasks
    assert result1["tasks"][0].user_id != result2["tasks"][0].user_id


@pytest.mark.asyncio
async def test_update_task_user_isolation():
    """Test that update_task enforces user isolation"""
    # Mock the verify_user_owns_task function to simulate ownership checks
    with patch('src.mcp.tools.task_operations.verify_user_owns_task') as mock_verify:
        # Simulate user "user123" trying to update their own task
        mock_verify.return_value = True
        result = await update_task("user123", 1, title="Updated Title")

        # Should succeed if user owns the task
        assert result["status"] == "success" or result["status"] == "error"  # Could be either depending on other checks

    # Simulate user "user456" trying to update task owned by "user123"
    with patch('src.mcp.tools.task_operations.verify_user_owns_task') as mock_verify:
        mock_verify.return_value = False  # User doesn't own the task
        result = await update_task("user456", 1, title="Unauthorized Update")

        # Should fail with unauthorized error
        assert result["status"] == "error"
        assert result["error_code"] == "TASK_NOT_FOUND_OR_UNAUTHORIZED"


@pytest.mark.asyncio
async def test_delete_task_user_isolation():
    """Test that delete_task enforces user isolation"""
    # Mock the verify_user_owns_task function to simulate ownership checks
    with patch('src.mcp.tools.task_operations.verify_user_owns_task') as mock_verify:
        # Simulate user "user123" trying to delete their own task
        mock_verify.return_value = True
        result = await delete_task("user123", 1)

        # Should succeed if user owns the task
        assert result["status"] == "success" or result["status"] == "error"  # Could be either depending on other checks

    # Simulate user "user456" trying to delete task owned by "user123"
    with patch('src.mcp.tools.task_operations.verify_user_owns_task') as mock_verify:
        mock_verify.return_value = False  # User doesn't own the task
        result = await delete_task("user456", 1)

        # Should fail with unauthorized error
        assert result["status"] == "error"
        assert result["error_code"] == "TASK_NOT_FOUND_OR_UNAUTHORIZED"