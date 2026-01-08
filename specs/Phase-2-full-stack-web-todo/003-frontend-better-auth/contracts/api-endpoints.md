# API Contracts: Frontend → Backend

**Feature**: 003-frontend-better-auth
**Date**: 2026-01-03
**Base URL**: `http://localhost:8000` (configurable via `NEXT_PUBLIC_API_URL`)

## Overview

This document defines the REST API contracts between the Next.js frontend and FastAPI backend. All endpoints require JWT authentication via `Authorization: Bearer <token>` header. Backend enforces user isolation by matching JWT `sub` claim with URL `user_id` parameter.

---

## Authentication

### JWT Token Format

**Header**:
```
Authorization: Bearer <jwt_token>
```

**Token Structure**:
- Algorithm: HS256
- Secret: `BETTER_AUTH_SECRET` (shared with Better Auth)
- Payload:
  ```json
  {
    "sub": "auth0|12345",  // User ID
    "iat": 1735920000,
    "exp": 1736006400
  }
  ```

**Token Management**:
- Issued by Better Auth on signup/login
- Stored in cookie or localStorage (Better Auth configuration)
- Extracted by API client and attached to all requests
- Validated by backend `get_current_user_id` dependency

---

## Base URL Configuration

**Development**:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Production** (example):
```
NEXT_PUBLIC_API_URL=https://api.todo-app.com
```

---

## Endpoints

### Health Check

**Purpose**: Verify backend is running

**Request**:
```
GET /health
```

**Response**:
```json
{
  "status": "healthy"
}
```

**Authentication**: Not required

---

### Create Task

**Purpose**: Create a new task for the authenticated user

**Request**:
```
POST /{user_id}/tasks
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**Path Parameters**:
- `user_id` (string): User ID from Better Auth (must match JWT `sub`)

**Request Body**:
```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}
```

**Rules**:
- `title`: Required, 1-200 characters
- `description`: Optional, max 5000 characters
- `user_id` in URL must match JWT `sub` claim (401 if mismatch)

**Success Response**:
```
201 Created
Content-Type: application/json
```

```json
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "user_id": "auth0|12345",
  "created_at": "2026-01-03T12:00:00Z",
  "updated_at": "2026-01-03T12:00:00Z"
}
```

**Error Responses**:
```
401 Unauthorized
{
  "error": "Unauthorized",
  "message": "User ID mismatch: token user does not match URL user_id",
  "details": null
}
```

```
422 Unprocessable Entity
{
  "error": "Validation error",
  "message": "Title is required",
  "details": {
    "title": "ensure this value has at least 1 characters"
  }
}
```

---

### List Tasks

**Purpose**: Get all tasks for the authenticated user

**Request**:
```
GET /{user_id}/tasks
Authorization: Bearer <jwt_token>
```

**Path Parameters**:
- `user_id` (string): User ID from Better Auth (must match JWT `sub`)

**Rules**:
- Returns tasks ordered by `created_at` (newest first)
- Only returns tasks owned by the authenticated user
- Empty array returned if user has no tasks

**Success Response**:
```
200 OK
Content-Type: application/json
```

```json
[
  {
    "id": 2,
    "title": "Walk the dog",
    "description": null,
    "completed": true,
    "user_id": "auth0|12345",
    "created_at": "2026-01-03T13:00:00Z",
    "updated_at": "2026-01-03T14:00:00Z"
  },
  {
    "id": 1,
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": false,
    "user_id": "auth0|12345",
    "created_at": "2026-01-03T12:00:00Z",
    "updated_at": "2026-01-03T12:00:00Z"
  }
]
```

**Error Responses**:
```
401 Unauthorized
{
  "error": "Unauthorized",
  "message": "User ID mismatch: token user does not match URL user_id",
  "details": null
}
```

---

### Get Task

**Purpose**: Get a single task by ID

**Request**:
```
GET /{user_id}/tasks/{task_id}
Authorization: Bearer <jwt_token>
```

**Path Parameters**:
- `user_id` (string): User ID from Better Auth (must match JWT `sub`)
- `task_id` (integer): Task ID

**Rules**:
- Only returns task if owned by authenticated user
- Returns 404 if task not found or belongs to another user

**Success Response**:
```
200 OK
Content-Type: application/json
```

```json
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "user_id": "auth0|12345",
  "created_at": "2026-01-03T12:00:00Z",
  "updated_at": "2026-01-03T12:00:00Z"
}
```

**Error Responses**:
```
401 Unauthorized
{
  "error": "Unauthorized",
  "message": "User ID mismatch: token user does not match URL user_id",
  "details": null
}
```

```
404 Not Found
{
  "error": "Not found",
  "message": "Task not found",
  "details": null
}
```

---

### Update Task

**Purpose**: Update an existing task

**Request**:
```
PUT /{user_id}/tasks/{task_id}
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**Path Parameters**:
- `user_id` (string): User ID from Better Auth (must match JWT `sub`)
- `task_id` (integer): Task ID

**Request Body** (partial update):
```json
{
  "title": "Updated task title"
}
```

Or:
```json
{
  "description": "Updated description"
}
```

Or:
```json
{
  "completed": true
}
```

**Rules**:
- All fields optional (partial update)
- Only updates fields provided in request body
- `user_id` in URL must match JWT `sub` claim
- Only updates task if owned by authenticated user

**Success Response**:
```
200 OK
Content-Type: application/json
```

```json
{
  "id": 1,
  "title": "Updated task title",
  "description": "Milk, eggs, bread",
  "completed": false,
  "user_id": "auth0|12345",
  "created_at": "2026-01-03T12:00:00Z",
  "updated_at": "2026-01-03T15:00:00Z"
}
```

**Error Responses**:
```
401 Unauthorized
{
  "error": "Unauthorized",
  "message": "User ID mismatch: token user does not match URL user_id",
  "details": null
}
```

```
404 Not Found
{
  "error": "Not found",
  "message": "Task not found",
  "details": null
}
```

```
422 Unprocessable Entity
{
  "error": "Validation error",
  "message": "Title is required",
  "details": {
    "title": "ensure this value has at least 1 characters"
  }
}
```

---

### Delete Task

**Purpose**: Delete a task

**Request**:
```
DELETE /{user_id}/tasks/{task_id}
Authorization: Bearer <jwt_token>
```

**Path Parameters**:
- `user_id` (string): User ID from Better Auth (must match JWT `sub`)
- `task_id` (integer): Task ID

**Rules**:
- Only deletes task if owned by authenticated user
- Returns 204 No Content on successful deletion

**Success Response**:
```
204 No Content
```

**Error Responses**:
```
401 Unauthorized
{
  "error": "Unauthorized",
  "message": "User ID mismatch: token user does not match URL user_id",
  "details": null
}
```

```
404 Not Found
{
  "error": "Not found",
  "message": "Task not found",
  "details": null
}
```

---

### Toggle Task Completion

**Purpose**: Toggle task completion status (true ↔ false)

**Request**:
```
PATCH /{user_id}/tasks/{task_id}/complete
Authorization: Bearer <jwt_token>
```

**Path Parameters**:
- `user_id` (string): User ID from Better Auth (must match JWT `sub`)
- `task_id` (integer): Task ID

**Rules**:
- Only toggles task if owned by authenticated user
- Completion status flips (false → true, true → false)
- `updated_at` timestamp is updated

**Success Response**:
```
200 OK
Content-Type: application/json
```

```json
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": true,
  "user_id": "auth0|12345",
  "created_at": "2026-01-03T12:00:00Z",
  "updated_at": "2026-01-03T15:30:00Z"
}
```

**Error Responses**:
```
401 Unauthorized
{
  "error": "Unauthorized",
  "message": "User ID mismatch: token user does not match URL user_id",
  "details": null
}
```

```
404 Not Found
{
  "error": "Not found",
  "message": "Task not found",
  "details": null
}
```

---

## API Client Implementation Guide

### TypeScript Types

```typescript
// API Request/Response types (from data-model.md)
interface Task {
  id: number;
  title: string;
  description: string | null;
  completed: boolean;
  user_id: string;
  created_at: string;
  updated_at: string;
}

interface TaskCreate {
  title: string;
  description?: string;
}

interface TaskUpdate {
  title?: string;
  description?: string;
  completed?: boolean;
}

interface ErrorResponse {
  error: string;
  message: string;
  details?: Record<string, unknown>;
}
```

### API Client Function Signatures

```typescript
// src/lib/api-client.ts
async function getHealth(): Promise<{ status: string }>

async function createTask(
  userId: string,
  taskData: TaskCreate
): Promise<Task>

async function listTasks(userId: string): Promise<Task[]>

async function getTask(
  userId: string,
  taskId: number
): Promise<Task>

async function updateTask(
  userId: string,
  taskId: number,
  taskData: TaskUpdate
): Promise<Task>

async function deleteTask(
  userId: string,
  taskId: number
): Promise<void>

async function toggleCompletion(
  userId: string,
  taskId: number
): Promise<Task>
```

---

## Error Handling Patterns

### 401 Unauthorized
- **Action**: Redirect to login page
- **Reason**: JWT expired or invalid
- **Implementation**: Global fetch wrapper or API client

### 404 Not Found
- **Action**: Show "not found" error message
- **Reason**: Task doesn't exist or belongs to another user

### 422 Validation Error
- **Action**: Show field-level validation errors
- **Reason**: Input validation failed
- **Implementation**: Display `details` object keys/values to user

### 5xx Server Error
- **Action**: Show "something went wrong" with retry option
- **Reason**: Backend error
- **Implementation**: Retry button, check connection

---

## Summary

**Key Points**:
1. All endpoints require `Authorization: Bearer <token>` header
2. `user_id` in URL must match JWT `sub` claim (401 if mismatch)
3. Backend enforces user isolation automatically
4. All responses use standard JSON format with typed structures
5. CRUD operations fully supported (Create, Read, Update, Delete)
6. Completion toggle is a dedicated endpoint for UX optimization
7. Frontend API client must extract token from Better Auth session

**Next**: Quickstart Guide (quickstart.md) - Step-by-step implementation instructions
