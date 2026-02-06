---
id: 1
title: "Constitution Amendment Phase III Todo AI Chatbot"
stage: "constitution"
date_iso: "2026-02-06"
surface: "agent"
model: "claude-opus-4-5-20251101"
feature: "todo-ai-chatbot"
branch: "main"
user: "user"
command: "/sp.constitution"
labels: ["constitution", "phase-iii", "todo-ai-chatbot", "amendment"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - ".specify/memory/constitution.md"
tests_yaml: []
---

# Constitution Amendment Phase III Todo AI Chatbot

## Summary

Updated the project constitution to incorporate Phase III: Todo AI Chatbot amendments while preserving all existing principles from Phase II. Added new principles for stateless AI architecture, MCP-first AI design, tool-driven intelligence, and safety & determinism.

## Prompt Text

```
# Constitution Amendment — Phase III: Todo AI Chatbot

## Amendment Purpose

This amendment extends the project constitution from Phase II (Full-Stack Web Application)
to Phase III (Todo AI Chatbot).

Phase III introduces an AI-powered conversational interface while **preserving all architectural,
security, and persistence guarantees established in Phase II**.

This amendment is binding and must be strictly followed by all agents, specs, plans, and task generations.

---

## Immutable Principles (Carry Forward)

The following principles from Phase II remain **unchanged and mandatory**:

1. **Spec-Driven Development Only**
   - Workflow is strictly: `spec.md → plan.md → task.md → implementation`
   - No manual coding
   - No speculative features outside the spec

2. **Separation of Concerns**
   - `/frontend`, `/backend`, `/specs` remain isolated
   - AI logic must NOT leak into frontend UI code
   - MCP tools must NOT contain business UI logic

3. **Persistent Storage is Mandatory**
   - All state must be stored in **Neon Serverless PostgreSQL**
   - No in-memory adapters
   - No volatile server state

4. **Authentication is Mandatory**
   - Better Auth remains the single source of truth
   - JWT verification is required for all AI chat requests
   - AI agents must act strictly on behalf of the authenticated user

---

## New Principles Introduced in Phase III

### 1. Stateless AI Architecture (Hard Rule)

- The FastAPI server must remain **stateless**
- Conversation context must be reconstructed **per request** from the database
- No server-side memory, cache, or session storage

### 2. MCP-First AI Design

- AI agents may **only interact with the system through MCP tools**
- MCP tools are the **exclusive interface** to task operations
- The agent must never call database logic directly

### 3. Tool-Driven Intelligence

- Natural language understanding → tool selection → confirmation response
- No hidden side effects
- Every task mutation must correspond to an explicit MCP tool call

### 4. Safety & Determinism

- AI responses must be:
  - Deterministic where possible
  - Auditable via stored messages + tool calls
- Silent failures are forbidden

---

## Completion Standard

Phase III is considered complete **only when**:

- All todo operations
```

## Response Text

Updated the constitution file at `.specify/memory/constitution.md` to include the new Phase III AI Chatbot principles while maintaining all existing Phase II principles. The updated constitution now includes:

1. All immutable principles from Phase II carried forward
2. Four new principles for Phase III:
   - IX. Stateless AI Architecture (Hard Rule)
   - X. MCP-First AI Design
   - XI. Tool-Driven Intelligence
   - XII. Safety & Determinism
3. Updated scope boundaries to include AI chatbot functionality
4. Updated functional guarantees to include AI chatbot operations
5. Updated interaction rules to specify MCP tool usage for AI
6. Updated UX standards to include AI chatbot interface considerations
7. Updated quality standards to address AI-specific requirements
8. Version incremented from 2.0.0 to 3.0.0 to reflect the significant addition of AI principles

The constitution now serves as the authoritative guide for implementing the Todo AI Chatbot phase while preserving all architectural, security, and persistence guarantees from Phase II.

## Outcome

The constitution has been successfully updated and saved to `.specify/memory/constitution.md`. It now reflects the requirements for Phase III: Todo AI Chatbot with all necessary principles and guidelines while maintaining backward compatibility with existing functionality.