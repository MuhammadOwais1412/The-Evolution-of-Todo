---
id: 013
title: Frontend Better Auth Plan
stage: plan
date: 2026-01-03
surface: agent
model: claude-sonnet-4-5-20250929
feature: 003-frontend-better-auth
branch: main
user: unknown
command: /sp.plan
labels: ["nextjs", "better-auth", "jwt", "rest-api", "frontend"]
links:
  spec: ../specs/003-frontend-better-auth/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/003-frontend-better-auth/plan.md
 - specs/003-frontend-better-auth/research.md
 - specs/003-frontend-better-auth/data-model.md
 - specs/003-frontend-better-auth/quickstart.md
 - specs/003-frontend-better-auth/contracts/api-endpoints.md
tests:
 - none
---

## Prompt

# Plan.md — STEP 2: Frontend Application (Presentation Layer)

Analyze the approved **STEP 2 Frontend Specification** inside 003-frontend-better-auth and the project constitution, then generate a **clear, execution-oriented implementation plan** for the frontend layer.

## Scope & Context

- This step implements the **Frontend Application only**
- Backend (STEP 1) is complete, stable, and must NOT be modified
- Frontend must live **strictly inside**: Phase-2-web-todo/frontend/
- Separation of concerns is mandatory

---

## Must-Follow Requirements

The plan MUST:

1. Use **Next.js 16+ with App Router**
2. Implement **Better Auth** for user signup/signin
3. Configure Better Auth to **issue JWT tokens**
4. Attach JWT to every backend API request: Authorization: Bearer <token>

5. Communicate with backend **only via REST API**
6. Implement full **Todo CRUD + completion** via backend APIs
7. Build a **responsive, minimal, professional UI**
8. Respect backend-enforced user isolation
9. Follow **clean architecture** and **spec-driven workflow**
10. Avoid unnecessary abstractions or module systems

---

## Plan Structure Requirements

The plan must:

- Be broken into **ordered, logical steps**
- Clearly identify **dependencies** (e.g. auth before API calls)
- Specify:
- Auth setup
- API client setup
- Page/route structure
- State handling
- Assume backend endpoints and JWT verification already exist
- Remain concise and implementation-focused

---

## Output Expectation

Produce a **professional, minimal, step-by-step plan** suitable for direct execution by an engineer, aligned with the approved specs and constitution.

## Response snapshot

Successfully generated comprehensive implementation plan for frontend application with Better Auth JWT authentication. Created five artifacts: plan.md (technical context and constitution check), research.md (technology decisions), data-model.md (frontend types), contracts/api-endpoints.md (REST API specifications), and quickstart.md (step-by-step implementation guide). All artifacts align with constitution principles and backend API contracts.

## Outcome

- ✅ Impact: Complete frontend architecture plan with Next.js 16+, Better Auth JWT configuration, REST API client, and responsive UI approach. All constitution principles verified and documented.
- 🧪 Tests: none
- 📁 Files: Created 5 planning artifacts totaling ~20KB of documentation
- 🔁 Next prompts: /sp.tasks to generate implementation tasks with test cases
- 🧠 Reflection: Backend-first architecture with clear separation of concerns; frontend is purely presentation layer delegating all domain logic to backend via REST API.

## Evaluation notes (flywheel)

- Failure modes observed: Setup script initially returned wrong feature branch (001-project-spec-alignment instead of 003-frontend-better-auth). Resolved by manually reading spec and creating artifacts. Agent context update script attempted to use wrong plan file but completed (may have incorrect data).
- Graders run and results (PASS/FAIL): PASS - All constitution checks passed, no violations documented. Plan follows spec requirements exactly.
- Prompt variant (if applicable): None
- Next experiment (smallest change to try): Improve setup-plan.ps1 to correctly detect current working feature branch instead of relying on git branch or environment variable. Add manual --feature override flag.
