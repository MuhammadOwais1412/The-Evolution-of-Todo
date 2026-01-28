# API Contract: Phase II - Full-Stack Todo Application

**Created**: 2026-01-10
**Version**: 1.0.0

## Overview
REST API contract for communication between frontend and backend in the full-stack todo application. All endpoints require JWT authentication via Authorization header.

## Authentication
All protected endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer <jwt-token>
```

## Base URL
```
https://api.yourdomain.com/api/v1
```

## Endpoints

### Task Management

#### GET /tasks
Retrieve all tasks for the authenticated user

**Headers**:
- Authorization: Bearer <jwt-token>

**Response**:
- 200: Array of task objects
  ```json
  [
    {
      "id": 1,
      "title": "Sample task",
      "description": "Sample description",
      "completed": false,
      "userId": "user-uuid",
      "createdAt": "2026-01-10T10:00:00Z",
      "updatedAt": "2026-01-10T10:00:00Z"
    }
  ]
  ```
- 401: Unauthorized if JWT is invalid/expired
- 500: Internal server error

#### POST /tasks
Create a new task for the authenticated user

**Headers**:
- Authorization: Bearer <jwt-token>
- Content-Type: application/json

**Body**:
```json
{
  "title": "Task title",
  "description": "Task description"
}
```

**Response**:
- 201: Created task object
  ```json
  {
    "id": 1,
    "title": "Task title",
    "description": "Task description",
    "completed": false,
    "userId": "user-uuid",
    "createdAt": "2026-01-10T10:00:00Z",
    "updatedAt": "2026-01-10T10:00:00Z"
  }
  ```
- 400: Bad request if title is missing or invalid
- 401: Unauthorized if JWT is invalid/expired
- 500: Internal server error

#### PUT /tasks/{id}
Update an existing task

**Path Parameters**:
- id: Task ID (integer)

**Headers**:
- Authorization: Bearer <jwt-token>
- Content-Type: application/json

**Body**:
```json
{
  "title": "Updated task title",
  "description": "Updated task description",
  "completed": true
}
```

**Response**:
- 200: Updated task object
- 400: Bad request if data is invalid
- 401: Unauthorized if JWT is invalid/expired
- 404: Task not found
- 500: Internal server error

#### PATCH /tasks/{id}/toggle
Toggle the completion status of a task

**Path Parameters**:
- id: Task ID (integer)

**Headers**:
- Authorization: Bearer <jwt-token>

**Response**:
- 200: Updated task object with toggled completion status
- 401: Unauthorized if JWT is invalid/expired
- 404: Task not found
- 500: Internal server error

#### DELETE /tasks/{id}
Delete a task

**Path Parameters**:
- id: Task ID (integer)

**Headers**:
- Authorization: Bearer <jwt-token>

**Response**:
- 204: No content (task deleted successfully)
- 401: Unauthorized if JWT is invalid/expired
- 404: Task not found
- 500: Internal server error

## Error Response Format
All error responses follow this format:
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": "Additional error details if applicable"
  }
}
```

## Common Error Codes
- AUTH_001: Invalid or expired JWT token
- TASK_001: Task not found
- VALIDATION_001: Validation error in request data
- SYSTEM_001: Internal server error