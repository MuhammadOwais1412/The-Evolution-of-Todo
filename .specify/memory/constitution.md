<!--
Sync Impact Report:
- Version change: 2.0.0 → 3.0.0
- Modified principles: Added new principles for Phase III AI Chatbot (Stateless AI Architecture, MCP-First AI Design, Tool-Driven Intelligence, Safety & Determinism)
- Added sections: Principles IX-XII for AI Chatbot functionality
- Templates status:
  * ⚠ spec-template.md - Needs alignment with Phase 3 scope
  * ⚠ plan-template.md - Needs structure update for AI components
  * ⚠ tasks-template.md - Needs update for AI phases
- Follow-up TODOs: Manual update of templates to reflect AI chatbot structure.
-->

# Todo AI Chatbot Constitution

## Core Principles

### I. Persistence & State Ownership
The system MUST use persistent storage (Neon Serverless PostgreSQL via SQLModel). The backend is the sole owner of system state and the "source of truth." The frontend MUST NOT maintain a separate source-of-truth for domain data.

Rationale: Ensures data durability across sessions and maintains a single, reliable state repository.

### II. Clean Architecture
The system MUST adhere to Single Responsibility Principle, clear separation of concerns, and deterministic behavior. Logic MUST be layered: Domain logic in the backend, rendering and interaction logic in the frontend, AI intelligence through MCP tools only.

Rationale: Prevents business logic leakage, ensures testability, and maintains a manageable codebase as complexity grows.

### III. No Global Mutable State
Global mutable state is strictly prohibited. State ownership must be explicit (e.g., React context or state management for UI, backend services for domain, conversation context reconstructed per request for AI). No hardcoded magic values.

Rationale: Maintains predictability and prevents side-effect-driven bugs in a distributed system (frontend/backend/AI).

### IV. Spec-Driven Development (NON-NEGOTIABLE)
All development MUST follow: Specification → Plan → Tasks → Implementation. No coding without approved specs. The constitution overrides plans and tasks on conflict.

Rationale: Maintains traceability and prevents scope creep or architectural drift.

### V. API-First & Validation
Communication between frontend and backend MUST occur ONLY via structured REST APIs. Every operation MUST validate inputs at the system boundary (API endpoints). Errors MUST be explicit, structured, and actionable.

Rationale: Decouples components and ensures system integrity against malformed or malicious input.

### VI. Smallest Viable Change
Changes must be minimal, reversible, and traceable to requirements. No speculative features or premature abstractions for "Phase 4+."

Rationale: Focuses effort on current objectives and reduces cognitive load.

### VII. API-First Architecture
The backend is the system of record. The frontend communicates with the backend ONLY via the defined REST API. Request/response contracts MUST be clear and documented.

Rationale: Enables independent evolution of frontend and backend while maintaining a stable interface.

### VIII. Separation of Concerns
Backend handles domain logic, validation, and persistence. Frontend handles rendering, user interaction, and API calls. AI agents handle natural language understanding through MCP tools only. Business logic MUST NOT leak into UI components or AI agents directly interacting with databases.

Rationale: Keeps the UI "thin", AI agents "tool-driven", and the backend "authoritative," simplifying debugging and future changes.

### IX. Stateless AI Architecture (Hard Rule)
The FastAPI server hosting AI agents MUST remain stateless. Conversation context MUST be reconstructed per request from the database. No server-side memory, cache, or session storage for AI conversations is allowed.

Rationale: Ensures scalability and reliability of AI services without server-side state dependencies that could cause inconsistencies or failures.

### X. MCP-First AI Design
AI agents MAY ONLY interact with the system through MCP tools. MCP tools are the EXCLUSIVE interface to task operations. The agent MUST NEVER call database logic directly or bypass the MCP tool layer for any business operations.

Rationale: Maintains a single, auditable path for all system modifications and ensures AI actions follow the same validated pathways as other system components.

### XI. Tool-Driven Intelligence
Natural language understanding MUST map to tool selection, followed by confirmation responses. No hidden side effects are allowed. Every task mutation MUST correspond to an explicit MCP tool call visible in the conversation history and audit trail.

Rationale: Ensures transparency and auditability of AI actions, allowing for deterministic reproduction of system states from conversation logs and tool calls.

### XII. Safety & Determinism
AI responses MUST be deterministic where possible and auditable via stored messages and tool calls. Silent failures are forbidden - all operations MUST return explicit success or failure states to maintain system integrity and debuggability.

Rationale: Ensures the system remains predictable and debuggable even with AI components that might otherwise introduce non-deterministic behavior.

## Scope Boundaries (Phase 3)

### In Scope
- Web UI (Next.js 16+ App Router)
- REST APIs (FastAPI)
- Database persistence (Neon PostgreSQL)
- Authentication/Authorization (Better Auth)
- Multi-user support
- Environment-based configuration
- CRUD operations exposed via UI and API
- AI-powered conversational interface for todo management
- MCP-first AI tool integration
- Conversation history stored and retrievable
- AI acting strictly on behalf of authenticated users

### Out of Scope
- Scalability beyond 10k users
- Cloud native complex architectures (Kubernetes, Kafka)
- Mobile applications (Native)
- Advanced real-time collaborative editing (except simple polling/refresh)
- Direct database access from AI agents
- Client-side AI processing

## Functional Guarantees

The application MUST support:
- Secure user signup and signin
- Personalised task lists (multi-user)
- Full CRUD functionality for tasks via both UI and AI chatbot
- Persistent state across browser refreshes
- Responsive web design
- Natural language interaction with todos through AI chatbot
- Conversation history reconstruction from database
- Proper authentication verification for all AI chat requests

## Frontend–Backend Interaction Rules

- All data fetching from the frontend MUST use the backend API.
- Frontend MUST handle loading, error, and empty states for all API interactions.
- Backend MUST return standard HTTP status codes and structured JSON error bodies.
- Authentication tokens (JWT) MUST be managed securely by Better Auth.
- AI agents MUST operate through MCP tools and NOT make direct database calls.
- Conversation context MUST be reconstructed from database per AI request for stateless architecture compliance.

## Web UX Standards

The web interface MUST:
- Be responsive (work on mobile/tablet/desktop).
- Provide immediate visual feedback for user actions (optimistic updates or loading states).
- Use clear, professional typography and spacing.
- Handle error states gracefully with user-friendly messages.
- Ensure task completion toggles are visually distinct and immediate.
- Display AI chatbot interactions clearly with tool confirmation and execution results visible to the user.

## Quality Standards

- Code MUST be readable by a junior developer.
- All API endpoints MUST be tested (contract/integration).
- Frontend components SHOULD be modular and reusable.
- AI interactions MUST follow MCP tool architecture and be auditable.
- Secrets MUST NOT be hardcoded (use `.env`).
- AI responses MUST be deterministic where possible and safe from harmful content generation.

## Change Control

Any change expanding scope beyond Phase 3 or altering architectural principles MUST be preceded by a constitution update.

## Enforcement Clause

1. The constitution takes precedence over all other practices.
2. Conflicts must be reported and resolved consciously.
3. Silent violations are prohibited.

## Success Definition

Phase 3 is successful when:
- A user can sign up, log in, manage tasks, and see them persist via both UI and AI chatbot.
- The AI chatbot properly integrates with MCP tools for all todo operations while maintaining stateless architecture.
- The system matches the specification exactly including AI chatbot functionality.
- The codebase follows the defined architecture with AI agents operating only through MCP tools.
- All API, UI, and AI requirements are fulfilled with proper authentication verification for AI requests.
- Conversation history is properly stored and reconstructible from the database.

## Governance

### Amendment Process
1. Propose changes with rationale.
2. Document impact.
3. Update version (Semantic Versioning).
   - MAJOR: Principle removals/redefinitions.
   - MINOR: New sections/expanded guidance.
   - PATCH: Wording/typo fixes.

**Version**: 3.0.0 | **Ratified**: 2025-12-27 | **Last Amended**: 2026-02-06