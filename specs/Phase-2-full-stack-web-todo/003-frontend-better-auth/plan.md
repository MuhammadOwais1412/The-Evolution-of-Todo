# Implementation Plan: Frontend Application with Better Auth

**Branch**: `003-frontend-better-auth` | **Date**: 2026-01-03 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-frontend-better-auth/spec.md`

## Summary

Implement a Next.js 16+ frontend application using App Router for a multi-user todo application. The frontend must use Better Auth for JWT-based authentication (signup/signin), communicate with an existing FastAPI backend via REST API, and provide a responsive, professional UI for task management (CRUD + completion). Backend is complete and stable; no modifications allowed. Frontend must live strictly in `Phase-2-web-todo/frontend/`.

## Technical Context

**Language/Version**: TypeScript 5+, Next.js 16+ with App Router
**Primary Dependencies**: Next.js, React 19+, Better Auth, Tailwind CSS (or shadcn/ui), zustand or React Context (state)
**Storage**: N/A (backend manages state in Neon PostgreSQL)
**Testing**: Jest + React Testing Library, Playwright for E2E
**Target Platform**: Web browsers (modern: Chrome, Firefox, Safari, Edge), responsive (mobile 320px+ to desktop)
**Project Type**: web (frontend of full-stack application)
**Performance Goals**: <2s page load, <100ms UI interaction response, <500ms API roundtrip
**Constraints**: JWT must be attached to all API requests, no backend modifications, stateless UI (backend is source of truth)
**Scale/Scope**: 10k users max, ~5 pages/routes, minimal UI complexity

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] I. Persistence & State Ownership: Neon PostgreSQL used, backend is source of truth?
  - **YES**: Frontend will use backend API as source of truth; no local database or state source-of-truth for domain data
- [x] II. Clean Architecture: Domain logic in backend, UI thin?
  - **YES**: Frontend components will only handle rendering and API calls; all validation and business logic is in backend
- [x] V. API-First & Validation: Interaction only via REST, structured errors?
  - **YES**: All data communication via REST API; backend validates inputs and returns structured errors
- [x] VII. API-First Architecture: Clear request/response contracts?
  - **YES**: Will document API contracts in Phase 1; backend endpoints already defined
- [x] VIII. Separation of Concerns: No business logic in UI?
  - **YES**: UI will delegate to backend API for all operations
- [x] Web UX Standards: Responsive, loading/error states handled?
  - **YES**: Will implement responsive design with loading/error states for all API interactions

## Project Structure

### Documentation (this feature)

```text
specs/003-frontend-better-auth/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
Phase-2-web-todo/frontend/
├── src/
│   ├── app/                    # Next.js App Router
│   │   ├── (auth)/            # Auth route group
│   │   │   ├── login/         # Login page
│   │   │   └── signup/        # Signup page
│   │   ├── (dashboard)/       # Protected route group
│   │   │   └── tasks/         # Task dashboard
│   │   ├── layout.tsx         # Root layout
│   │   └── page.tsx           # Landing/home page
│   ├── components/            # React components
│   │   ├── auth/              # Auth components
│   │   └── tasks/             # Task components
│   ├── lib/                   # Utilities and clients
│   │   └── api-client.ts      # REST API client with JWT handling
│   ├── services/              # Business logic wrappers
│   │   └── auth.service.ts    # Better Auth integration
│   └── types/                 # TypeScript types
│       └── api.ts             # API request/response types
├── public/                    # Static assets
├── package.json
├── tsconfig.json
├── next.config.js
└── .env                       # Environment variables
```

**Structure Decision**: Following standard Next.js 16+ App Router structure with route groups for logical separation. Auth pages in `(auth)` group, protected dashboard in `(dashboard)` group. State management via React hooks/Context or Zustand (minimal complexity). No complex module systems or abstraction layers.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | N/A | No constitution violations; design follows all principles |
