"""Task API endpoints with Pydantic models and JWT authentication."""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_session
from src.api.deps import get_current_user_id
from src.services.task_service import TaskService


# Pydantic models for request/response
class TaskCreate(BaseModel):
    """Schema for creating a task."""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=5000)


class TaskRead(BaseModel):
    """Schema for reading a task."""
    id: int
    title: str
    description: Optional[str]
    completed: bool
    user_id: str
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


class TaskUpdate(BaseModel):
    """Schema for updating a task."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=5000)
    completed: Optional[bool] = None


class ErrorResponse(BaseModel):
    """Schema for error responses."""
    error: str
    message: str
    details: Optional[dict] = None


# Create router
router = APIRouter(prefix="", tags=["tasks"])


async def verify_user_id_match(
    current_user_id: str = Depends(get_current_user_id),
    url_user_id: str = ""
) -> str:
    """
    Verify that the JWT user_id matches the URL user_id.

    Args:
        current_user_id: User ID from JWT token
        url_user_id: User ID from URL path

    Returns:
        The verified user_id

    Raises:
        HTTPException: If user IDs don't match
    """
    if current_user_id != url_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID mismatch: token user does not match URL user_id"
        )
    return current_user_id


@router.post(
    "/{user_id}/tasks",
    response_model=TaskRead,
    status_code=status.HTTP_201_CREATED,
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        422: {"model": ErrorResponse, "description": "Validation error"},
    }
)
async def create_task(
    user_id: str,
    task_data: TaskCreate,
    session: AsyncSession = Depends(get_session),
    current_user_id: str = Depends(get_current_user_id)
) -> TaskRead:
    """
    Create a new task for a user.

    - JWT user_id must match the URL user_id
    - Title is required (1-200 characters)
    - Description is optional (max 5000 characters)
    """
    if current_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID mismatch: token user does not match URL user_id"
        )

    task = await TaskService.create_task(
        session=session,
        title=task_data.title,
        description=task_data.description,
        user_id=user_id
    )

    return TaskRead(
        id=task.id,
        title=task.title,
        description=task.description,
        completed=task.completed,
        user_id=task.user_id,
        created_at=task.created_at.isoformat(),
        updated_at=task.updated_at.isoformat()
    )


@router.get(
    "/{user_id}/tasks",
    response_model=List[TaskRead],
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"},
    }
)
async def list_tasks(
    user_id: str,
    session: AsyncSession = Depends(get_session),
    current_user_id: str = Depends(get_current_user_id)
) -> List[TaskRead]:
    """
    List all tasks for a user.

    - JWT user_id must match the URL user_id
    - Returns tasks ordered by creation date (newest first)
    """
    if current_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID mismatch: token user does not match URL user_id"
        )

    tasks = await TaskService.get_tasks_by_user(session, user_id)

    return [
        TaskRead(
            id=task.id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            user_id=task.user_id,
            created_at=task.created_at.isoformat(),
            updated_at=task.updated_at.isoformat()
        )
        for task in tasks
    ]


@router.get(
    "/{user_id}/tasks/{task_id}",
    response_model=TaskRead,
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        404: {"model": ErrorResponse, "description": "Task not found"},
    }
)
async def get_task(
    user_id: str,
    task_id: int,
    session: AsyncSession = Depends(get_session),
    current_user_id: str = Depends(get_current_user_id)
) -> TaskRead:
    """
    Get a single task by ID.

    - JWT user_id must match the URL user_id
    - Returns 404 if task not found or belongs to another user
    """
    if current_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID mismatch: token user does not match URL user_id"
        )

    task = await TaskService.get_task_by_id(session, task_id, user_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return TaskRead(
        id=task.id,
        title=task.title,
        description=task.description,
        completed=task.completed,
        user_id=task.user_id,
        created_at=task.created_at.isoformat(),
        updated_at=task.updated_at.isoformat()
    )


@router.put(
    "/{user_id}/tasks/{task_id}",
    response_model=TaskRead,
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        404: {"model": ErrorResponse, "description": "Task not found"},
        422: {"model": ErrorResponse, "description": "Validation error"},
    }
)
async def update_task(
    user_id: str,
    task_id: int,
    task_data: TaskUpdate,
    session: AsyncSession = Depends(get_session),
    current_user_id: str = Depends(get_current_user_id)
) -> TaskRead:
    """
    Update a task.

    - JWT user_id must match the URL user_id
    - Returns 404 if task not found or belongs to another user
    - All fields are optional; only provided fields are updated
    """
    if current_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID mismatch: token user does not match URL user_id"
        )

    task = await TaskService.update_task(
        session=session,
        task_id=task_id,
        user_id=user_id,
        title=task_data.title,
        description=task_data.description,
        completed=task_data.completed
    )

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return TaskRead(
        id=task.id,
        title=task.title,
        description=task.description,
        completed=task.completed,
        user_id=task.user_id,
        created_at=task.created_at.isoformat(),
        updated_at=task.updated_at.isoformat()
    )


@router.delete(
    "/{user_id}/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        404: {"model": ErrorResponse, "description": "Task not found"},
    }
)
async def delete_task(
    user_id: str,
    task_id: int,
    session: AsyncSession = Depends(get_session),
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Delete a task.

    - JWT user_id must match the URL user_id
    - Returns 404 if task not found or belongs to another user
    - Returns 204 No Content on successful deletion
    """
    if current_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID mismatch: token user does not match URL user_id"
        )

    deleted = await TaskService.delete_task(session, task_id, user_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )


@router.patch(
    "/{user_id}/tasks/{task_id}/complete",
    response_model=TaskRead,
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        404: {"model": ErrorResponse, "description": "Task not found"},
    }
)
async def toggle_completion(
    user_id: str,
    task_id: int,
    session: AsyncSession = Depends(get_session),
    current_user_id: str = Depends(get_current_user_id)
) -> TaskRead:
    """
    Toggle task completion status.

    - JWT user_id must match the URL user_id
    - Returns 404 if task not found or belongs to another user
    - Completion status is toggled (true -> false, false -> true)
    """
    if current_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID mismatch: token user does not match URL user_id"
        )

    task = await TaskService.toggle_completion(session, task_id, user_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return TaskRead(
        id=task.id,
        title=task.title,
        description=task.description,
        completed=task.completed,
        user_id=task.user_id,
        created_at=task.created_at.isoformat(),
        updated_at=task.updated_at.isoformat()
    )
