# Implementation Plan: Python Console Todo App

**Feature Branch**: `1-python-todo-app`
**Created**: 2025-12-28
**Status**: Ready for Implementation
**Feature Spec**: `specs/1-python-todo-app/spec.md`
**Data Model**: `specs/1-python-todo-app/data-model.md`
**Contracts**: `specs/1-python-todo-app/contracts/operations.yaml`
**Research**: `specs/1-python-todo-app/research.md`

---

## Constitution Check

| Principle | Compliance | Notes |
|-----------|------------|-------|
| In-Memory Only | ✅ Compliant | No file storage, databases, or persistence mechanisms |
| Clean Architecture | ✅ Compliant | Single responsibility, clear separation, explicit data flow |
| No Global Mutable State | ✅ Compliant | State owned by TaskService, no global variables |
| Spec-Driven Development | ✅ Compliant | Following spec-first, plan-second, implement-third order |
| Input Validation & Error Handling | ✅ Compliant | All inputs validated, errors handled gracefully |
| Smallest Viable Change | ✅ Compliant | Minimal modules, no speculative features |

---

## Technical Context

- **Language**: Python 3.13+
- **Standard Library Only**: No external dependencies
- **Architecture**: 3 modules (task.py, ui.py, main.py)
- **State Management**: TaskService class holding Task instances in a list
- **Colors**: ANSI escape codes via sys.stdout

---

## Phased Implementation Plan

### Phase 1: Foundation

**Step 1.1: Create Project Structure**

| Item | Details |
|------|---------|
| **Description** | Create directory structure and initialize project |
| **Files** | `src/__init__.py`, `tests/__init__.py`, `pyproject.toml` |
| **Dependencies** | None |
| **Verification** | Directories exist, files importable |

**Step 1.2: Implement Task Data Model**

| Item | Details |
|------|---------|
| **Description** | Create Task dataclass and TaskService class |
| **Files** | `src/task.py` |
| **Classes** | `Task`, `TaskService` |
| **Methods** | `add()`, `list()`, `get()`, `update()`, `delete()`, `toggle()` |
| **Verification** | Unit tests pass for all TaskService methods |

---

### Phase 2: User Interface

**Step 2.1: Implement Console UI Layer**

| Item | Details |
|------|---------|
| **Description** | Create UI module with menu and input handling |
| **Files** | `src/ui.py` |
| **Functions** | `show_menu()`, `get_choice()`, `show_tasks()`, `prompt_task_data()`, `show_message()` |
| **ANSI Colors** | Blue for headers, green for success, red for errors |
| **Verification** | Menu displays correctly, inputs read properly |

**Step 2.2: Implement Main Application Loop**

| Item | Details |
|------|---------|
| **Description** | Create main entry point with menu loop |
| **Files** | `src/main.py` |
| **Logic** | Import TaskService, display menu, route to operations |
| **Verification** | Application runs, menu loops until exit |

---

### Phase 3: Testing & Verification

**Step 3.1: Write Unit Tests**

| Item | Details |
|------|---------|
| **Files** | `tests/test_task.py`, `tests/test_ui.py`, `tests/conftest.py` |
| **Coverage** | All TaskService methods, error cases, UI flows |
| **Verification** | `pytest --cov` shows >90% coverage |

**Step 3.2: Integration Testing**

| Item | Details |
|------|---------|
| **Description** | Verify complete user workflows |
| **Scenarios** | Add-View-Delete flow, Update flow, Toggle flow, Error handling |
| **Verification** | All acceptance scenarios from spec pass |

---

## Implementation Steps (Ordered)

### Step 1: Initialize Project

```bash
# Create project structure
mkdir -p src tests
touch src/__init__.py tests/__init__.py

# Create pyproject.toml
cat > pyproject.toml << 'EOF'
[project]
name = "python-console-todo-app"
version = "0.1.0"
requires-python = ">=3.13"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
EOF
```

**Deliverable**: Project structure ready for development

---

### Step 2: Implement Task Model (src/task.py)

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class Task:
    id: int
    title: str
    description: str
    completed: bool = False

class TaskService:
    def __init__(self) -> None:
        self._tasks: list[Task] = []
        self._next_id: int = 1

    def add(self, title: str, description: str = "") -> Task:
        # Validate title not empty
        if not title or not title.strip():
            raise ValueError("Title cannot be empty")
        task = Task(id=self._next_id, title=title.strip(),
                    description=description, completed=False)
        self._tasks.append(task)
        self._next_id += 1
        return task

    def list(self) -> list[Task]:
        return list(self._tasks)

    def get(self, task_id: int) -> Optional[Task]:
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    def update(self, task_id: int, title: Optional[str] = None,
               description: Optional[str] = None) -> Task:
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
        original_len = len(self._tasks)
        self._tasks = [t for t in self._tasks if t.id != task_id]
        if len(self._tasks) == original_len:
            raise KeyError(f"Task with ID {task_id} not found")

    def toggle(self, task_id: int) -> Task:
        task = self.get(task_id)
        if task is None:
            raise KeyError(f"Task with ID {task_id} not found")
        task.completed = not task.completed
        return task
```

**Deliverable**: Task dataclass and TaskService class with all CRUD operations

---

### Step 3: Implement UI Layer (src/ui.py)

```python
import sys

# ANSI color codes
BLUE = "\033[94m"
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"

def header(text: str) -> None:
    print(f"{BLUE}{BOLD}{text}{RESET}")

def success(text: str) -> None:
    print(f"{GREEN}{text}{RESET}")

def error(text: str) -> None:
    print(f"{RED}{text}{RESET}")

def show_menu() -> None:
    print()
    header("       Todo Application       ")
    print("  1. Add Task")
    print("  2. View Tasks")
    print("  3. Update Task")
    print("  4. Delete Task")
    print("  5. Mark Task Complete")
    print("  6. Mark Task Incomplete")
    print("  7. Exit")
    print()

def get_choice() -> int:
    while True:
        try:
            choice = int(input("Enter your choice: "))
            if 1 <= choice <= 7:
                return choice
            error("Invalid choice. Please enter a number between 1 and 7.")
        except ValueError:
            error("Invalid choice. Please enter a number between 1 and 7.")

def prompt_task_data() -> tuple[str, str]:
    while True:
        title = input("Enter task title: ").strip()
        if title:
            break
        error("Title cannot be empty. Please enter a task title.")
    description = input("Enter task description (optional): ").strip()
    return title, description

def show_tasks(tasks: list) -> None:
    if not tasks:
        print("No tasks available.")
        return
    print(f"  {'ID':<4} {'Title':<16} {'Description':<18} {'Status':<10}")
    print("  " + "-" * 50)
    for task in tasks:
        status = "Complete" if task.completed else "Incomplete"
        print(f"  {task.id:<4} {task.title[:16]:<16} {task.description[:18]:<18} {status:<10}")

def prompt_task_id() -> int:
    while True:
        try:
            task_id = int(input("Enter task ID: "))
            if task_id > 0:
                return task_id
            error("Invalid ID. Please enter a positive number.")
        except ValueError:
            error("Invalid ID. Please enter a positive number.")

def prompt_update_data() -> tuple[Optional[str], Optional[str]]:
    title = input("Enter new title (leave empty to keep current): ").strip()
    description = input("Enter new description (leave empty to keep current): ").strip()
    return title or None, description or None
```

**Deliverable**: UI module with all display and input functions

---

### Step 4: Implement Main Application (src/main.py)

```python
from task import TaskService
from ui import (show_menu, get_choice, show_tasks, prompt_task_data,
                prompt_task_id, prompt_update_data, success, error)

def main() -> None:
    service = TaskService()

    while True:
        show_menu()
        choice = get_choice()

        if choice == 1:  # Add Task
            title, description = prompt_task_data()
            task = service.add(title, description)
            success(f"Task {task.id} created successfully")

        elif choice == 2:  # View Tasks
            tasks = service.list()
            show_tasks(tasks)

        elif choice == 3:  # Update Task
            task_id = prompt_task_id()
            title, description = prompt_update_data()
            try:
                service.update(task_id, title, description)
                success(f"Task {task_id} updated successfully")
            except KeyError:
                error(f"Task with ID {task_id} not found.")

        elif choice == 4:  # Delete Task
            task_id = prompt_task_id()
            try:
                service.delete(task_id)
                success(f"Task {task_id} deleted successfully")
            except KeyError:
                error(f"Task with ID {task_id} not found.")

        elif choice == 5:  # Mark Complete
            task_id = prompt_task_id()
            try:
                service.toggle(task_id)
                success(f"Task {task_id} marked as complete")
            except KeyError:
                error(f"Task with ID {task_id} not found.")

        elif choice == 6:  # Mark Incomplete
            task_id = prompt_task_id()
            try:
                service.toggle(task_id)
                success(f"Task {task_id} marked as incomplete")
            except KeyError:
                error(f"Task with ID {task_id} not found.")

        elif choice == 7:  # Exit
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()
```

**Deliverable**: Complete application with main loop

---

### Step 5: Write Tests (tests/test_task.py, tests/test_ui.py)

```python
# tests/test_task.py
import pytest
from task import Task, TaskService

def test_add_task():
    service = TaskService()
    task = service.add("Test task", "Description")
    assert task.id == 1
    assert task.title == "Test task"
    assert task.description == "Description"
    assert task.completed is False

def test_add_empty_title_raises():
    service = TaskService()
    with pytest.raises(ValueError):
        service.add("")

def test_list_empty():
    service = TaskService()
    assert service.list() == []

def test_list_with_tasks():
    service = TaskService()
    service.add("Task 1")
    service.add("Task 2")
    assert len(service.list()) == 2

def test_get_task():
    service = TaskService()
    task = service.add("Test task")
    found = service.get(task.id)
    assert found is task

def test_get_nonexistent():
    service = TaskService()
    assert service.get(999) is None

def test_update_task():
    service = TaskService()
    task = service.add("Original")
    service.update(task.id, title="Updated")
    assert task.title == "Updated"

def test_delete_task():
    service = TaskService()
    task = service.add("To delete")
    service.delete(task.id)
    assert service.list() == []

def test_toggle_completion():
    service = TaskService()
    task = service.add("Task")
    assert task.completed is False
    service.toggle(task.id)
    assert task.completed is True
```

**Deliverable**: Comprehensive test suite

---

## Dependency Graph

```
Step 1 (Project Structure)
    |
    v
Step 2 (Task Model) <-- Required by Step 3, 4
    |
    v
Step 3 (UI Layer) <-- Required by Step 4
    |
    v
Step 4 (Main App) <-- Required by Step 5 (integration tests)
    |
    v
Step 5 (Tests)
```

---

## Verification Checkpoints

| Checkpoint | Criteria | Status |
|------------|----------|--------|
| Project compiles | `python -m py_compile src/*.py` passes | |
| Task model tests | All 9 tests in test_task.py pass | |
| TaskService correctness | All CRUD operations work correctly | |
| UI functions work | Menu displays, inputs read correctly | |
| Full workflow | Add 3 tasks, update 1, delete 1, toggle 1 | |
| No crashes | Invalid inputs handled gracefully | |
| Coverage | >90% code coverage on src/task.py | |

---

## Complexity Tracking

| Aspect | Estimate | Actual | Notes |
|--------|----------|--------|-------|
| Modules | 3 | 3 | task.py, ui.py, main.py |
| Classes | 2 | 2 | Task, TaskService |
| Functions | 15+ | ~15 | All small, single-purpose |
| Lines of code | ~200 | ~200 | Clean, readable |
| Test coverage | >90% | | Unit tests required |

---

## Next Steps

After this plan is approved:

1. Run `/sp.implement` to execute tasks.md generation
2. Implement each step in order
3. Verify at each checkpoint
4. Complete integration testing before marking done
