# Data Model: Python Console Todo App

**Feature**: 1-python-todo-app
**Date**: 2025-12-28

## Entities

### Task

Represents a single to-do item managed by the application.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | `int` | Positive, unique, sequential | Unique identifier assigned at creation |
| `title` | `str` | Non-empty, required | Brief task description |
| `description` | `str` | Optional, may be empty | Detailed task information |
| `completed` | `bool` | Required, default: `False` | Completion status flag |

### TaskCollection

Container for all tasks in the system.

| Field | Type | Description |
|-------|------|-------------|
| `tasks` | `List[Task]` | Ordered list of all tasks |
| `next_id` | `int` | Counter for next task ID assignment |

## Validation Rules

### Task Validation

1. **Title**: Must be non-empty string (after stripping whitespace)
2. **Description**: Optional, can be empty string
3. **ID**: Must exist in collection when performing operations

### Collection Operations

1. **Add Task**: Assigns `next_id`, increments counter, appends to list
2. **Delete Task**: Removes task by ID from list (shifts remaining elements)
3. **Update Task**: Finds task by ID, updates specified fields
4. **Toggle Status**: Finds task by ID, flips `completed` boolean

## State Transitions

```
Task Lifecycle:

Created (incomplete)  <--->  Marked Complete
        |
        v
    Deleted (removed from collection)
```

## Persistence Model

- **Storage**: In-memory only (Python `list`)
- **Lifetime**: Application session only
- **No persistence**: Data discarded on exit
