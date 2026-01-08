# Data Model: Frontend Application

**Feature**: 003-frontend-better-auth
**Date**: 2026-01-03
**Source**: Backend API contracts (FastAPI Pydantic models)

## Overview

This document defines the frontend data model types based on the backend API schema. All types are TypeScript interfaces that mirror the backend Pydantic models for type-safe API communication.

---

## Entities

### User

**Purpose**: Represents an authenticated user managed by Better Auth.

**Fields**:
- `id: string` - Unique user identifier (from Better Auth)
- `email: string` - User email address (for login)

**Notes**:
- User creation and authentication handled by Better Auth
- User data not stored in backend database (Better Auth manages users)
- `user_id` is used as foreign key in Task entity

**Backend Mapping**: Managed by Better Auth, not in backend database schema

---

### Task

**Purpose**: Represents a todo item owned by a user.

**Fields**:
```typescript
interface Task {
  id: number;
  title: string;
  description: string | null;
  completed: boolean;
  user_id: string;
  created_at: string;  // ISO 8601 timestamp
  updated_at: string;  // ISO 8601 timestamp
}
```

**Validation Rules**:
- `id`: Auto-generated integer, unique per task
- `title`: Required, min 1 character, max 200 characters
- `description`: Optional, max 5000 characters if provided
- `completed`: Boolean, defaults to `false`
- `user_id`: Required, must match authenticated user's ID (from JWT)
- `created_at`: Auto-generated timestamp (ISO 8601 format)
- `updated_at`: Auto-updated timestamp (ISO 8601 format)

**Backend Mapping**: `backend/src/models/task.py` (Task SQLModel)

---

### TaskCreate

**Purpose**: Request payload for creating a new task.

**Fields**:
```typescript
interface TaskCreate {
  title: string;           // Required, 1-200 chars
  description?: string;    // Optional, max 5000 chars
}
```

**Validation Rules**:
- `title`: Required, min 1, max 200 characters
- `description`: Optional, max 5000 characters

**Backend Mapping**: `backend/src/api/tasks.py` (TaskCreate Pydantic model)

---

### TaskUpdate

**Purpose**: Request payload for updating an existing task.

**Fields**:
```typescript
interface TaskUpdate {
  title?: string;          // Optional, 1-200 chars
  description?: string;    // Optional, max 5000 chars
  completed?: boolean;     // Optional, toggles completion
}
```

**Validation Rules**:
- All fields optional (partial update supported)
- If `title` provided: min 1, max 200 characters
- If `description` provided: max 5000 characters

**Backend Mapping**: `backend/src/api/tasks.py` (TaskUpdate Pydantic model)

---

### ErrorResponse

**Purpose**: Standard error response from backend API.

**Fields**:
```typescript
interface ErrorResponse {
  error: string;
  message: string;
  details?: Record<string, unknown>;
}
```

**Backend Mapping**: `backend/src/api/tasks.py` (ErrorResponse Pydantic model)

---

## Relationships

### User → Tasks

**Relationship**: One-to-Many (One user has many tasks)

**Implementation**:
- Tasks have `user_id` foreign key referencing the user
- Backend enforces user isolation: users can only access their own tasks
- Frontend must pass `user_id` in URL path (e.g., `/{user_id}/tasks`)
- Backend verifies JWT `sub` claim matches URL `user_id`

**Example**:
```
User (auth0|12345)
├── Task (id: 1, user_id: auth0|12345)
├── Task (id: 2, user_id: auth0|12345)
└── Task (id: 3, user_id: auth0|12345)
```

---

## State Transitions

### Task Completion Toggle

**Initial State**: Task created with `completed: false`

**Transition**: User clicks completion toggle

**Action**:
1. Frontend calls `PATCH /{user_id}/tasks/{task_id}/complete`
2. Backend toggles `completed` field (false → true or true → false)
3. Backend returns updated Task object
4. Frontend updates UI to reflect new completion state

**Error Handling**:
- If task not found (404): Show error, keep existing state
- If unauthorized (401): Redirect to login
- If network error: Retry option

---

### Task Edit

**Initial State**: Task exists with current title/description

**Transition**: User edits task details

**Action**:
1. Frontend opens edit modal/form with current values
2. User modifies fields (client-side validation)
3. Frontend calls `PUT /{user_id}/tasks/{task_id}` with TaskUpdate payload
4. Backend validates and updates task
5. Backend returns updated Task object
6. Frontend updates UI

**Error Handling**:
- If validation error (422): Show field-level errors
- If not found (404): Show error, redirect to task list
- If unauthorized (401): Redirect to login

---

### Task Deletion

**Initial State**: Task exists

**Transition**: User confirms deletion

**Action**:
1. Frontend shows confirmation dialog
2. User confirms
3. Frontend calls `DELETE /{user_id}/tasks/{task_id}`
4. Backend deletes task (returns 204 No Content)
5. Frontend removes task from list (optimistic update)

**Error Handling**:
- If not found (404): Already deleted, remove from local state
- If unauthorized (401): Redirect to login
- If user cancels: No action

---

## Frontend State Management

### AuthContext State

```typescript
interface AuthState {
  isAuthenticated: boolean;
  userId: string | null;
  token: string | null;  // JWT from Better Auth
  isLoading: boolean;
  error: string | null;
}
```

### TaskContext State

```typescript
interface TaskState {
  tasks: Task[];
  isLoading: boolean;
  error: string | null;
}
```

### UI Component State (Local)

```typescript
interface ComponentState {
  isEditing: boolean;       // Edit modal open/closed
  isDeleting: boolean;      // Delete confirmation
  formValues: Partial<TaskCreate | TaskUpdate>;
  errors: Record<string, string>;  // Field-level validation errors
}
```

---

## Summary

**Key Points**:
1. All frontend types mirror backend Pydantic models for type safety
2. Backend is the source of truth; frontend state is transient
3. User isolation enforced by backend via JWT `sub` claim
4. Tasks have CRUD operations with completion toggle
5. Standard error response format for all endpoints
6. Minimal frontend state: auth session, task cache, and component UI state

**Next**: API Contracts (contracts/) - Define exact REST endpoints and request/response formats
