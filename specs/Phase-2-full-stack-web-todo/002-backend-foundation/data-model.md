# Data Model: Backend Foundation

**Feature**: 002-backend-foundation | **Date**: 2026-01-01
**Purpose**: Define domain entities, relationships, and validation rules.

## Entity: Task

### Description
Represents a todo item owned by a user in the multi-user todo system.

### Fields

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `id` | `int` (SERIAL) | Yes | Primary key, auto-increment | Unique identifier for the task |
| `title` | `str` (VARCHAR 200) | Yes | 1-200 characters | Task title/title |
| `description` | `str` (TEXT) | No | Max 5000 characters | Optional detailed description |
| `completed` | `bool` | No | Default: `false` | Completion status flag |
| `user_id` | `str` (VARCHAR 255) | Yes | Non-empty, indexed | Foreign reference to task owner |
| `created_at` | `datetime` | Yes | Default: current timestamp | Task creation timestamp |
| `updated_at` | `datetime` | Yes | Default: current timestamp, auto-update | Last modification timestamp |

### Relationships

| Relationship | Target Entity | Cardinality | Description |
|--------------|---------------|-------------|-------------|
| `owner` | (Future: User entity) | Many-to-One | Task belongs to exactly one user |

### Validation Rules

1. **Title**:
   - Must be non-empty string
   - Minimum length: 1 character
   - Maximum length: 200 characters
   - Cannot be null

2. **Description**:
   - Optional (can be null)
   - Maximum length: 5000 characters

3. **User ID**:
   - Must be non-empty string
   - Validated against JWT claim during API calls
   - Cannot be null

4. **Timestamps**:
   - `created_at`: Set once on creation, never modified
   - `updated_at`: Updated on every write operation

### State Transitions

**Completed Status**:
- `false` → `true`: Task marked as complete (PATCH `/api/{user_id}/tasks/{id}/complete`)
- `true` → `false`: Task marked as incomplete (same endpoint)
- Transition is idempotent (calling complete twice on `true` returns `true`)

### Constraints

**Database Constraints**:
```sql
-- Primary key
PRIMARY KEY (id)

-- User isolation index
CREATE INDEX idx_tasks_user_id ON tasks(user_id);

-- Query optimization index
CREATE INDEX idx_tasks_completed ON tasks(completed);

-- Title non-null constraint
NOT NULL (title)

-- User_id non-null constraint
NOT NULL (user_id)
```

### SQLModel Definition

```python
from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=200, min_length=1)
    description: Optional[str] = Field(default=None, max_length=5000)
    completed: bool = Field(default=False)
    user_id: str = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Buy groceries",
                "description": "Milk, eggs, bread",
                "completed": False,
                "user_id": "auth0|12345",
                "created_at": "2026-01-01T12:00:00Z",
                "updated_at": "2026-01-01T12:00:00Z"
            }
        }
```

## Future Entities (Out of Scope for Step 1)

The following entities are NOT part of Step 1 implementation:

- **User**: Authentication is handled by Better Auth; no local user table needed
- **Lists/Tags**: Not required for current scope
- **Comments**: Not required for current scope

## Data Access Patterns

### Create Task
```python
async def create_task(session: AsyncSession, task: TaskCreate, user_id: str) -> Task:
    db_task = Task(**task.dict(), user_id=user_id)
    session.add(db_task)
    await session.commit()
    await session.refresh(db_task)
    return db_task
```

### Read Tasks by User
```python
async def get_tasks_by_user(session: AsyncSession, user_id: str) -> List[Task]:
    stmt = select(Task).where(Task.user_id == user_id).order_by(Task.created_at.desc())
    result = await session.execute(stmt)
    return result.scalars().all()
```

### Toggle Completion
```python
async def toggle_completion(session: AsyncSession, task_id: int, user_id: str) -> Optional[Task]:
    stmt = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    result = await session.execute(stmt)
    task = result.scalar_one_or_none()
    if task:
        task.completed = not task.completed
        task.updated_at = datetime.utcnow()
        await session.commit()
        await session.refresh(task)
    return task
```

### Delete Task
```python
async def delete_task(session: AsyncSession, task_id: int, user_id: str) -> bool:
    stmt = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    result = await session.execute(stmt)
    task = result.scalar_one_or_none()
    if task:
        await session.delete(task)
        await session.commit()
        return True
    return False
```

## Indexes

| Index | Fields | Purpose | Query Pattern |
|-------|--------|---------|---------------|
| `PRIMARY` | `id` | Unique row identification | `SELECT * FROM tasks WHERE id = ?` |
| `idx_tasks_user_id` | `user_id` | User isolation, list queries | `SELECT * FROM tasks WHERE user_id = ?` |
| `idx_tasks_completed` | `completed` | Filter by completion status | `SELECT * FROM tasks WHERE user_id = ? AND completed = ?` |

## Security Considerations

1. **Row-Level Access**: All database queries MUST include `user_id` in WHERE clause
2. **SQL Injection Prevention**: SQLModel/SQLAlchemy handles parameterized queries automatically
3. **Input Validation**: Pydantic models validate all inputs before database operations
4. **Timestamp Integrity**: `created_at` never modified, `updated_at` updated on every write

## Migration Notes

**Initial Schema** (Step 1):
- Single `tasks` table
- No schema version tracking (manual migrations for now)
- Indexes created at schema creation

**Future Migrations** (if needed):
- Add new columns using ALTER TABLE
- Add new indexes using CREATE INDEX
- No breaking changes to existing columns
