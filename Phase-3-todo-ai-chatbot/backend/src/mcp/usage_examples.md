# MCP Server Usage Examples

This document provides API usage examples for each MCP tool in the Todo AI Chatbot system.

## Available Tools

### 1. add_task
Create a new task for the authenticated user.

**Parameters:**
- `user_id` (required): The ID of the user creating the task
- `title` (required): The title of the task (1-200 characters)
- `description` (optional): Detailed description of the task
- `priority` (optional): Priority level ("low", "medium", "high")

**Example Request:**
```python
import requests

response = requests.post("http://localhost:8000/mcp/add_task", json={
    "user_id": "user123",
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "priority": "medium"
})
```

**Successful Response:**
```json
{
    "status": "success",
    "task": {
        "id": 1,
        "user_id": "user123",
        "title": "Buy groceries",
        "description": "Milk, eggs, bread",
        "completed": false,
        "created_at": "2023-01-01T00:00:00",
        "updated_at": "2023-01-01T00:00:00",
        "priority": "medium"
    },
    "message": "Task created successfully"
}
```

### 2. list_tasks
Retrieve all tasks for the authenticated user.

**Parameters:**
- `user_id` (required): The ID of the user whose tasks to retrieve
- `status` (optional): Filter by status ("all", "pending", "completed")

**Example Request:**
```python
import requests

response = requests.post("http://localhost:8000/mcp/list_tasks", json={
    "user_id": "user123",
    "status": "pending"
})
```

**Successful Response:**
```json
{
    "status": "success",
    "tasks": [
        {
            "id": 1,
            "user_id": "user123",
            "title": "Buy groceries",
            "description": "Milk, eggs, bread",
            "completed": false,
            "created_at": "2023-01-01T00:00:00",
            "updated_at": "2023-01-01T00:00:00",
            "priority": "medium"
        }
    ],
    "message": "Retrieved 1 tasks"
}
```

### 3. update_task
Update properties of an existing task for the authenticated user.

**Parameters:**
- `user_id` (required): The ID of the user who owns the task
- `task_id` (required): The ID of the task to update
- `title` (optional): New title for the task
- `description` (optional): New description for the task
- `priority` (optional): New priority level ("low", "medium", "high")
- `completed` (optional): New completion status (true/false)

**Example Request:**
```python
import requests

response = requests.post("http://localhost:8000/mcp/update_task", json={
    "user_id": "user123",
    "task_id": 1,
    "title": "Buy groceries and fruits",
    "completed": true
})
```

**Successful Response:**
```json
{
    "status": "success",
    "task": {
        "id": 1,
        "user_id": "user123",
        "title": "Buy groceries and fruits",
        "description": "Milk, eggs, bread",
        "completed": true,
        "created_at": "2023-01-01T00:00:00",
        "updated_at": "2023-01-02T00:00:00",
        "priority": "medium"
    },
    "message": "Task updated successfully"
}
```

### 4. complete_task
Mark a task as complete or incomplete for the authenticated user.

**Parameters:**
- `user_id` (required): The ID of the user who owns the task
- `task_id` (required): The ID of the task to update
- `completed` (required): Whether the task should be marked as complete (true/false)

**Example Request:**
```python
import requests

response = requests.post("http://localhost:8000/mcp/complete_task", json={
    "user_id": "user123",
    "task_id": 1,
    "completed": true
})
```

**Successful Response:**
```json
{
    "status": "success",
    "task": {
        "id": 1,
        "user_id": "user123",
        "title": "Buy groceries and fruits",
        "description": "Milk, eggs, bread",
        "completed": true,
        "created_at": "2023-01-01T00:00:00",
        "updated_at": "2023-01-02T00:00:00",
        "priority": "medium"
    },
    "message": "Task completion status updated successfully"
}
```

### 5. delete_task
Remove a task for the authenticated user.

**Parameters:**
- `user_id` (required): The ID of the user who owns the task
- `task_id` (required): The ID of the task to delete

**Example Request:**
```python
import requests

response = requests.post("http://localhost:8000/mcp/delete_task", json={
    "user_id": "user123",
    "task_id": 1
})
```

**Successful Response:**
```json
{
    "status": "success",
    "task_id": 1,
    "message": "Task deleted successfully"
}
```

## Error Handling

All tools return consistent error responses in the following format:

```json
{
    "status": "error",
    "error_code": "ERROR_CODE",
    "message": "Descriptive error message",
    "details": { /* optional details */ }
}
```

Common error codes:
- `INVALID_USER_ID`: User ID is invalid or missing
- `INVALID_TITLE`: Title is missing or invalid
- `TASK_NOT_FOUND_OR_UNAUTHORIZED`: Task doesn't exist or user not authorized
- `TASK_NOT_FOUND`: Task doesn't exist
- `DATABASE_ERROR`: Database operation failed
- `UNEXPECTED_ERROR`: Unexpected error occurred