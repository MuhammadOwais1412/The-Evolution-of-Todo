# Data Model: Phase II - Full-Stack Todo Application

**Created**: 2026-01-10

## Entities

### User Session
- **Description**: Represents authenticated user state
- **Fields**:
  - sessionId: string (unique identifier for the session)
  - userId: string (identifier from Better Auth)
  - jwtToken: string (JWT token issued by Better Auth)
  - createdAt: datetime (session creation timestamp)
  - expiresAt: datetime (session expiration timestamp)
- **Relationships**: Links to user's tasks via userId

### Task
- **Description**: Represents individual todo items
- **Fields**:
  - id: integer (primary key, auto-increment)
  - title: string (task title, max 255 characters)
  - description: string (optional task description)
  - completed: boolean (completion status, default false)
  - userId: string (foreign key to user who owns the task)
  - createdAt: datetime (task creation timestamp)
  - updatedAt: datetime (last modification timestamp)
- **Validation Rules**:
  - Title is required (not null)
  - Title must be between 1-255 characters
  - UserId is required (not null)
  - Completed defaults to false
- **Relationships**: Belongs to a single User via userId

### Authentication Token
- **Description**: JWT issued by Better Auth for backend API authorization
- **Fields**:
  - token: string (the JWT token string)
  - userId: string (user identifier from Better Auth)
  - issuedAt: datetime (token creation timestamp)
  - expiresAt: datetime (token expiration timestamp)
  - issuer: string (who issued the token - Better Auth)
- **Validation Rules**:
  - Token is required (not null)
  - Token must be a valid JWT format
  - Expiration must be in the future
- **Relationships**: Associated with user who can use it for API access

## Relationships

### User Session → Tasks
- One user session can access many tasks
- Foreign key: userId in Task table references user identifier in session
- Constraint: Users can only access tasks with matching userId

### Authentication Token → User Session
- One authentication token corresponds to one user session
- The token's userId must match the session's userId
- Constraint: Token must be valid and not expired

## State Transitions

### Task State Transitions
- **Created**: New task with completed = false
- **Updated**: Task details modified (title, description)
- **Completed**: Task completed status changed to true
- **Reopened**: Completed task status changed back to false
- **Deleted**: Task removed from system

### User Session State Transitions
- **Started**: User logs in, session created with JWT token
- **Active**: User interacts with system using valid token
- **Expired**: Session token expires, requires re-authentication
- **Terminated**: User logs out, session invalidated

## Constraints

### Data Integrity
- All tasks must have a valid userId that corresponds to an authenticated user
- Task titles cannot exceed 255 characters
- Task completion status is binary (true/false)
- Created/updated timestamps are automatically managed

### Access Control
- Users can only access tasks with their own userId
- Backend enforces user isolation at the API level
- Authentication tokens must be valid and unexpired for API access

### Audit Trail
- Creation and modification timestamps are automatically recorded
- User identity is tracked for all operations
- Authentication events are logged for security monitoring