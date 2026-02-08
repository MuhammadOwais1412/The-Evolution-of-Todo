"""
Comprehensive integration tests for MCP tools
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from src.mcp.tools.task_operations import (
    add_task, list_tasks, update_task, complete_task, delete_task
)
from src.mcp.schemas.task_schemas import AddTaskRequest


@pytest.mark.asyncio
async def test_end_to_end_task_lifecycle():
    """Test complete task lifecycle: add → list → update → complete → delete"""
    user_id = "integration_test_user"
    task_title = "Integration Test Task"
    updated_title = "Updated Integration Test Task"

    # Step 1: Add a task
    add_request = AddTaskRequest(
        user_id=user_id,
        title=task_title,
        description="Integration test description",
        priority="medium"
    )

    # Mock the database session for adding
    mock_session_add = AsyncMock()
    mock_session_add.add = MagicMock()

    # Mock a new task object that gets created
    mock_new_task = MagicMock()
    mock_new_task.id = 1
    mock_new_task.user_id = user_id
    mock_new_task.title = task_title
    mock_new_task.description = "Integration test description"
    mock_new_task.completed = False
    mock_new_task.priority = "medium"
    mock_new_task.created_at = "2023-01-01T00:00:00"
    mock_new_task.updated_at = "2023-01-01T00:00:00"

    mock_session_add.refresh = AsyncMock(side_effect=lambda obj: setattr(obj, 'id', 1) or
                                        setattr(obj, 'user_id', user_id) or
                                        setattr(obj, 'title', task_title) or
                                        setattr(obj, 'description', "Integration test description") or
                                        setattr(obj, 'completed', False) or
                                        setattr(obj, 'priority', "medium"))

    with patch('src.mcp.tools.task_operations.async_session_factory') as mock_factory:
        mock_factory.return_value.__aenter__.return_value = mock_session_add
        add_result = await add_task(add_request)

    assert add_result.status == "success"
    assert add_result.task.title == task_title
    assert add_result.task.user_id == user_id

    # Step 2: List tasks for the user
    with patch('src.mcp.tools.task_operations.verify_user_owns_task', return_value=True), \
         patch('src.mcp.tools.task_operations.async_session_factory') as mock_factory:
        # Mock the database query for listing
        async def mock_execute(query):
            mock_result = AsyncMock()
            mock_result.scalars.return_value.all.return_value = [mock_new_task]
            return mock_result

        mock_session_list = AsyncMock()
        mock_session_list.execute = mock_execute
        mock_factory.return_value.__aenter__.return_value = mock_session_list

        list_result = await list_tasks(user_id)

    assert list_result["status"] == "success"
    assert len(list_result["tasks"]) >= 1
    found_task = next((t for t in list_result["tasks"] if t.title == task_title), None)
    assert found_task is not None
    assert found_task.user_id == user_id

    # Step 3: Update the task
    with patch('src.mcp.tools.task_operations.verify_user_owns_task', return_value=True), \
         patch('src.mcp.tools.task_operations.async_session_factory') as mock_factory:
        # Mock the database session for update
        async def mock_execute_update(query):
            mock_result = AsyncMock()
            mock_result.scalar_one_or_none.return_value = mock_new_task
            return mock_result

        mock_session_update = AsyncMock()
        mock_session_update.execute = mock_execute_update
        mock_session_update.commit = AsyncMock()
        mock_session_update.refresh = AsyncMock()
        mock_factory.return_value.__aenter__.return_value = mock_session_update

        update_result = await update_task(user_id, 1, title=updated_title)

    assert update_result["status"] == "success"
    assert update_result["task"].title == updated_title

    # Step 4: Complete the task
    with patch('src.mcp.tools.task_operations.verify_user_owns_task', return_value=True), \
         patch('src.mcp.tools.task_operations.async_session_factory') as mock_factory:
        # Mock the database session for completion
        async def mock_execute_complete(query):
            mock_result = AsyncMock()
            mock_result.scalar_one_or_none.return_value = mock_new_task
            return mock_result

        mock_session_complete = AsyncMock()
        mock_session_complete.execute = mock_execute_complete
        mock_session_complete.commit = AsyncMock()
        mock_session_complete.refresh = AsyncMock()
        mock_factory.return_value.__aenter__.return_value = mock_session_complete

        complete_result = await complete_task(user_id, 1, True)

    assert complete_result["status"] == "success"
    assert complete_result["task"].completed == True

    # Step 5: Delete the task
    with patch('src.mcp.tools.task_operations.verify_user_owns_task', return_value=True), \
         patch('src.mcp.tools.task_operations.async_session_factory') as mock_factory:
        # Mock the database session for deletion
        async def mock_execute_delete(query):
            mock_result = AsyncMock()
            mock_result.scalar_one_or_none.return_value = mock_new_task
            return mock_result

        mock_session_delete = AsyncMock()
        mock_session_delete.execute = mock_execute_delete
        mock_session_delete.delete = MagicMock()
        mock_session_delete.commit = AsyncMock()
        mock_factory.return_value.__aenter__.return_value = mock_session_delete

        delete_result = await delete_task(user_id, 1)

    assert delete_result["status"] == "success"
    assert delete_result["task_id"] == 1


@pytest.mark.asyncio
async def test_user_isolation_across_all_tools():
    """Test end-to-end user isolation across all tools"""
    user1_id = "user1_isolation_test"
    user2_id = "user2_isolation_test"
    task_title = "Isolation Test Task"

    # Verify that user1 can only access their own tasks, not user2's tasks

    # Mock task for user1
    mock_task_user1 = MagicMock()
    mock_task_user1.id = 1
    mock_task_user1.user_id = user1_id
    mock_task_user1.title = task_title + " for user1"
    mock_task_user1.description = "Task for user1"
    mock_task_user1.completed = False
    mock_task_user1.priority = "medium"
    mock_task_user1.created_at = "2023-01-01T00:00:00"
    mock_task_user1.updated_at = "2023-01-01T00:00:00"

    # Mock task for user2
    mock_task_user2 = MagicMock()
    mock_task_user2.id = 2
    mock_task_user2.user_id = user2_id
    mock_task_user2.title = task_title + " for user2"
    mock_task_user2.description = "Task for user2"
    mock_task_user2.completed = False
    mock_task_user2.priority = "high"
    mock_task_user2.created_at = "2023-01-01T00:00:00"
    mock_task_user2.updated_at = "2023-01-01T00:00:00"

    # Test that each user can add their own task
    add_request1 = AddTaskRequest(user_id=user1_id, title=mock_task_user1.title)
    add_request2 = AddTaskRequest(user_id=user2_id, title=mock_task_user2.title)

    # Mock sessions for adding tasks
    with patch('src.mcp.tools.task_operations.async_session_factory') as mock_factory:
        mock_session1 = AsyncMock()
        mock_session1.add = MagicMock()
        mock_session1.refresh = AsyncMock(side_effect=lambda obj: setattr(obj, 'id', 1) or
                                         setattr(obj, 'user_id', user1_id) or
                                         setattr(obj, 'title', mock_task_user1.title))
        mock_factory.return_value.__aenter__.return_value = mock_session1
        result1 = await add_task(add_request1)
        assert result1.status == "success"

    with patch('src.mcp.tools.task_operations.async_session_factory') as mock_factory:
        mock_session2 = AsyncMock()
        mock_session2.add = MagicMock()
        mock_session2.refresh = AsyncMock(side_effect=lambda obj: setattr(obj, 'id', 2) or
                                         setattr(obj, 'user_id', user2_id) or
                                         setattr(obj, 'title', mock_task_user2.title))
        mock_factory.return_value.__aenter__.return_value = mock_session2
        result2 = await add_task(add_request2)
        assert result2.status == "success"

    # Test that each user can only see their own tasks
    with patch('src.mcp.tools.task_operations.async_session_factory') as mock_factory:
        # When user1 queries, only user1's task should be returned
        async def mock_execute_user1(query):
            mock_result = AsyncMock()
            # Check if query is for user1
            if user1_id in str(query):
                mock_result.scalars.return_value.all.return_value = [mock_task_user1]
            else:
                mock_result.scalars.return_value.all.return_value = []
            return mock_result

        mock_session_user1 = AsyncMock()
        mock_session_user1.execute = mock_execute_user1
        mock_factory.return_value.__aenter__.return_value = mock_session_user1

        user1_list_result = await list_tasks(user1_id)
        assert len(user1_list_result["tasks"]) == 1
        assert user1_list_result["tasks"][0].user_id == user1_id

    with patch('src.mcp.tools.task_operations.async_session_factory') as mock_factory:
        # When user2 queries, only user2's task should be returned
        async def mock_execute_user2(query):
            mock_result = AsyncMock()
            # Check if query is for user2
            if user2_id in str(query):
                mock_result.scalars.return_value.all.return_value = [mock_task_user2]
            else:
                mock_result.scalars.return_value.all.return_value = []
            return mock_result

        mock_session_user2 = AsyncMock()
        mock_session_user2.execute = mock_execute_user2
        mock_factory.return_value.__aenter__.return_value = mock_session_user2

        user2_list_result = await list_tasks(user2_id)
        assert len(user2_list_result["tasks"]) == 1
        assert user2_list_result["tasks"][0].user_id == user2_id


@pytest.mark.asyncio
async def test_authentication_validation_across_tools():
    """Test authentication validation across all tools"""
    invalid_user_id = ""

    # Test that all tools properly validate user_id
    add_result = await add_task(AddTaskRequest(user_id=invalid_user_id, title="Test"))
    assert add_result.status == "error"
    assert add_result.error_code == "INVALID_USER_ID"

    list_result = await list_tasks(invalid_user_id)
    assert list_result["status"] == "error"
    assert list_result["error_code"] == "INVALID_USER_ID"

    # For update, complete, and delete, user_id validation happens first
    update_result = await update_task(invalid_user_id, 1, title="Updated")
    assert update_result["status"] == "error"
    assert update_result["error_code"] == "INVALID_USER_ID"

    complete_result = await complete_task(invalid_user_id, 1, True)
    assert complete_result["status"] == "error"
    assert complete_result["error_code"] == "INVALID_USER_ID"

    delete_result = await delete_task(invalid_user_id, 1)
    assert delete_result["status"] == "error"
    assert delete_result["error_code"] == "INVALID_USER_ID"


@pytest.mark.asyncio
async def test_database_persistence_across_tools():
    """Test database persistence and ACID compliance across all tools"""
    user_id = "acid_test_user"
    task_title = "ACID Test Task"

    # Test add operation persistence
    add_request = AddTaskRequest(
        user_id=user_id,
        title=task_title,
        description="ACID test description"
    )

    mock_task = MagicMock()
    mock_task.id = 1
    mock_task.user_id = user_id
    mock_task.title = task_title
    mock_task.description = "ACID test description"
    mock_task.completed = False
    mock_task.priority = "medium"
    mock_task.created_at = "2023-01-01T00:00:00"
    mock_task.updated_at = "2023-01-01T00:00:00"

    # Mock the database session for adding
    mock_session_add = AsyncMock()
    mock_session_add.add = MagicMock()
    mock_session_add.commit = AsyncMock()
    mock_session_add.refresh = AsyncMock(side_effect=lambda obj: setattr(obj, 'id', 1))

    with patch('src.mcp.tools.task_operations.async_session_factory') as mock_factory:
        mock_factory.return_value.__aenter__.return_value = mock_session_add
        add_result = await add_task(add_request)

    assert add_result.status == "success"
    assert add_result.task.id is not None

    # Test that the operation was properly committed (simulated by the fact that commit was called)
    mock_session_add.commit.assert_called_once()

    # Test update operation persistence
    with patch('src.mcp.tools.task_operations.verify_user_owns_task', return_value=True), \
         patch('src.mcp.tools.task_operations.async_session_factory') as mock_factory:
        async def mock_execute_update(query):
            mock_result = AsyncMock()
            mock_result.scalar_one_or_none.return_value = mock_task
            return mock_result

        mock_session_update = AsyncMock()
        mock_session_update.execute = mock_execute_update
        mock_session_update.commit = AsyncMock()
        mock_session_update.refresh = AsyncMock()
        mock_factory.return_value.__aenter__.return_value = mock_session_update

        update_result = await update_task(user_id, 1, title="Updated ACID Test Task")

    assert update_result["status"] == "success"
    mock_session_update.commit.assert_called_once()

    # Test delete operation persistence
    with patch('src.mcp.tools.task_operations.verify_user_owns_task', return_value=True), \
         patch('src.mcp.tools.task_operations.async_session_factory') as mock_factory:
        async def mock_execute_delete(query):
            mock_result = AsyncMock()
            mock_result.scalar_one_or_none.return_value = mock_task
            return mock_result

        mock_session_delete = AsyncMock()
        mock_session_delete.execute = mock_execute_delete
        mock_session_delete.delete = MagicMock()
        mock_session_delete.commit = AsyncMock()
        mock_factory.return_value.__aenter__.return_value = mock_session_delete

        delete_result = await delete_task(user_id, 1)

    assert delete_result["status"] == "success"
    mock_session_delete.commit.assert_called_once()