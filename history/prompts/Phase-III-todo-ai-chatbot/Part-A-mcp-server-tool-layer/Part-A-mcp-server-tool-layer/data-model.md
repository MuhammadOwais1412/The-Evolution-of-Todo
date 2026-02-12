# Data Model: MCP Server & Tool Layer

## Task Entity

### Core Properties
- `id`: UUID (primary key) - Unique identifier for each task
- `user_id`: UUID (foreign key) - Links task to authenticated user
- `title`: String (required) - Task title/description (max 255 chars)
- `description`: String (optional) - Detailed task description (max 1000 chars)
- `completed`: Boolean - Completion status (default: false)
- `created_at`: DateTime - Timestamp of creation
- `updated_at`: DateTime - Timestamp of last update
- `priority`: String (optional) - Priority level (enum: low, medium, high)

### Validation Rules
- `title` must be 1-255 characters
- `user_id` must be a valid UUID format
- `priority` if provided must be one of: 'low', 'medium', 'high'
- `completed` must be boolean type

## MCP Tool Parameters

### Common Parameters
- `user_id`: Required UUID for all operations to ensure user isolation

### add_task Parameters
- `title`: Required string
- `description`: Optional string
- `priority`: Optional string ('low', 'medium', 'high')

### list_tasks Parameters
- None required beyond `user_id`

### update_task Parameters
- `task_id`: Required UUID of task to update
- `title`: Optional string (if updating title)
- `description`: Optional string (if updating description)
- `priority`: Optional string ('low', 'medium', 'high')
- `completed`: Optional boolean (if updating completion status)

### complete_task Parameters
- `task_id`: Required UUID of task to mark complete/incomplete
- `completed`: Required boolean (true for complete, false for incomplete)

### delete_task Parameters
- `task_id`: Required UUID of task to delete

## Return Types

### Success Responses
- `add_task`: Returns created task object with all properties
- `list_tasks`: Returns array of task objects
- `update_task`: Returns updated task object
- `complete_task`: Returns updated task object
- `delete_task`: Returns confirmation object with deleted task ID

### Error Responses
- All tools return structured error object with:
  - `error_code`: String identifier for error type
  - `message`: Human-readable error description
  - `details`: Optional additional error context