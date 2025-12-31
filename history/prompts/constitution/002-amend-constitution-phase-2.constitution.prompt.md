---
id: 002
title: Amend Constitution for Phase 2 Full-Stack Web App
stage: constitution
date: 2025-12-31
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: Owais
command: /sp.constitution
labels: [constitution, phase-2, full-stack]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
  - .specify/templates/plan-template.md
  - .specify/templates/spec-template.md
tests:
  - N/A
---

## Prompt

# Task: Amend Constitution for Phase 2 – Todo Full-Stack Web Application

You are operating under **Spec-Driven Development (NON-NEGOTIABLE)**.

Phase 1 (Python Console Todo App) is **completed** and its constitution already exists.
Your task is to **edit, evolve, and formally amend** the existing constitution so it governs:

> **Phase 2: Todo Full-Stack Web Application**

This is NOT a greenfield constitution.
This is a **versioned constitutional evolution**.

---

## 1. Inputs You Must Use

You MUST read and use:

1. The existing `constitution.md` (Phase 1 – Python Console Todo App)
2. The Hackathon II – Todo Spec-Driven Development document
3. Phase 2 requirements defined in the hackathon:
   - Backend: Python FastAPI
   - Frontend: Next.js 16+ (App Router)
   - REST API between frontend and backend
   - ORM: SQLModel
   - Persistent storage (database allowed): Neon Serverless PostgreSQL
   - Authentication: – Implement user signup/signin using Better Auth
   - Clean architecture & spec-driven workflow
   - CRUD + completion functionality exposed via API and UI
   - Build responsive frontend interface
   - Securing the REST API: Better Auth + FastAPI Integration
   - Better Auth can be configured to issue JWT (JSON Web Token) tokens when users log in.

---

## 2. Core Objective

Produce an **updated constitution** that:

- Preserves valid Phase-1 principles
- Explicitly **removes or relaxes constraints** that no longer apply (e.g. in-memory only)
- Introduces **new, explicit rules** required for a Full-Stack Web system
- Clearly defines **scope boundaries for Phase 2**
- Remains learning-focused, correctness-first
- Is suitable for Claude Code + Spec-Kit Plus enforcement

---

## 3. Mandatory Structural Rules

The resulting constitution MUST:

1. Remain a **single `constitution.md` file**
2. Use **clear section headers**
3. Include a **version bump** (e.g. `1.0.0 → 2.0.0`)
4. Clearly reflect that this is **Phase 2**
5. Be written in **assertive, enforceable language** (MUST / MUST NOT / SHOULD)
6. Remain **technology-specific only where required** (FastAPI, Next.js)

---

## 4. Required Constitutional Changes (Non-Optional)

You MUST address all of the following explicitly:

### A. Persistence Rules
- Allow database usage
- Define ownership of state (backend only)
- Forbid frontend-side source-of-truth state
- Require explicit schema ownership

### B. API-First Architecture
- Backend is the system of record
- Frontend communicates ONLY via API
- Clear request/response contracts

### C. Clean Separation of Concerns
- Backend: domain logic, validation, persistence
- Frontend: rendering, user interaction, API calls
- No business logic leakage into UI components

### D. Spec-Driven Enforcement
- Specs → Plan → Tasks → Implementation
- No direct coding without approved specs
- Constitution overrides plans and tasks on conflict

### E. Error Handling & UX Guarantees
- API errors must be explicit and structured
- Frontend must handle loading, error, empty states
- User confusion is considered a failure

### F. Scope Expansion (Explicitly Allowed)
Include:
- Web UI
- REST APIs
- Database persistence
- Environment-based configuration
- Authentication / authorization
- Multi-user support
- Realtime features
- Background workers

---

## 5. Amendment Process Rules

You MUST:

1. Update the **Scope Boundaries** section for Phase 2
2. Update or replace **Console UX Standards** with **Web UX Standards**
3. Introduce **API Contracts & Data Flow Rules**
4. Add **Frontend–Backend Interaction Rules**
5. Update **Success Definition** to match Full-Stack delivery
6. Update **Version, Ratification Date, and Amendment Notes**

---

## 6. Output Requirements

Your final output MUST be:

- Fully rewritten `constitution.md`
- Clean and professional

---

## 8. Absolute Prohibitions

You MUST NOT:

- Introduce Phase 3+ concepts (cloud, Kafka, Dapr, Kubernetes)
- Add authentication or users
- Add speculative scalability concerns
- Over-engineer abstractions
- Change the spec-driven workflow

---

## Deliverable

Return ONLY the updated **Phase-2 Constitution Markdown**.
Nothing else.

## Response snapshot

The constitution has been updated to version 2.0.0, evolving from a Python Console Todo App to a Full-Stack Web Application. Core principles now include Persistence & State Ownership (Neon PostgreSQL), API-First Architecture (FastAPI), and Web UX Standards (Next.js). Constraints like "In-Memory Only" were removed, and new rules for frontend-backend interaction and separation of concerns were introduced. Dependent templates (plan and spec) were also synced.

## Outcome

- ✅ Impact: High - Governs the architecture and workflow for Phase 2.
- 🧪 Tests: No runtime tests; validation via checklist in templates.
- 📁 Files: constitution.md, plan-template.md, spec-template.md.
- 🔁 Next prompts: Start Phase 2 feature specification and planning.
- 🧠 Reflection: The transition from v1 to v2 reflects the shift from an educational CLI tool to a production-ready full-stack prototype.

## Evaluation notes (flywheel)

- Failure modes observed: Initial Edit tools failed due to invisible character mismatches (detected via cat -A).
- Graders run and results (PASS/FAIL): PASS (Manually verified constitution matches all requirements).
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
