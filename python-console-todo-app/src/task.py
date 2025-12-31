"""Task management domain model and service."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Task:
    """Represents a single to-do item."""
    id: int
    title: str
    description: str
    completed: bool = False


class TaskService:
    """Service for managing tasks in memory."""

    def __init__(self) -> None:
        self._tasks: list[Task] = []
        self._next_id: int = 1

    def add(self, title: str, description: str = "") -> Task:
        """Add a new task with the given title and description."""
        if not title or not title.strip():
            raise ValueError("Title cannot be empty")
        task = Task(
            id=self._next_id,
            title=title.strip(),
            description=description,
            completed=False
        )
        self._tasks.append(task)
        self._next_id += 1
        return task

    def list(self) -> list[Task]:
        """Return a copy of all tasks."""
        return list(self._tasks)

    def get(self, task_id: int) -> Optional[Task]:
        """Get a task by its ID, or None if not found."""
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    def update(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None
    ) -> Task:
        """Update a task's title and/or description."""
        task = self.get(task_id)
        if task is None:
            raise KeyError(f"Task with ID {task_id} not found")
        if title is not None:
            if not title.strip():
                raise ValueError("Title cannot be empty")
            task.title = title.strip()
        if description is not None:
            task.description = description
        return task

    def delete(self, task_id: int) -> None:
        """Delete a task by its ID."""
        original_len = len(self._tasks)
        self._tasks = [t for t in self._tasks if t.id != task_id]
        if len(self._tasks) == original_len:
            raise KeyError(f"Task with ID {task_id} not found")

    def toggle(self, task_id: int) -> Task:
        """Toggle a task's completion status."""
        task = self.get(task_id)
        if task is None:
            raise KeyError(f"Task with ID {task_id} not found")
        task.completed = not task.completed
        return task
