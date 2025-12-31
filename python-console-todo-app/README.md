# Python Console Todo App

A command-line Todo application written in Python that runs entirely in the terminal and stores all tasks in memory only.

## Prerequisites

- Python 3.13 or higher
- UV package manager (recommended) or pip

## Installation

### Using UV (Recommended)

```bash
# Create virtual environment
uv venv

# Install dependencies
uv pip install pytest pytest-cov
```

### Using pip

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install pytest pytest-cov
```

## Running the Application

```bash
# Activate virtual environment first (if not already activated)
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux

# Run the application
python src/main.py
```

## Project Structure

```
python-console-todo-app/
├── src/
│   ├── __init__.py      # Makes src a Python package
│   ├── main.py          # Application entry point
│   ├── task.py          # Task dataclass and TaskService
│   └── ui.py            # Console UI and user interaction
├── tests/
│   ├── __init__.py      # Makes tests a Python package
│   └── test_task.py     # Task model tests (23 tests)
├── .venv/               # Virtual environment
├── .python-version      # Python version specification
├── pyproject.toml       # Project configuration
└── README.md            # This file
```

## First Run

1. Run `python src/main.py`
2. You'll see the main menu:
   ```
         Todo Application
     1. Add Task
     2. View Tasks
     3. Update Task
     4. Delete Task
     5. Mark Task Complete
     6. Mark Task Incomplete
     7. Exit

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

# Verify coverage (>90% required)
pytest --cov=src --cov-report=term-missing tests/
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

## Features

- Add tasks with title and optional description
- View all tasks in a formatted table
- Update task title and/or description
- Delete tasks by ID
- Mark tasks as complete or incomplete
- Clear error messages for invalid inputs
- ANSI color-coded output (blue headers, green success, red errors)
- 100% test coverage on core task model

## Architecture

- **Task dataclass**: Simple data model with id, title, description, completed
- **TaskService**: In-memory CRUD operations (add, list, get, update, delete, toggle)
- **UI module**: Console interaction functions (menu, prompts, display)
- **Main loop**: Menu-driven application flow
