---
name: backend-development
description: Design and implement robust, production-grade backend systems with clean architecture, strong correctness guarantees, and long-term maintainability. Use this skill when building APIs, services, business logic, data pipelines, authentication systems, or backend-heavy applications.
version: "1.0.0"
---

This skill guides the creation of **high-quality backend systems** that prioritize **correctness, clarity, scalability, and maintainability** over shortcuts or fragile implementations.

The focus is on **real, working backend code** with disciplined structure, explicit boundaries, and well-defined responsibilities—avoiding "AI slop" such as bloated abstractions, leaky layers, or undocumented magic behavior.

The user provides backend requirements such as APIs, services, data models, workflows, integrations, or system constraints.

---

## Backend Design Thinking

Before writing code, deeply understand the system context and commit to a **clear architectural direction**:

- **Purpose**: What problem does the backend solve? Who depends on it (users, services, clients)?
- **Domain**: What are the core business concepts? What must always be correct?
- **Boundaries**: What belongs in the backend vs elsewhere?
- **Constraints**: Performance, scalability, security, data integrity, deployment environment.
- **Failure Modes**: What can go wrong, and how should the system behave?

**CRITICAL**: Backend quality is defined by predictability and correctness, not cleverness. Simple, explicit systems outperform complex, implicit ones.

---

## Architectural Principles

Implement backend systems that are:

- **Deterministic**: Same inputs → same outputs
- **Observable**: Errors are visible, debuggable, and logged
- **Testable**: Core logic is isolated and verifiable
- **Composable**: Components can evolve independently
- **Defensive**: Invalid input is handled gracefully

Prefer:
- Explicit data flow
- Clear contracts between layers
- Stateless services where possible

Avoid:
- Hidden global state
- God objects or god services
- Over-abstraction and premature optimization
- Tight coupling between infrastructure and business logic

---

## Backend Structure Guidelines

Organize code around **responsibilities**, not frameworks:
Frameworks are tools—not the architecture.

---

## Data & State Management

- Clearly define data models and invariants
- Validate input at system boundaries
- Keep business rules out of controllers/routers
- Separate persistence logic from domain logic
- Prefer immutability where reasonable

Data integrity is **non-negotiable**.

---

## Error Handling & Reliability

Backend systems must fail **loudly, clearly, and safely**:

- Use structured error types
- Never swallow exceptions silently
- Provide actionable error messages
- Differentiate between:
  - User errors
  - System errors
  - Infrastructure failures

Log with intent. Errors should tell a story.

---

## Security & Safety

Always assume:
- Input is untrusted
- Dependencies may fail
- Clients may behave incorrectly

Apply:
- Input validation
- Authentication & authorization boundaries
- Principle of least privilege
- Explicit permission checks

Security is part of design—not an afterthought.

---

## Performance & Scalability

Design for:
- Reasonable defaults first
- Measurable bottlenecks, not hypothetical ones
- Horizontal scalability where applicable

Avoid premature optimization—but never ignore obvious inefficiencies.

---

## Development Workflow Expectations

- Start from a **clear specification**
- Define contracts before implementation
- Implement incrementally
- Verify behavior continuously
- Refactor deliberately, not constantly

Specs drive code—not the other way around.

---

## Code Quality Standards

Backend code must be:

- Readable without explanation
- Explicit rather than clever
- Consistent in naming and structure
- Documented where intent is non-obvious

If future-you cannot understand it in 6 months, it is not done.

---

## Success Criteria

A backend implementation is successful when:

- The system behaves exactly as specified
- Core logic is easy to reason about
- Failures are predictable and diagnosable
- The codebase is safe to extend
- No part of the system feels "fragile"

---

## Philosophy

Backend engineering is about **trust**.

Clients trust the backend to:
- Be correct
- Be stable
- Protect data
- Fail responsibly

This skill enforces discipline, precision, and long-term thinking—over speed or flash.

Build systems that last.
