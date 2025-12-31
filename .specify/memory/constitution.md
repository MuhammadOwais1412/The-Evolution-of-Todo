<!--
Sync Impact Report:
- Version change: 1.0.0 → 2.0.0
- Modified principles:
  * Principle I: In-Memory Only → Persistence & State Ownership (Allowed DB, backend ownership)
  * Principle V: Input Validation & Error Handling → API-First & Validation (Structured errors, contracts)
- Added sections:
  * Principle VII: API-First Architecture
  * Principle VIII: Separation of Concerns
  * Web UX Standards (Replaced Console UX Standards)
  * Frontend-Backend Interaction Rules
- Removed sections:
  * Console UX Standards
- Templates status:
  * ⚠ spec-template.md - Needs alignment with Phase 2 scope
  * ⚠ plan-template.md - Needs structure update for backend/frontend
  * ⚠ tasks-template.md - Needs update for web phases
- Follow-up TODOs: Manual update of templates to reflect full-stack structure.
-->

# Todo Full-Stack Web Application Constitution

## Core Principles

### I. Persistence & State Ownership
The system MUST use persistent storage (Neon Serverless PostgreSQL via SQLModel). The backend is the sole owner of system state and the "source of truth." The frontend MUST NOT maintain a separate source-of-truth for domain data.

Rationale: Ensures data durability across sessions and maintains a single, reliable state repository.

### II. Clean Architecture
The system MUST adhere to Single Responsibility Principle, clear separation of concerns, and deterministic behavior. Logic MUST be layered: Domain logic in the backend, rendering and interaction logic in the frontend.

Rationale: Prevents business logic leakage, ensures testability, and maintains a manageable codebase as complexity grows.

### III. No Global Mutable State
Global mutable state is strictly prohibited. State ownership must be explicit (e.g., React context or state management for UI, backend services for domain). No hardcoded magic values.

Rationale: Maintains predictability and prevents side-effect-driven bugs in a distributed system (frontend/backend).

### IV. Spec-Driven Development (NON-NEGOTIABLE)
All development MUST follow: Specification → Plan → Tasks → Implementation. No coding without approved specs. The constitution overrides plans and tasks on conflict.

Rationale: Maintains traceability and prevents scope creep or architectural drift.

### V. API-First & Validation
Communication between frontend and backend MUST occur ONLY via structured REST APIs. Every operation MUST validate inputs at the system boundary (API endpoints). Errors MUST be explicit, structured, and actionable.

Rationale: Decouples components and ensures system integrity against malformed or malicious input.

### VI. Smallest Viable Change
Changes must be minimal, reversible, and traceable to requirements. No speculative features or premature abstractions for "Phase 3+."

Rationale: Focuses effort on current objectives and reduces cognitive load.

### VII. API-First Architecture
The backend is the system of record. The frontend communicates with the backend ONLY via the defined REST API. Request/response contracts MUST be clear and documented.

Rationale: Enables independent evolution of frontend and backend while maintaining a stable interface.

### VIII. Separation of Concerns
Backend handles domain logic, validation, and persistence. Frontend handles rendering, user interaction, and API calls. Business logic MUST NOT leak into UI components.

Rationale: Keeps the UI "thin" and the backend "authoritative," simplifying debugging and future changes.

## Scope Boundaries (Phase 2)

### In Scope
- Web UI (Next.js 16+ App Router)
- REST APIs (FastAPI)
- Database persistence (Neon PostgreSQL)
- Authentication/Authorization (Better Auth)
- Multi-user support
- Environment-based configuration
- CRUD operations exposed via UI and API

### Out of Scope
- Scalability beyond 10k users
- Cloud native complex architectures (Kubernetes, Kafka)
- Mobile applications (Native)
- Advanced real-time collaborative editing (except simple polling/refresh)

## Functional Guarantees

The application MUST support:
- Secure user signup and signin
- Personalised task lists (multi-user)
- Full CRUD functionality for tasks
- Persistent state across browser refreshes
- Responsive web design

## Frontend–Backend Interaction Rules

- All data fetching from the frontend MUST use the backend API.
- Frontend MUST handle loading, error, and empty states for all API interactions.
- Backend MUST return standard HTTP status codes and structured JSON error bodies.
- Authentication tokens (JWT) MUST be managed securely by Better Auth.

## Web UX Standards

The web interface MUST:
- Be responsive (work on mobile/tablet/desktop).
- Provide immediate visual feedback for user actions (optimistic updates or loading states).
- Use clear, professional typography and spacing.
- Handle error states gracefully with user-friendly messages.
- Ensure task completion toggles are visually distinct and immediate.

## Quality Standards

- Code MUST be readable by a junior developer.
- All API endpoints MUST be tested (contract/integration).
- Frontend components SHOULD be modular and reusable.
- Secrets MUST NOT be hardcoded (use `.env`).

## Change Control

Any change expanding scope beyond Phase 2 or altering architectural principles MUST be preceded by a constitution update.

## Enforcement Clause

1. The constitution takes precedence over all other practices.
2. Conflicts must be reported and resolved consciously.
3. Silent violations are prohibited.

## Success Definition

Phase 2 is successful when:
- A user can sign up, log in, manage tasks, and see them persist.
- The system matches the specification exactly.
- The codebase follows the defined architecture.
- All API and UI requirements are fulfilled.

## Governance

### Amendment Process
1. Propose changes with rationale.
2. Document impact.
3. Update version (Semantic Versioning).
   - MAJOR: Principle removals/redefinitions.
   - MINOR: New sections/expanded guidance.
   - PATCH: Wording/typo fixes.

**Version**: 2.0.0 | **Ratified**: 2025-12-27 | **Last Amended**: 2025-12-31
