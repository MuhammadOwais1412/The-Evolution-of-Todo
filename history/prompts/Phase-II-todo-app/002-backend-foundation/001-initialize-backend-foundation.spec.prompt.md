---
id: 001
title: Initialize Phase 2 Step 1 Backend Foundation Spec
stage: spec
date: 2025-12-31
surface: agent
model: claude-sonnet-4-5-20250929
feature: backend-foundation
branch: 002-backend-foundation
user: Owais
command: /sp.specify
labels: ["spec", "backend", "fastapi", "foundation"]
links:
  spec: specs/002-backend-foundation/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-backend-foundation/spec.md
  - specs/002-backend-foundation/checklists/requirements.md
tests:
  - none
---

## Prompt

# Phase 2 – STEP 1 Spec
## Backend System (Foundation Layer)

You are operating under **Spec-Driven Development (NON-NEGOTIABLE)**.

This specification defines **STEP 1 ONLY** of Phase 2.
No frontend implementation is allowed in this step.

---

## 1. Phase-2 System Definition (High-Level)

The Phase-2 system is a **Full-Stack Todo Application** whose backend acts as:

- The **single source of truth**
- The **owner of business logic**
- The **enforcer of authentication and user isolation**
- The **only authority over persistence**

The backend exposes a **REST API** consumed by a separate frontend (built later).
The backend MUST be fully usable and verifiable **without any frontend**.

---

## 2. Core Rule — Lock Business Model Before APIs

Before defining or implementing API routes:

- The **Task domain model** MUST be fully specified
- Task fields, constraints, identity rules, and lifecycle MUST be finalized
- User–Task ownership MUST be explicit
- Completion semantics MUST be unambiguous

🚫 API behavior MUST NOT define business rules
✅ APIs may only expose already-defined domain behavior

---

## 3. Scope of This Step (STRICT)

### In Scope
- Backend service only
- Domain model
- Database persistence
- REST API
- Authentication verification
- User-scoped data access

### Out of Scope
- Frontend or UI logic
- Styling or UX
- Cloud deployment

---

## 4. Technical Requirements (Binding)

The backend MUST be implemented using:

- **Backend Framework:** Python FastAPI
- **ORM:** SQLModel
- **Database:** Neon Serverless PostgreSQL
- **API Style:** REST
- **Authentication:** Better Auth (JWT-based)
- **Architecture:** Clean Architecture
- **Workflow:** Spec → Plan → Tasks → Implementation

Manual coding without Claude Code is NOT permitted.

---

## 5. Functional Requirements

The backend MUST support the following **task operations**:

- Create task
- Read task(s)
- Update task
- Delete task
- Toggle completion status

All operations MUST:
- Be scoped to the authenticated user
- Validate input
- Enforce task ownership
- Return clear error responses

---

## 6. REST API Contract (Fixed)

The following endpoints MUST exist and MUST NOT change:

| Method | Endpoint | Description |
|------|---------|-------------|
| GET | /api/{user_id}/tasks | List all tasks |
| POST | /api/{user_id}/tasks | Create a new task |
| GET | /api/{user_id}/tasks/{id} | Get task details |
| PUT | /api/{user_id}/tasks/{id} | Update a task |
| DELETE | /api/{user_id}/tasks/{id} | Delete a task |
| PATCH | /api/{user_id}/tasks/{id}/complete | Toggle completion |

The backend MUST verify that:
- {user_id} matches the authenticated user
- Cross-user access is impossible

---

## 7. Authentication & Security Specification

### Authentication Model
- Better Auth runs on the frontend (outside this step)
- Better Auth issues **JWT tokens** after login
- Backend verifies JWT tokens on every request

### JWT Verification Rules
- Token is provided via `Authorization: Bearer <token>`
- Backend verifies signature using shared secret
- Backend extracts user identity from token
- Token verification is mandatory for all endpoints

### Shared Secret
- Both frontend and backend use the same secret
- Secret is provided via environment variable:
  `BETTER_AUTH_SECRET`

---

## 8. API Security Behavior (Mandatory)

After authentication is enabled:

- All endpoints REQUIRE a valid JWT
- Requests without token → `401 Unauthorized`
- Requests with invalid token → `401 Unauthorized`
- Users can only access their own tasks
- Task ownership is enforced at query level

---

## 9. What MUST Be Completed in This Step

The following MUST be fully implemented and working:

- FastAPI project setup
- Database integration (SQLModel + Neon PostgreSQL)
- Task domain model (CRUD + completion)
- User isolation logic (per-user tasks)
- JWT verification middleware (Better Auth compatible)
- Fully functional REST API matching this spec

---

## 10. Deliverables

At the end of this step:

- Backend runs independently
- API endpoints work via curl / HTTP client
- Data persists in the database
- Authentication is enforced
- No frontend is required or expected

---

## 11. Enforcement

If any instruction conflicts with:
- The Phase-2 Constitution
- This specification

Then:
1. The conflict MUST be reported
2. No silent deviations are allowed
3. This spec takes precedence over implementation convenience

---

## End of STEP 1 Spec

## Response snapshot

I have initialized the specification for the Phase 2 Step 1 Backend Foundation.
- Created branch `002-backend-foundation`.
- Generated `specs/002-backend-foundation/spec.md` with prioritized user stories (CRUD, completion, isolation).
- Defined Functional Requirements (FR-001 to FR-008) including technology mandates (FastAPI, SQLModel, Neon, Better Auth).
- Established Success Criteria for independent verification.
- Validated the spec against the Quality Checklist.

## Outcome

- ✅ Impact: Established foundation for Backend Phase 2.
- 🧪 Tests: Acceptance scenarios defined for P1 journeys.
- 📁 Files: spec.md, requirements.md.
- 🔁 Next prompts: /sp.plan
- 🧠 Reflection: The spec strictly avoids frontend logic as requested. User isolation and JWT verification are prioritized as P1 security requirements.

## Evaluation notes (flywheel)

- Failure modes observed: Initial branch creation script failed on manual command substitution; resolved with manual file/branch creation.
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): Proceeding to planning.
