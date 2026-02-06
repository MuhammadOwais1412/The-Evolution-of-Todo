"""
MCP task operations for todo management
"""
from typing import Optional
from sqlmodel import select
from sqlalchemy.exc import SQLAlchemyError
from ...models.task import Task
from ..schemas.task_schemas import (
    AddTaskRequest,
    AddTaskResponse,
    ErrorResponse,
    TaskSchema
)
from .auth_validation import validate_user_from_token, verify_user_owns_task, validate_user_id
from ..db import async_session_factory
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


async def add_task(request: AddTaskRequest) -> AddTaskResponse:
    """
    Add a new task to the system

    Args:
        request: AddTaskRequest containing user_id, title, description, and priority

    Returns:
        AddTaskResponse with the created task details
    """
    try:
        # Validate user_id format
        if not validate_user_id(request.user_id):
            return ErrorResponse(
                error_code="INVALID_USER_ID",
                message="Invalid user ID format"
            )

        # Validate title length
        if not request.title or len(request.title.strip()) == 0 or len(request.title) > 200:
            return ErrorResponse(
                error_code="INVALID_TITLE",
                message="Title is required and must be between 1 and 200 characters"
            )

        # Create the new task
        new_task = Task(
            title=request.title.strip(),
            description=request.description,
            completed=False,
            user_id=request.user_id,
            priority=request.priority
        )

        # Save to database
        async with async_session_factory() as session:
            session.add(new_task)
            await session.commit()
            await session.refresh(new_task)

        # Return success response
        return AddTaskResponse(
            task=TaskSchema(
                id=new_task.id,
                user_id=new_task.user_id,
                title=new_task.title,
                description=new_task.description,
                completed=new_task.completed,
                created_at=new_task.created_at,
                updated_at=new_task.updated_at,
                priority=new_task.priority
            ),
            message="Task created successfully"
        )

    except SQLAlchemyError as e:
        logger.error(f"Database error in add_task: {str(e)}")
        return ErrorResponse(
            error_code="DATABASE_ERROR",
            message="Database error occurred while creating task"
        )
    except Exception as e:
        logger.error(f"Unexpected error in add_task: {str(e)}")
        return ErrorResponse(
            error_code="UNEXPECTED_ERROR",
            message=f"An unexpected error occurred: {str(e)}"
        )


async def list_tasks(user_id: str, status: Optional[str] = None) -> dict:
    """
    List tasks for a specific user

    Args:
        user_id: The ID of the user whose tasks to list
        status: Optional status filter ("all", "pending", "completed")

    Returns:
        Dictionary containing the list of tasks
    """
    try:
        # Validate user_id format
        if not validate_user_id(user_id):
            return ErrorResponse(
                error_code="INVALID_USER_ID",
                message="Invalid user ID format"
            )

        # Build query based on status filter
        query = select(Task).where(Task.user_id == user_id)

        if status and status.lower() != "all":
            if status.lower() == "pending":
                query = query.where(Task.completed == False)
            elif status.lower() == "completed":
                query = query.where(Task.completed == True)

        # Execute query
        async with async_session_factory() as session:
            result = await session.execute(query)
            tasks = result.scalars().all()

        # Convert to schema format
        task_schemas = [
            TaskSchema(
                id=task.id,
                user_id=task.user_id,
                title=task.title,
                description=task.description,
                completed=task.completed,
                created_at=task.created_at,
                updated_at=task.updated_at,
                priority=task.priority
            ) for task in tasks
        ]

        return {
            "status": "success",
            "tasks": task_schemas,
            "message": f"Retrieved {len(task_schemas)} tasks"
        }

    except SQLAlchemyError as e:
        logger.error(f"Database error in list_tasks: {str(e)}")
        return ErrorResponse(
            error_code="DATABASE_ERROR",
            message="Database error occurred while retrieving tasks"
        )
    except Exception as e:
        logger.error(f"Unexpected error in list_tasks: {str(e)}")
        return ErrorResponse(
            error_code="UNEXPECTED_ERROR",
            message=f"An unexpected error occurred: {str(e)}"
        )


async def update_task(user_id: str, task_id: int, title: Optional[str] = None,
                     description: Optional[str] = None, priority=None,
                     completed: Optional[bool] = None) -> dict:
    """
    Update an existing task

    Args:
        user_id: The ID of the user who owns the task
        task_id: The ID of the task to update
        title: New title (optional)
        description: New description (optional)
        priority: New priority (optional)
        completed: New completion status (optional)

    Returns:
        Dictionary with updated task or error
    """
    try:
        # Validate user_id format
        if not validate_user_id(user_id):
            return ErrorResponse(
                error_code="INVALID_USER_ID",
                message="Invalid user ID format"
            )

        # Verify that the user owns this task
        if not await verify_user_owns_task(user_id, task_id):
            return ErrorResponse(
                error_code="TASK_NOT_FOUND_OR_UNAUTHORIZED",
                message="Task not found or user not authorized to update it"
            )

        # Query for the existing task
        async with async_session_factory() as session:
            # Get the task
            result = await session.execute(select(Task).where(Task.id == task_id))
            task = result.scalar_one_or_none()

            if not task:
                return ErrorResponse(
                    error_code="TASK_NOT_FOUND",
                    message="Task not found"
                )

            # Update the task fields if provided
            if title is not None:
                if len(title.strip()) == 0 or len(title) > 200:
                    return ErrorResponse(
                        error_code="INVALID_TITLE",
                        message="Title must be between 1 and 200 characters"
                    )
                task.title = title.strip()

            if description is not None:
                task.description = description

            if priority is not None:
                task.priority = priority

            if completed is not None:
                task.completed = completed

            # Update the updated_at timestamp
            task.updated_at = datetime.utcnow()

            # Commit changes
            await session.commit()
            await session.refresh(task)

        # Return success response
        return {
            "status": "success",
            "task": TaskSchema(
                id=task.id,
                user_id=task.user_id,
                title=task.title,
                description=task.description,
                completed=task.completed,
                created_at=task.created_at,
                updated_at=task.updated_at,
                priority=task.priority
            ),
            "message": "Task updated successfully"
        }

    except SQLAlchemyError as e:
        logger.error(f"Database error in update_task: {str(e)}")
        return ErrorResponse(
            error_code="DATABASE_ERROR",
            message="Database error occurred while updating task"
        )
    except Exception as e:
        logger.error(f"Unexpected error in update_task: {str(e)}")
        return ErrorResponse(
            error_code="UNEXPECTED_ERROR",
            message=f"An unexpected error occurred: {str(e)}"
        )


async def complete_task(user_id: str, task_id: int, completed: bool) -> dict:
    """
    Mark a task as complete or incomplete

    Args:
        user_id: The ID of the user who owns the task
        task_id: The ID of the task to update
        completed: Whether the task should be marked as complete

    Returns:
        Dictionary with updated task or error
    """
    try:
        # Validate user_id format
        if not validate_user_id(user_id):
            return ErrorResponse(
                error_code="INVALID_USER_ID",
                message="Invalid user ID format"
            )

        # Use update_task function to update the completion status
        return await update_task(user_id, task_id, completed=completed)

    except Exception as e:
        logger.error(f"Unexpected error in complete_task: {str(e)}")
        return ErrorResponse(
            error_code="UNEXPECTED_ERROR",
            message=f"An unexpected error occurred: {str(e)}"
        )


async def delete_task(user_id: str, task_id: int) -> dict:
    """
    Delete a task

    Args:
        user_id: The ID of the user who owns the task
        task_id: The ID of the task to delete

    Returns:
        Dictionary with success message or error
    """
    try:
        # Validate user_id format
        if not validate_user_id(user_id):
            return ErrorResponse(
                error_code="INVALID_USER_ID",
                message="Invalid user ID format"
            )

        # Verify that the user owns this task
        if not await verify_user_owns_task(user_id, task_id):
            return ErrorResponse(
                error_code="TASK_NOT_FOUND_OR_UNAUTHORIZED",
                message="Task not found or user not authorized to delete it"
            )

        # Delete the task
        async with async_session_factory() as session:
            # Get the task first to return its ID in the response
            result = await session.execute(select(Task).where(Task.id == task_id))
            task = result.scalar_one_or_none()

            if not task:
                return ErrorResponse(
                    error_code="TASK_NOT_FOUND",
                    message="Task not found"
                )

            # Delete the task
            await session.delete(task)
            await session.commit()

        # Return success response
        return {
            "status": "success",
            "task_id": task_id,
            "message": "Task deleted successfully"
        }

    except SQLAlchemyError as e:
        logger.error(f"Database error in delete_task: {str(e)}")
        return ErrorResponse(
            error_code="DATABASE_ERROR",
            message="Database error occurred while deleting task"
        )
    except Exception as e:
        logger.error(f"Unexpected error in delete_task: {str(e)}")
        return ErrorResponse(
            error_code="UNEXPECTED_ERROR",
            message=f"An unexpected error occurred: {str(e)}"
        )