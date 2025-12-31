"""Tests for TaskService."""

import pytest
from src.task import Task, TaskService


class TestTaskServiceAdd:
    """Tests for TaskService.add() method."""

    def test_add_task_creates_task_with_correct_attributes(self):
        """Verify task creation with title, description, and default status."""
        service = TaskService()
        task = service.add("Test task", "Description")
        assert task.id == 1
        assert task.title == "Test task"
        assert task.description == "Description"
        assert task.completed is False

    def test_add_task_assigns_sequential_ids(self):
        """Verify each task gets a unique sequential ID."""
        service = TaskService()
        task1 = service.add("Task 1")
        task2 = service.add("Task 2")
        task3 = service.add("Task 3")
        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3

    def test_add_empty_title_raises_value_error(self):
        """Verify empty title raises ValueError."""
        service = TaskService()
        with pytest.raises(ValueError) as exc_info:
            service.add("")
        assert "Title cannot be empty" in str(exc_info.value)

    def test_add_whitespace_only_title_raises_value_error(self):
        """Verify whitespace-only title raises ValueError."""
        service = TaskService()
        with pytest.raises(ValueError) as exc_info:
            service.add("   ")
        assert "Title cannot be empty" in str(exc_info.value)

    def test_add_task_with_empty_description(self):
        """Verify task can be created with empty description."""
        service = TaskService()
        task = service.add("Task title")
        assert task.description == ""


class TestTaskServiceList:
    """Tests for TaskService.list() method."""

    def test_list_empty_returns_empty_list(self):
        """Verify empty task list returns empty list."""
        service = TaskService()
        assert service.list() == []

    def test_list_with_tasks_returns_all_tasks(self):
        """Verify list returns all added tasks."""
        service = TaskService()
        service.add("Task 1")
        service.add("Task 2")
        service.add("Task 3")
        tasks = service.list()
        assert len(tasks) == 3

    def test_list_returns_copy_not_reference(self):
        """Verify list() returns a copy, not internal state."""
        service = TaskService()
        service.add("Task 1")
        tasks = service.list()
        tasks.append("fake")  # Should not affect internal state
        assert len(service.list()) == 1


class TestTaskServiceGet:
    """Tests for TaskService.get() method."""

    def test_get_existing_task(self):
        """Verify retrieving an existing task by ID."""
        service = TaskService()
        task = service.add("Test task")
        found = service.get(task.id)
        assert found is task

    def test_get_nonexistent_returns_none(self):
        """Verify non-existent ID returns None."""
        service = TaskService()
        assert service.get(999) is None

    def test_get_after_deletion_returns_none(self):
        """Verify deleted task cannot be retrieved."""
        service = TaskService()
        task = service.add("Test task")
        service.delete(task.id)
        assert service.get(task.id) is None


class TestTaskServiceUpdate:
    """Tests for TaskService.update() method."""

    def test_update_title(self):
        """Verify updating task title."""
        service = TaskService()
        task = service.add("Original")
        service.update(task.id, title="Updated")
        assert task.title == "Updated"

    def test_update_description(self):
        """Verify updating task description."""
        service = TaskService()
        task = service.add("Task", "Original description")
        service.update(task.id, description="Updated description")
        assert task.description == "Updated description"

    def test_update_both_title_and_description(self):
        """Verify updating both title and description."""
        service = TaskService()
        task = service.add("Original", "Original description")
        service.update(task.id, title="New title", description="New description")
        assert task.title == "New title"
        assert task.description == "New description"

    def test_update_with_none_preserves_existing(self):
        """Verify None values don't change existing values."""
        service = TaskService()
        task = service.add("Original", "Description")
        service.update(task.id, title=None, description=None)
        assert task.title == "Original"
        assert task.description == "Description"

    def test_update_empty_title_raises_value_error(self):
        """Verify empty title raises ValueError."""
        service = TaskService()
        task = service.add("Task")
        with pytest.raises(ValueError) as exc_info:
            service.update(task.id, title="")
        assert "Title cannot be empty" in str(exc_info.value)

    def test_update_nonexistent_raises_key_error(self):
        """Verify updating non-existent task raises KeyError."""
        service = TaskService()
        with pytest.raises(KeyError) as exc_info:
            service.update(999, title="New")
        assert "Task with ID 999 not found" in str(exc_info.value)


class TestTaskServiceDelete:
    """Tests for TaskService.delete() method."""

    def test_delete_removes_task(self):
        """Verify task is removed from collection."""
        service = TaskService()
        task = service.add("To delete")
        service.delete(task.id)
        assert service.list() == []

    def test_delete_preserves_remaining_tasks(self):
        """Verify other tasks are unaffected by deletion."""
        service = TaskService()
        task1 = service.add("Task 1")
        task2 = service.add("Task 2")
        task3 = service.add("Task 3")
        service.delete(task2.id)
        remaining = service.list()
        assert len(remaining) == 2
        assert task1 in remaining
        assert task3 in remaining

    def test_delete_nonexistent_raises_key_error(self):
        """Verify deleting non-existent task raises KeyError."""
        service = TaskService()
        with pytest.raises(KeyError) as exc_info:
            service.delete(999)
        assert "Task with ID 999 not found" in str(exc_info.value)


class TestTaskServiceToggle:
    """Tests for TaskService.toggle() method."""

    def test_toggle_incomplete_to_complete(self):
        """Verify toggling incomplete task to complete."""
        service = TaskService()
        task = service.add("Task")
        assert task.completed is False
        service.toggle(task.id)
        assert task.completed is True

    def test_toggle_complete_to_incomplete(self):
        """Verify toggling complete task to incomplete."""
        service = TaskService()
        task = service.add("Task")
        service.toggle(task.id)
        assert task.completed is True
        service.toggle(task.id)
        assert task.completed is False

    def test_toggle_nonexistent_raises_key_error(self):
        """Verify toggling non-existent task raises KeyError."""
        service = TaskService()
        with pytest.raises(KeyError) as exc_info:
            service.toggle(999)
        assert "Task with ID 999 not found" in str(exc_info.value)
