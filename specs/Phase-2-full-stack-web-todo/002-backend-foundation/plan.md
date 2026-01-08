# Implementation Plan: Backend Foundation

**Branch**: `002-backend-foundation` | **Date**: 2026-01-01 | **Spec**: ./spec.md
**Input**: Feature specification from `specs/Phase-2-full-stack-web-todo/002-backend-foundation/spec.md`

## Summary

Build a production-grade REST API backend for the multi-user todo application using Python FastAPI, SQLModel, and Neon PostgreSQL. The system enforces strict user isolation via Better Auth JWT tokens, provides full CRUD operations for tasks, and follows clean architecture principles.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: FastAPI, SQLModel, python-jose, asyncpg, pytest, httpx
**Storage**: Neon Serverless PostgreSQL (async connection via asyncpg)
**Testing**: pytest + pytest-asyncio + httpx for integration testing
**Target Platform**: Linux server (production), local development (dev)
**Project Type**: web (REST API backend)
**Performance Goals**: p95 latency < 200ms for CRUD operations
**Constraints**: < 200ms p95, single database, JWT-based auth, no over-engineering
**Scale/Scope**: Single database, single app instance (Phase 2 scope)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **I. Persistence & State Ownership**: Neon PostgreSQL used, backend is source of truth? YES
- [x] **II. Clean Architecture**: Domain logic in backend, UI thin? YES
- [x] **V. API-First & Validation**: Interaction only via REST, structured errors? YES
- [x] **VII. API-First Architecture**: Clear request/response contracts? YES
- [x] **VIII. Separation of Concerns**: No business logic in UI? YES
- [ ] **Web UX Standards**: Responsive, loading/error states handled? SKIPPED - UI not in Step 1

**Result**: All applicable gates passed. No violations requiring justification.


## Project Structure

### Documentation (this feature)

```text
specs/Phase-2-full-stack-web-todo/002-backend-foundation/
├── spec.md              # Feature specification
├── plan.md              # This file
├── research.md          # Phase 0 output - Technical decisions
├── data-model.md        # Phase 1 output - Task entity
├── quickstart.md        # Phase 1 output - Developer guide
├── contracts/           # Phase 1 output - API contracts
│   └── openapi.yaml     # OpenAPI 3.0 spec
└── tasks.md             # Phase 2 output
```

### Source Code (repository root)

```text
backend/
├── pyproject.toml              # Dependencies
├── .env.example                # Environment template
├── src/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app
│   ├── config.py               # Config loading
│   ├── db.py                   # Database setup
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py             # Task SQLModel
│   ├── services/
│   │   ├── __init__.py
│   │   └── task_service.py     # Task business logic
│   └── api/
│       ├── __init__.py
│       ├── deps.py             # JWT, DB deps
│       └── tasks.py            # Task endpoints
└── tests/
    ├── __init__.py
    ├── conftest.py             # Fixtures
    └── test_tasks.py           # Tests
```

**Structure Decision**: Layered architecture - models → services → api

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | N/A | No violations detected |

## Architecture & Design Decisions

### 1. Framework: FastAPI
**Rationale**: Native async, auto OpenAPI docs, Pydantic integration

### 2. ORM: SQLModel
**Rationale**: Single source of truth (SQLModel = Pydantic + SQLAlchemy)

### 3. Database Driver: asyncpg
**Rationale**: Fastest PostgreSQL driver, native async

### 4. Auth: JWT Verification Only
**Rationale**: Better Auth issues tokens, backend only verifies

### 5. User Isolation: Two-Layer
**Rationale**: API layer (fast fail) + service layer (defense-in-depth)

### 6. Error Handling: Structured
**Rationale**: Client-friendly, debuggable, matches Constitution V

## API Endpoints

- `GET /api/{user_id}/tasks` - List tasks
- `POST /api/{user_id}/tasks` - Create task
- `GET /api/{user_id}/tasks/{task_id}` - Get task
- `PUT /api/{user_id}/tasks/{task_id}` - Update task
- `DELETE /api/{user_id}/tasks/{task_id}` - Delete task
- `PATCH /api/{user_id}/tasks/{task_id}/complete` - Toggle completion

## Data Model

**Task Entity**:
```python
class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=200, min_length=1)
    description: Optional[str] = Field(default=None, max_length=5000)
    completed: bool = Field(default=False)
    user_id: str = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

See `data-model.md` for full specification.

## Success Criteria Verification

- SC-001: API endpoints work (verify via quickstart.md)
- SC-002: Persistence verified (Neon database)
- SC-003: 401 on unauthorized requests
- SC-004: p95 < 200ms (benchmark during testing)
- SC-005: User isolation enforced (all endpoints)

## Next Steps

1. Run `/sp.tasks` to generate tasks.md
2. Implement tasks in order
3. Run manual verification
4. Create pull request

## References

- Spec: spec.md
- Research: research.md
- Data Model: data-model.md
- Quickstart: quickstart.md
- Contracts: contracts/openapi.yaml
- Constitution: .specify/memory/constitution.md

