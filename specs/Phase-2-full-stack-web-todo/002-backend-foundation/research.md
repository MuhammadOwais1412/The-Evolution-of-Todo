# Research Document: Backend Foundation

**Feature**: 002-backend-foundation | **Date**: 2026-01-01
**Purpose**: Resolve technical unknowns and validate technology choices for backend API implementation.

## Research Questions & Decisions

### 1. Python Version Selection

**Decision**: Python 3.11+
**Rationale**:
- Stable and widely supported
- Performance improvements over 3.10
- Excellent FastAPI and async support
- SQLModel and all dependencies fully compatible

**Alternatives Considered**:
- Python 3.12+: Too new, some dependency ecosystems still stabilizing
- Python 3.10: Stable but missing newer performance features

---

### 2. FastAPI Structure for Clean Architecture

**Decision**: Layered architecture with clear separation
- `src/models/`: SQLModel table definitions (data layer)
- `src/services/`: Business logic and database operations (domain layer)
- `src/api/`: FastAPI routers and request/response handling (presentation layer)

**Rationale**:
- Aligns with Constitution Principle II (Clean Architecture)
- Easy to test each layer independently
- Prevents business logic from leaking into API handlers
- Matches spec requirement for structured, maintainable code

**Alternatives Considered**:
- Monolithic single-file: Violates clean architecture principle
- DDD-style with repositories: Over-engineering for Phase 2 scope

---

### 3. SQLModel for ORM

**Decision**: Use SQLModel (built on Pydantic + SQLAlchemy)
**Rationale**:
- Single source of truth for schemas (Pydantic v2)
- SQLAlchemy 2.0 core for database operations
- Type-safe and IDE-friendly
- Perfect match for FastAPI (automatic validation)

**Alternatives Considered**:
- SQLAlchemy alone: More verbose, requires separate Pydantic schemas
- Django ORM: Too heavy, brings entire framework overhead
- Raw SQL: Manual validation, error-prone

---

### 4. Neon PostgreSQL Integration

**Decision**: Use async PostgreSQL driver with connection pooling
**Rationale**:
- Neon is serverless and scales automatically
- Async driver (asyncpg) matches FastAPI's async model
- Connection pooling reduces latency
- Spec explicitly requires Neon

**Configuration Pattern**:
```python
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_async_engine(DATABASE_URL, echo=False)
async_session = async_sessionmaker(engine)
```

**Alternatives Considered**:
- Synchronous driver: Blocks event loop, poor performance
- Multiple engines: Unnecessary for single database

---

### 5. JWT Verification Strategy

**Decision**: Validate Better Auth JWT using PyJWT with secret key
**Rationale**:
- Better Auth uses standard JWT format (HS256)
- PyJWT is lightweight and widely used
- Secret-based verification matches Better Auth architecture
- No external dependency on Better Auth SDK needed

**Implementation Pattern**:
```python
from jose import jwt, JWTError
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET")
ALGORITHM = "HS256"

async def verify_jwt(credentials: HTTPAuthorizationCredentials) -> str:
    """Verify JWT and return user_id"""
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")  # Standard claim for user ID
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

**Alternatives Considered**:
- Better Auth SDK: Adds unnecessary client dependency
- Manual crypto: Re-inventing JWT parsing

---

### 6. User Isolation Enforcement

**Decision**: Enforce at two layers - API router and service layer
**Rationale**:
- API layer: Quick fail-fast for wrong user_id path param
- Service layer: Extra defense-in-depth for all queries

**Implementation Pattern**:
```python
# API layer
@router.get("/api/{user_id}/tasks")
async def get_tasks(
    user_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    verified_user_id = await verify_jwt(credentials)
    if verified_user_id != user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return task_service.get_by_user(user_id)

# Service layer
async def get_by_user(user_id: str) -> List[Task]:
    stmt = select(Task).where(Task.user_id == user_id)
    result = await session.execute(stmt)
    return result.scalars().all()
```

**Alternatives Considered**:
- Only API layer: Insufficient defense
- Database row-level security: Overkill for current scope

---

### 7. Error Handling & Validation

**Decision**: Use FastAPI's built-in validation + custom exceptions
**Rationale**:
- Pydantic models provide automatic 400/422 for invalid input
- Custom exception handlers for consistent error responses
- Structured error body matches Constitution Principle V

**Error Response Format**:
```json
{
  "error": "validation_error",
  "message": "Title is required and must be between 1 and 200 characters",
  "details": {
    "field": "title",
    "constraint": "min_length=1, max_length=200"
  }
}
```

**Status Code Convention**:
- 400: Malformed request (missing/invalid JSON)
- 401: Unauthorized (missing/invalid JWT, user mismatch)
- 404: Resource not found
- 422: Validation error (Pydantic)
- 500: Internal server error

**Alternatives Considered**:
- Try/except in every endpoint: Repetitive and error-prone
- Global catch-all: Too coarse, loses context

---

### 8. Database Migration Strategy

**Decision**: Manual SQL scripts for initial schema (Alembic overkill)
**Rationale**:
- Single table (tasks) with simple schema
- Neon provides migration tools in dashboard
- No complex schema evolution needed for Phase 2
- Smallest viable change

**Schema SQL**:
```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    user_id VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_completed ON tasks(completed);
```

**Alternatives Considered**:
- Alembic: Over-engineering for simple table
- ORM auto-create: No version control, risky for production

---

### 9. Testing Approach

**Decision**: pytest + httpx for async API testing
**Rationale**:
- pytest is de facto standard for Python
- httpx.AsyncClient tests FastAPI endpoints without server
- Test fixtures for database session isolation
- Matches spec requirement for testability

**Test Structure**:
```python
@pytest.mark.asyncio
async def test_create_task(client, auth_header):
    response = await client.post(
        "/api/user123/tasks",
        json={"title": "Test task"},
        headers=auth_header
    )
    assert response.status_code == 201
    assert response.json()["title"] == "Test task"
```

**Alternatives Considered**:
- Postman/manual: Not automated, violates Constitution
- Unit tests only: Misses integration validation

---

### 10. Project Structure

**Decision**: Standard Python project layout
```
backend/
├── pyproject.toml          # Dependencies and config
├── .env.example             # Environment variables template
├── src/
│   ├── __init__.py
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Environment loading
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py          # Task SQLModel
│   ├── services/
│   │   ├── __init__.py
│   │   └── task_service.py  # Task business logic
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py          # Dependencies (JWT, DB session)
│   │   └── tasks.py         # Task endpoints
│   └── db.py                # Database engine setup
└── tests/
    ├── __init__.py
    ├── conftest.py          # Pytest fixtures
    └── test_tasks.py        # Task endpoint tests
```

**Rationale**:
- Follows Python packaging best practices
- Clear separation of concerns
- Easy to navigate for junior developers
- Matches Constitution Principle VIII (Separation of Concerns)

**Alternatives Considered**:
- Flat structure: Violates clean architecture
- Domain-driven design: Over-engineering for Phase 2

---

## Summary of Decisions

All decisions align with:
- Constitution principles (I, II, V, VII, VIII)
- Spec requirements (FR-001 through FR-008)
- Smallest viable change principle
- No premature abstractions

**No violations** detected in Constitution Check. All "NEEDS CLARIFICATION" items resolved.
