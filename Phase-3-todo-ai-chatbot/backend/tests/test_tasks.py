"""Test cases for task API endpoints."""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_task(client: AsyncClient, auth_headers: dict, clean_db):
    """Test creating a task returns 201 with task details."""
    response = await client.post(
        "/api/test-user-123/tasks",
        json={"title": "Test task", "description": "Test description"},
        headers=auth_headers
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test task"
    assert data["description"] == "Test description"
    assert data["completed"] is False
    assert data["user_id"] == "test-user-123"
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


@pytest.mark.asyncio
async def test_list_tasks(client: AsyncClient, auth_headers: dict, clean_db):
    """Test listing tasks returns list of user's tasks."""
    # Create some tasks first
    await client.post(
        "/api/test-user-123/tasks",
        json={"title": "Task 1"},
        headers=auth_headers
    )
    await client.post(
        "/api/test-user-123/tasks",
        json={"title": "Task 2"},
        headers=auth_headers
    )

    response = await client.get(
        "/api/test-user-123/tasks",
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    # Tasks should be ordered by created_at desc (newest first)
    assert data[0]["title"] == "Task 2"
    assert data[1]["title"] == "Task 1"


@pytest.mark.asyncio
async def test_create_task_validation_error(client: AsyncClient, auth_headers: dict, clean_db):
    """Test creating task without title returns 422."""
    response = await client.post(
        "/api/test-user-123/tasks",
        json={},
        headers=auth_headers
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_task_empty_title_validation_error(client: AsyncClient, auth_headers: dict, clean_db):
    """Test creating task with empty title returns 422."""
    response = await client.post(
        "/api/test-user-123/tasks",
        json={"title": ""},
        headers=auth_headers
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_single_task(client: AsyncClient, auth_headers: dict, clean_db):
    """Test getting a single task returns the task."""
    # Create a task
    create_response = await client.post(
        "/api/test-user-123/tasks",
        json={"title": "Test task"},
        headers=auth_headers
    )
    task_id = create_response.json()["id"]

    response = await client.get(
        f"/api/test-user-123/tasks/{task_id}",
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Test task"


@pytest.mark.asyncio
async def test_get_single_task_not_found(client: AsyncClient, auth_headers: dict, clean_db):
    """Test getting non-existent task returns 404."""
    response = await client.get(
        "/api/test-user-123/tasks/99999",
        headers=auth_headers
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_task(client: AsyncClient, auth_headers: dict, clean_db):
    """Test updating a task returns updated task."""
    # Create a task
    create_response = await client.post(
        "/api/test-user-123/tasks",
        json={"title": "Original title"},
        headers=auth_headers
    )
    task_id = create_response.json()["id"]

    response = await client.put(
        f"/api/test-user-123/tasks/{task_id}",
        json={"title": "Updated title", "completed": True},
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated title"
    assert data["completed"] is True


@pytest.mark.asyncio
async def test_delete_task(client: AsyncClient, auth_headers: dict, clean_db):
    """Test deleting a task returns 204."""
    # Create a task
    create_response = await client.post(
        "/api/test-user-123/tasks",
        json={"title": "Task to delete"},
        headers=auth_headers
    )
    task_id = create_response.json()["id"]

    response = await client.delete(
        f"/api/test-user-123/tasks/{task_id}",
        headers=auth_headers
    )

    assert response.status_code == 204

    # Verify task is deleted
    get_response = await client.get(
        f"/api/test-user-123/tasks/{task_id}",
        headers=auth_headers
    )
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_update_task_validation_error(client: AsyncClient, auth_headers: dict, clean_db):
    """Test updating task with invalid data returns 422."""
    # Create a task
    create_response = await client.post(
        "/api/test-user-123/tasks",
        json={"title": "Test task"},
        headers=auth_headers
    )
    task_id = create_response.json()["id"]

    response = await client.put(
        f"/api/test-user-123/tasks/{task_id}",
        json={"title": ""},
        headers=auth_headers
    )

    assert response.status_code == 422


# User Story 2: Task Completion Lifecycle Tests

@pytest.mark.asyncio
async def test_toggle_completion_to_complete(client: AsyncClient, auth_headers: dict, clean_db):
    """Test PATCH changes false to true."""
    # Create a task
    create_response = await client.post(
        "/api/test-user-123/tasks",
        json={"title": "Test task"},
        headers=auth_headers
    )
    task_id = create_response.json()["id"]

    response = await client.patch(
        f"/api/test-user-123/tasks/{task_id}/complete",
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    assert data["completed"] is True


@pytest.mark.asyncio
async def test_toggle_completion_to_incomplete(client: AsyncClient, auth_headers: dict, clean_db):
    """Test PATCH changes true to false."""
    # Create and complete a task
    create_response = await client.post(
        "/api/test-user-123/tasks",
        json={"title": "Test task"},
        headers=auth_headers
    )
    task_id = create_response.json()["id"]
    await client.patch(
        f"/api/test-user-123/tasks/{task_id}/complete",
        headers=auth_headers
    )

    # Toggle again
    response = await client.patch(
        f"/api/test-user-123/tasks/{task_id}/complete",
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    assert data["completed"] is False


@pytest.mark.asyncio
async def test_toggle_completion_idempotent(client: AsyncClient, auth_headers: dict, clean_db):
    """Test calling PATCH twice on true returns true."""
    # Create and complete a task
    create_response = await client.post(
        "/api/test-user-123/tasks",
        json={"title": "Test task"},
        headers=auth_headers
    )
    task_id = create_response.json()["id"]
    await client.patch(
        f"/api/test-user-123/tasks/{task_id}/complete",
        headers=auth_headers
    )

    # Toggle twice
    response = await client.patch(
        f"/api/test-user-123/tasks/{task_id}/complete",
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    assert data["completed"] is False


# User Story 3: Secure User Isolation Tests

@pytest.mark.asyncio
async def test_get_tasks_unauthorized_cross_user(client: AsyncClient, other_user_auth_headers: dict, clean_db):
    """Test GET User A's tasks with User B's JWT returns 401."""
    response = await client.get(
        "/api/test-user-123/tasks",
        headers=other_user_auth_headers
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_create_task_unauthorized_cross_user(client: AsyncClient, other_user_auth_headers: dict, clean_db):
    """Test POST to User A's tasks with User B's JWT returns 401."""
    response = await client.post(
        "/api/test-user-123/tasks",
        json={"title": "Hacked task"},
        headers=other_user_auth_headers
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_delete_task_unauthorized_cross_user(client: AsyncClient, other_user_auth_headers: dict, clean_db):
    """Test DELETE User A's task with User B's JWT returns 401."""
    # Create task as user A
    create_response = await client.post(
        "/api/test-user-123/tasks",
        json={"title": "User A task"},
        headers={"Authorization": f"Bearer {create_test_token('test-user-123')}"}
    )
    task_id = create_response.json()["id"]

    # Try to delete as user B
    response = await client.delete(
        f"/api/test-user-123/tasks/{task_id}",
        headers=other_user_auth_headers
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_invalid_jwt_returns_401(client: AsyncClient, clean_db):
    """Test expired/invalid JWT returns 401 on any endpoint."""
    response = await client.get(
        "/api/test-user-123/tasks",
        headers={"Authorization": "Bearer invalid-token"}
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_missing_auth_returns_401(client: AsyncClient, clean_db):
    """Test missing Authorization header returns 401."""
    response = await client.get(
        "/api/test-user-123/tasks"
    )

    assert response.status_code == 401


# Helper function for creating tokens in tests
def create_test_token(user_id: str, expires_in: int = 3600) -> str:
    """Create a test JWT token for a user."""
    import time as time_module
    from jose import jwt
    from src.config import get_settings

    settings = get_settings()
    payload = {
        "sub": user_id,
        "exp": time_module.time() + expires_in
    }
    return jwt.encode(payload, settings.better_auth_secret, algorithm="HS256")