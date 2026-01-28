"""Task service for business logic operations."""
from datetime import datetime
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.task import Task


class TaskService:
    """Service class for task CRUD operations."""

    @staticmethod
    async def create_task(
        session: AsyncSession,
        title: str,
        description: Optional[str],
        user_id: str
    ) -> Task:
        """
        Create a new task for a user.

        Args:
            session: Database session
            title: Task title (1-200 characters)
            description: Optional task description
            user_id: Owner user ID from JWT

        Returns:
            Created Task instance
        """
        task = Task(
            title=title,
            description=description,
            user_id=user_id
        )
        session.add(task)
        await session.commit()
        await session.refresh(task)
        return task

    @staticmethod
    async def get_tasks_by_user(
        session: AsyncSession,
        user_id: str
    ) -> List[Task]:
        """
        Retrieve all tasks for a user, ordered by creation date.

        Args:
            session: Database session
            user_id: Owner user ID from JWT

        Returns:
            List of Task instances
        """
        stmt = (
            select(Task)
            .where(Task.user_id == user_id)
            .order_by(Task.created_at.desc())
        )
        result = await session.execute(stmt)
        return list(result.scalars().all())

    @staticmethod
    async def get_task_by_id(
        session: AsyncSession,
        task_id: int,
        user_id: str
    ) -> Optional[Task]:
        """
        Retrieve a single task by ID with user isolation.

        Args:
            session: Database session
            task_id: Task ID to retrieve
            user_id: Owner user ID from JWT

        Returns:
            Task if found and owned by user, None otherwise
        """
        stmt = (
            select(Task)
            .where(Task.id == task_id, Task.user_id == user_id)
        )
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def update_task(
        session: AsyncSession,
        task_id: int,
        user_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        completed: Optional[bool] = None
    ) -> Optional[Task]:
        """
        Update a task with user isolation.

        Args:
            session: Database session
            task_id: Task ID to update
            user_id: Owner user ID from JWT
            title: New title (optional)
            description: New description (optional)
            completed: New completion status (optional)

        Returns:
            Updated Task if found, None otherwise
        """
        task = await TaskService.get_task_by_id(session, task_id, user_id)
        if task is None:
            return None

        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if completed is not None:
            task.completed = completed

        task.updated_at = datetime.utcnow()
        await session.commit()
        await session.refresh(task)
        return task

    @staticmethod
    async def delete_task(
        session: AsyncSession,
        task_id: int,
        user_id: str
    ) -> bool:
        """
        Delete a task with user isolation.
<<<<<<< HEAD
        This operation is idempotent - deleting an already deleted task returns True.
=======
>>>>>>> 003-frontend-better-auth

        Args:
            session: Database session
            task_id: Task ID to delete
            user_id: Owner user ID from JWT

        Returns:
<<<<<<< HEAD
            True if deletion was successful or task was already deleted, False if task doesn't belong to user
        """
        task = await TaskService.get_task_by_id(session, task_id, user_id)
        if task is None:
            # Task doesn't exist or doesn't belong to user
            # For idempotency, if it doesn't exist, we consider it as successfully "deleted"
            # But we need to distinguish between "already deleted" and "doesn't belong to user"
            # Check if task exists but belongs to different user
            stmt = select(Task).where(Task.id == task_id)
            result = await session.execute(stmt)
            existing_task = result.scalar_one_or_none()
            if existing_task is not None and existing_task.user_id != user_id:
                # Task exists but belongs to another user - return False to indicate unauthorized
                return False
            # Task doesn't exist at all or was already deleted - return True for idempotency
            return True
=======
            True if deleted, False if not found
        """
        task = await TaskService.get_task_by_id(session, task_id, user_id)
        if task is None:
            return False
>>>>>>> 003-frontend-better-auth

        await session.delete(task)
        await session.commit()
        return True

    @staticmethod
    async def toggle_completion(
        session: AsyncSession,
        task_id: int,
        user_id: str
    ) -> Optional[Task]:
        """
        Toggle task completion status.

        Args:
            session: Database session
            task_id: Task ID to toggle
            user_id: Owner user ID from JWT

        Returns:
            Updated Task if found, None otherwise
        """
        task = await TaskService.get_task_by_id(session, task_id, user_id)
        if task is None:
            return None

        task.completed = not task.completed
        task.updated_at = datetime.utcnow()
        await session.commit()
        await session.refresh(task)
        return task
