---
id: 002
title: Generate Implementation Plan Chat UI Integration
stage: plan
date: 2026-02-12
surface: agent
model: Claude Opus 4.6 (1M context)
feature: Part-C-chat-ui-integration
branch: main
user: HCI
command: /sp.plan
labels: ["phase-3", "chat-ui", "planning", "architecture"]
links:
  spec: specs/Phase-III-todo-ai-chatbot/Part-C-chat-ui-integration/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/Phase-III-todo-ai-chatbot/Part-C-chat-ui-integration/plan.md
  - specs/Phase-III-todo-ai-chatbot/Part-C-chat-ui-integration/research.md
  - specs/Phase-III-todo-ai-chatbot/Part-C-chat-ui-integration/data-model.md
  - specs/Phase-III-todo-ai-chatbot/Part-C-chat-ui-integration/contracts/chat-endpoint.json
  - specs/Phase-III-todo-ai-chatbot/Part-C-chat-ui-integration/contracts/conversation-history-endpoint.json
  - specs/Phase-III-todo-ai-chatbot/Part-C-chat-ui-integration/quickstart.md
tests:
  - Constitution check validation (all 12 principles passed)
  - Research questions resolved (5 areas investigated)
  - Data model design validated (2 entities, relationships, indexes)
  - API contracts generated (OpenAPI 3.0 specifications)
---

## Prompt

```text
# Prompt: Generate plan.md for Phase III — Part C: Chat UI & Integration

You are generating **plan.md** based strictly on the approved `spec.md` for
**Phase III — Part C: Chat UI & End-to-End Integration**.

---

## Context (Locked)

- MCP Server & Tools are COMPLETE
- AI Agent & Orchestration are COMPLETE
- Frontend uses Next.js
- Authentication uses Better Auth + JWT

---

## Objective of This Plan

Produce a plan to:

- Integrate a chat UI with the AI agent
- Secure chat requests with JWT
- Persist conversations and messages
- Verify full end-to-end behavior

---

## Plan Rules (Must Follow)

- Scope is **integration and verification only**
- No new task features
- No backend redesign
- No auth model changes
- No speculative UX features

---

## Must Remember (Critical)

- Chat endpoint must be authenticated
- Backend remains stateless
- All messages must persist in Neon PostgreSQL
- AI actions must route through MCP tools

---

Generate `plan.md`.
```

## Response snapshot

Generated complete implementation plan for Phase III Part C: Chat UI & End-to-End Integration with all required phases and artifacts.

**Plan Structure Created**:

1. **Main Plan Document** (`plan.md`):
   - Summary and technical context
   - Constitution check (all 12 principles validated ✅)
   - Project structure (documentation and source code)
   - Phase 0: Research & Technology Validation
   - Phase 1: Design & Contracts
   - Phase 2: Task Generation (to be executed by /sp.tasks)
   - Risk assessment and success metrics
   - Dependencies and next steps

2. **Phase 0: Research Document** (`research.md`):
   - 5 research areas investigated:
     - OpenAI ChatKit integration with Next.js → Decision: Use ChatKit with client components
     - JWT token management → Decision: Better Auth + Axios interceptor
     - Conversation persistence patterns → Decision: Two-table schema with indexes
     - Real-time UI updates → Decision: Optimistic updates + loading states
     - Chat-specific error handling → Decision: Tiered strategy with user-friendly messages
   - All decisions documented with rationale, alternatives considered, and implementation notes

3. **Phase 1: Data Model** (`data-model.md`):
   - 2 entities defined: Conversation, Message
   - Complete SQLModel definitions with relationships
   - 5 query patterns documented with performance characteristics
   - Migration script for database schema
   - Indexes: Primary keys, foreign keys, composite index on (conversation_id, timestamp)
   - Data integrity constraints and security considerations

4. **Phase 1: API Contracts**:
   - `contracts/chat-endpoint.json`: OpenAPI 3.0 spec for POST /api/{user_id}/chat
     - Request/response schemas
     - 6 error codes (AUTH_FAILED, UNAUTHORIZED, RATE_LIMIT, INVALID_INPUT, AI_ERROR, DATABASE_ERROR)
     - 3 example scenarios (new conversation, existing conversation, confirmation)
   - `contracts/conversation-history-endpoint.json`: OpenAPI 3.0 spec for GET /api/{user_id}/conversations/{conversation_id}/messages
     - Pagination support (limit, offset)
     - 3 example responses (with messages, paginated, empty)

5. **Phase 1: Quickstart Guide** (`quickstart.md`):
   - 7-step setup process: Prerequisites, Database Migration, Install Dependencies, Environment Config, Start System, Manual Testing, Automated Testing
   - 6 manual test cases covering authentication, message sending, persistence, error handling, responsive design
   - Performance verification procedures
   - Troubleshooting guide for 5 common issues
   - Verification checklist (functionality, performance, UX, security)

**Technical Decisions**:
- Language: Python 3.11+ (backend), TypeScript (frontend with Next.js 16+)
- Dependencies: FastAPI, SQLModel, OpenAI ChatKit, Better Auth
- Storage: Neon PostgreSQL with two-table schema (conversations, messages)
- Performance targets: <3s response time, <2s history load, 100 concurrent sessions
- Architecture: Stateless server, per-request context reconstruction

**Constitution Compliance**: ✅ All 12 principles validated
- Persistence & State Ownership ✅
- Clean Architecture ✅
- API-First & Validation ✅
- Stateless AI Architecture ✅
- MCP-First AI Design ✅
- Tool-Driven Intelligence ✅
- Safety & Determinism ✅
- Web UX Standards ✅

**Risk Assessment**:
- 3 technical risks identified (ChatKit compatibility, performance under load, token expiration)
- 2 integration risks (AI agent response time, database schema changes)
- 2 UX risks (interface usability, error message clarity)
- All risks have mitigation strategies

## Outcome

- ✅ Impact: Complete implementation plan created with research, data model, API contracts, and quickstart guide ready for task generation
- 🧪 Tests: Constitution check passed (12/12 principles), research validated (5 areas), data model validated (2 entities, indexes, relationships)
- 📁 Files: 6 files created (plan.md, research.md, data-model.md, 2 contract files, quickstart.md)
- 🔁 Next prompts: `/sp.tasks` to generate detailed task list in tasks.md
- 🧠 Reflection: Planning phase complete with all Phase 0 and Phase 1 artifacts generated. Architecture follows established patterns from Parts A and B. No constitution violations. Ready for task generation and implementation.

## Evaluation notes (flywheel)

- Failure modes observed: PowerShell script unavailable (pwsh not found) - agent context update skipped but not blocking
- Graders run and results (PASS/FAIL): Constitution Check - PASS (12/12), Research Completeness - PASS (5/5 areas), Data Model Validation - PASS (entities, relationships, indexes defined), API Contracts - PASS (OpenAPI 3.0 compliant)
- Prompt variant (if applicable): Standard /sp.plan workflow with detailed feature requirements
- Next experiment (smallest change to try): Execute /sp.tasks to generate dependency-ordered task list from plan artifacts
