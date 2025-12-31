# Feature Specification: Phase 2 Step 1 Backend Foundation

**Feature Branch**: `002-backend-foundation`
**Created**: 2025-12-31
**Status**: Draft
**Input**: User description: "Phase 2 Step 1: Backend System Foundation Layer"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Create and Retrieve Tasks (Priority: P1)

As a verified user, I want to create new tasks and retrieve my list of tasks via the REST API so that I can manage my todo list programmatically.

**Why this priority**: Managing the list is the core functionality of a todo app. Without basic CRUD, the system has no value.

**Independent Test**: Can be tested by sending a POST request to `/api/{user_id}/tasks` with task details and then a GET request to verify the task appears in the list.

**Acceptance Scenarios**:

1. **Given** a valid JWT token for user "A", **When** a POST request is made to `/api/A/tasks` with `{"title": "Buy milk"}`, **Then** the system returns `201 Created` and reflects the new task.
2. **Given** a valid JWT token for user "A", **When** a GET request is made to `/api/A/tasks`, **Then** the system returns a list containing "Buy milk".

---

### User Story 2 - Task Completion Lifecycle (Priority: P2)

As a user, I want to toggle the completion status of my tasks so that I can keep track of what I've accomplished.

**Why this priority**: Toggle completion is a primary interaction in a todo app.

**Independent Test**: Can be tested by sending a PATCH request to `/api/{user_id}/tasks/{id}/complete` and verifying the `completed` field changes state in the database.

**Acceptance Scenarios**:

1. **Given** an existing incomplete task with ID "101" for user "A", **When** user "A" sends a PATCH to `/api/A/tasks/101/complete`, **Then** the task's `completed` status becomes `true`.
2. **Given** an existing complete task with ID "101" for user "A", **When** user "A" sends a PATCH to `/api/A/tasks/101/complete`, **Then** the task's `completed` status becomes `false`.

---

### User Story 3 - Secure User Isolation (Priority: P1)

As a user, I want to ensure my tasks are private and cannot be accessed or modified by other users.

**Why this priority**: Security and data privacy are non-negotiable for multi-user systems.

**Independent Test**: Can be tested by attempting to access User A's tasks using User B's token and verifying a `401 Unauthorized` or `404 Not Found`/`403 Forbidden` response.

**Acceptance Scenarios**:

1. **Given** user "B" has a valid JWT, **When** they attempt a GET request to `/api/A/tasks`, **Then** the system returns `401 Unauthorized`.
2. **Given** user "B" has a valid JWT, **When** they attempt to DELETE `/api/A/tasks/101`, **Then** the system returns `401 Unauthorized`.

---

### Edge Cases

- **Invalid JWT**: What happens when an expired or modified JWT is provided? (System MUST return 401).
- **Malformed Payload**: How does the system handle a POST request with missing required fields like `title`? (System MUST return 400/422 with clear validation errors).
- **Task Not Found**: What happens when updating or deleting a task ID that doesn't exist? (System MUST return 404).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a REST API for CRUD operations on tasks.
- **FR-002**: System MUST implement Python FastAPI as the web framework.
- **FR-003**: System MUST use SQLModel for ORM and schema definitions.
- **FR-004**: System MUST persist data in a Neon Serverless PostgreSQL database.
- **FR-005**: System MUST enforce user isolation: users can only see/modify their own tasks.
- **FR-006**: System MUST verify JWT tokens issued by Better Auth using the `BETTER_AUTH_SECRET`.
- **FR-007**: System MUST validate that the `{user_id}` in the URL matches the identity in the JWT.
- **FR-008**: System MUST support a `PATCH /api/{user_id}/tasks/{id}/complete` endpoint to toggle completion status.

### Key Entities *(include if feature involves data)*

- **Task**: Represents a todo item.
  - `id`: Unique identifier (UUID or Serial).
  - `title`: String (required, validated length).
  - `description`: String (optional).
  - `completed`: Boolean (defaults to false).
  - `user_id`: String/UUID (links task to its owner).
  - `created_at`: Timestamp.
  - `updated_at`: Timestamp.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: API endpoints respond successfully via HTTP client (curl/Postman) without a frontend.
- **SC-002**: Database state persists consistently across application restarts.
- **SC-003**: Unauthorized requests (missing token, invalid token, cross-user access) correctly return `401 Unauthorized`.
- **SC-004**: Task creation and retrieval latency is negligible (p95 < 200ms).
- **SC-005**: 100% of task operations are restricted to the owner identity extracted from the JWT.
