---
id: 003
title: create-plan-backend-foundation
stage: plan
date: 2026-01-01
surface: agent
model: claude-sonnet-4.5-20250929
feature: 002-backend-foundation
branch: 002-backend-foundation
user: Owais
command: /sp.plan
labels: ["plan", "backend", "fastapi", "postgresql", "jwt"]
links:
  spec: specs/Phase-2-full-stack-web-todo/002-backend-foundation/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/Phase-2-full-stack-web-todo/002-backend-foundation/plan.md
  - specs/Phase-2-full-stack-web-todo/002-backend-foundation/research.md
  - specs/Phase-2-full-stack-web-todo/002-backend-foundation/data-model.md
  - specs/Phase-2-full-stack-web-todo/002-backend-foundation/quickstart.md
  - specs/Phase-2-full-stack-web-todo/002-backend-foundation/contracts/openapi.yaml
  - .claude/agents/backend-development.md
tests: []
---

## Prompt

# Phase 2 – STEP 1 Plan  
## Backend System (Foundation Layer)

You are operating under **Spec-Driven Development (NON-NEGOTIABLE)**.

This plan MUST strictly follow:
- The Phase-2 Constitution
- The approved STEP-1 Backend Specification (`spec.md`)

If any conflict exists, the **constitution LModel + Neon PostgreSQL)
3. Task domain model definition (user-scoped)
4. Authentication verification (JWT via Better Auth secret)
5. CRUD + completion API endpoints
6. Error handling and validation
7. Manual API verification (curl / HTTP client)

---

## Constraints & Discipline

- Clean Architecture is required
- Spec → Plan → Tasks → Implementation (no shortcuts)
- No over-engineering
- No premature abstractions
- No manual coding outside Claude Code
- Only implement what the spec explicitly requires

---

## Deliverable of This Plan

This plan must enable generation of:
- plan.md for A fully working backend API
- Persistent, user-isolated task storage
- Secure, JWT-protected endpoints

---

## End of Plan Prompt

## Response snapshot

Generated comprehensive implementation plan for Phase 2 Backend Foundation with all Phase 0 and Phase 1 artifacts:

**Planning Artifacts Created**:

1. **research.md** - Resolved all technical unknowns:
   - Python 3.11+ selected for FastAPI compatibility
   - Layered architecture (models/services/api) for clean separation
   - SQLModel for single source of truth (Pydantic + SQLAlchemy)
   - asyncpg driver for non-blocking PostgreSQL operations
   - JWT verification only (Better Auth handles token issuance)
   - Two-layer user isolation (API + service)
   - Structured error responses with status codes
   - Manual SQL migrations (no Alembic over-engineering)
   - pytest + httpx for async API testing
   - Standard Python package structure

2. **data-model.md** - Complete Task entity definition:
   - Fields: id, title, description, completed, user_id, created_at, updated_at
   - Validation: title (1-200 chars), description (optional, max 5000 chars)
   - Indexes: user_id (isolation), completed (query optimization)
   - State transitions: completed toggle via PATCH endpoint
   - Data access patterns for all CRUD operations

3. **contracts/openapi.yaml** - Full API specification:
   - 6 endpoints: GET (list, get), POST, PUT, DELETE, PATCH (complete)
   - JWT bearer authentication scheme
   - Structured error response schema (error, message, details)
   - Input schemas: TaskCreate, TaskUpdate
   - Output schema: Task with all fields
   - All response codes documented (200, 201, 204, 400, 401, 404, 422, 500)

4. **quickstart.md** - Developer onboarding guide:
   - Neon PostgreSQL setup instructions
   - Environment configuration (.env setup)
   - Dependency installation
   - Server startup (uvicorn)
   - JWT token acquisition
   - 8 manual test scenarios with curl commands
   - Troubleshooting section
   - Success criteria checklist

5. **plan.md** - Comprehensive implementation plan:
   - Technical context (Python 3.11+, FastAPI, SQLModel, Neon, asyncpg)
   - Constitution check (all applicable gates passed)
   - Project structure (backend/ with layers: models, services, api)
   - Architecture decisions for all major technology choices
   - API endpoint summary
   - Non-functional requirements (performance, reliability, security, observability, maintainability)
   - Operational readiness (deployment, database, health checks)
   - Risk analysis with mitigation strategies
   - Success criteria verification mapping to spec

6. **.claude/agents/backend-development.md** - Updated agent context:
   - Added complete technology stack section
   - Project structure reference
   - Key architectural patterns
   - Environment variables
   - API endpoints list
   - OpenAPI documentation locations

**Constitution Compliance**:
- I. Persistence & State Ownership: ✅ Neon PostgreSQL, backend owns state
- II. Clean Architecture: ✅ Layered separation (models/services/api)
- V. API-First & Validation: ✅ REST only, Pydantic validation
- VII. API-First Architecture: ✅ Clear contracts in OpenAPI spec
- VIII. Separation of Concerns: ✅ No UI logic, domain in services

**Architecture Decisions**:
- FastAPI over Flask/Django (async, auto-docs, performance)
- SQLModel over raw SQL/SQLAlchemy alone (single source of truth)
- asyncpg over psycopg2 (non-blocking, performance)
- JWT verification only (Better Auth handles issuance)
- Two-layer isolation (defense-in-depth)

No violations detected. All requirements from spec addressed. Ready for `/sp.tasks` to generate implementation tasks.

## Outcome

- ✅ Impact: Complete implementation plan created for backend API foundation with all technical decisions resolved, architecture defined, and contracts documented
- 🧪 Tests: None applicable (planning phase)
- 📁 Files: Created plan.md, research.md, data-model.md, quickstart.md, contracts/openapi.yaml, updated .claude/agents/backend-development.md
- 🔁 Next prompts: /sp.tasks to generate executable implementation tasks, then /sp.implement to run them
- 🧠 Reflection: Plan strictly follows spec-driven development. Specification was complete with clear user stories, functional requirements, and success criteria. All technical unknowns resolved in research.md without needing external queries. Clean architecture (models → services → api layers) aligns with Constitution Principle II. User isolation via JWT verification at API + service layers provides defense-in-depth. No premature abstractions - only what spec requires (single Task entity, 6 endpoints). Ready for task generation.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A - planning complete, ready for implementation

