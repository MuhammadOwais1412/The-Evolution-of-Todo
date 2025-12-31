# Quickstart: Python Console Todo App

**Feature**: 1-python-todo-app
**Date**: 2025-12-28

## Prerequisites

- Python 3.13 or higher installed
- Terminal/console access

## Installation

No installation required. The application is a standalone Python script.

## Running the Application

```bash
python src/main.py
```

## Project Structure

```
src/
  main.py           # Application entry point
  task.py           # Task dataclass and operations
  ui.py             # Console UI and user interaction
tests/
  test_task.py      # Task model tests
  test_ui.py        # UI tests
  conftest.py       # Test fixtures
```

## First Run

1. Run `python src/main.py`
2. You'll see the main menu:
   ```
   +----------------------------------+
   |       Todo Application           |
   +----------------------------------+
   | 1. Add Task                      |
   | 2. View Tasks                    |
   | 3. Update Task                   |
   | 4. Delete Task                   |
   | 5. Mark Task Complete            |
   | 6. Mark Task Incomplete          |
   | 7. Exit                          |
   +----------------------------------+
   Enter your choice:
   ```
3. Select option `1` to add your first task
4. Enter a title when prompted
5. Enter an optional description
6. Task is created and you return to the menu

## Development

```bash
# Run tests
pytest tests/

# Run with coverage
pytest --cov=src tests/
```

## Key Commands

| Action | Menu Option |
|--------|-------------|
| Add task | 1 |
| List tasks | 2 |
| Edit task | 3 |
| Remove task | 4 |
| Mark done | 5 |
| Mark undone | 6 |
| Exit | 7 |
