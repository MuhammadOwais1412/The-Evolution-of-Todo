# Research: Frontend Application with Better Auth

**Feature**: 003-frontend-better-auth
**Date**: 2026-01-03
**Phase**: Phase 0 - Technical Research

## Overview

This document consolidates research findings for implementing the frontend application with Next.js 16+, Better Auth, and REST API integration. All research aligns with the spec requirements, constitution principles, and backend API contracts.

---

## Technology Decisions

### 1. Next.js Framework

**Decision**: Next.js 16+ with App Router

**Rationale**:
- Next.js 16+ provides the latest App Router with built-in optimizations (Server Components, streaming, SEO)
- App Router simplifies route organization and nested layouts
- Strong TypeScript support out of the box
- Mature ecosystem with excellent developer experience
- Matches the requirement for modern, production-ready frontend

**Alternatives Considered**:
- Remix: Excellent data loading but steeper learning curve
- Vite + React Router: More control but requires more manual setup
- Nuxt.js: Vue-based, not matching React ecosystem

**Selected**: Next.js 16+ App Router

---

### 2. Authentication: Better Auth

**Decision**: Better Auth for JWT-based authentication

**Rationale**:
- Better Auth is a modern, lightweight authentication solution designed for Next.js
- Supports JWT token issuance with configurable expiration
- Provides server-side and client-side utilities for session management
- Can be configured to issue JWT tokens that match backend expectations
- Includes signup, signin, logout, and session persistence out of the box
- Minimal boilerplate compared to custom auth implementations

**JWT Configuration**:
- Better Auth will be configured to issue JWT tokens with `sub` claim containing user_id
- Tokens will be stored in secure HTTP-only cookies or localStorage (depending on Better Auth configuration)
- Backend expects JWT in `Authorization: Bearer <token>` header
- Better Auth client-side utilities will automatically extract and attach tokens

**Alternatives Considered**:
- NextAuth.js (Auth.js): More complex setup, heavier dependency
- Supabase Auth: Vendor lock-in, overkill for this use case
- Custom JWT implementation: Would require more boilerplate and security considerations

**Selected**: Better Auth with JWT token configuration

---

### 3. State Management

**Decision**: React Context API + React Hooks (minimal complexity)

**Rationale**:
- React Context is built into React and requires no additional dependencies
- Sufficient for the limited state needs: auth session, task list, loading/error states
- Backend is the source of truth (constitution compliance), so frontend state is purely transient
- Avoids over-engineering with Redux Toolkit or Zustand for a simple todo app
- Easier for junior developers to understand and maintain

**State Breakdown**:
- AuthContext: Stores JWT token and user session from Better Auth
- TaskContext: Manages transient task list state (cached from backend)
- Individual components: Manage their own UI state (forms, modals, etc.)

**Alternatives Considered**:
- Zustand: Lightweight but adds dependency; Context is sufficient
- Redux Toolkit: Overkill for this scope; adds significant boilerplate
- React Query (TanStack Query): Good for caching but adds complexity; can be added later if needed

**Selected**: React Context API + React Hooks

---

### 4. UI Framework: Tailwind CSS

**Decision**: Tailwind CSS for styling

**Rationale**:
- Tailwind CSS is industry-standard for modern React applications
- Provides rapid UI development with utility classes
- Excellent responsive design support (mobile-first)
- Smaller bundle size with JIT mode in Next.js 16+
- Easy to create professional, consistent designs
- No CSS files to manage (CSS-in-JS via utility classes)

**UI Component Approach**: Use shadcn/ui (optional, minimal components)
- shadcn/ui provides high-quality, accessible components built with Radix UI
- Components are copied into the codebase (not npm package), so full control
- Start with custom Tailwind classes, use shadcn/ui for complex components (modals, dialogs) if needed

**Alternatives Considered**:
- CSS Modules: More boilerplate, less flexible than Tailwind
- Styled Components: Runtime overhead, larger bundle size
- Material UI / MUI: Heavier, more opinionated design system

**Selected**: Tailwind CSS (with optional shadcn/ui for complex components)

---

### 5. API Client Implementation

**Decision**: Custom lightweight fetch wrapper with JWT injection

**Rationale**:
- Backend has RESTful endpoints with JWT authentication
- Need a client that:
  - Attaches JWT token to all requests via `Authorization: Bearer <token>` header
  - Handles common error responses (401 unauthorized, 404, 500)
  - Provides TypeScript types for requests/responses
  - Supports loading/error states for UI integration
- Custom wrapper is simpler than axios or fetch wrappers
- Full control over error handling and token management

**Implementation Strategy**:
- Create `src/lib/api-client.ts` with typed API functions
- Extract JWT token from Better Auth session
- Auto-inject `Authorization` header for all requests
- Handle 401 errors (redirect to login)
- Return typed responses matching backend Pydantic models

**Alternatives Considered**:
- axios: Popular but larger dependency
- ky: Lightweight but additional dependency
- React Query: Good for caching but adds complexity for first implementation

**Selected**: Custom fetch wrapper with JWT injection

---

## Integration Patterns

### Better Auth + Backend JWT Alignment

**Challenge**: Backend expects JWT with specific structure (HS256, `sub` claim with user_id)

**Solution**:
1. Configure Better Auth to issue JWT tokens matching backend expectations
2. Use Better Auth's JWT plugin or custom token generation
3. Share `BETTER_AUTH_SECRET` between frontend and backend via environment variables
4. Backend already validates JWTs using this secret (see `backend/src/config.py`)
5. Frontend Better Auth will store token and make it available to API client

**Token Flow**:
1. User signs up/logs in via Better Auth
2. Better Auth issues JWT token with `sub: user_id`
3. Token stored in cookie or localStorage
4. API client extracts token from Better Auth session
5. All API requests include `Authorization: Bearer <token>`
6. Backend validates token and extracts `sub` as `user_id`
7. User isolation enforced by matching `user_id` from JWT with URL path

---

### Error Handling Strategy

**Frontend Error Handling**:
- Network errors: Show retry option, check connection
- 401 Unauthorized: Redirect to login, clear session
- 404 Not Found: Show "not found" message (e.g., task doesn't exist)
- 422 Validation Error: Show field-level validation messages
- 500 Server Error: Show "something went wrong" message, suggest retry

**Loading States**:
- Show spinner/skeleton during API calls
- Disable buttons/actions during async operations
- Provide feedback for long-running operations (timeout after 5s)

---

### Responsive Design Approach

**Mobile-First Strategy**:
- Base styles for mobile (320px+)
- Use Tailwind breakpoints: `md:`, `lg:`, `xl:`
- Touch-friendly targets (min 44x44px)
- Vertical layout for mobile tasks
- Horizontal cards for desktop tasks

**Viewport Breakpoints**:
- Mobile: <768px (default styles)
- Tablet: 768px-1024px (md: prefix)
- Desktop: >1024px (lg: prefix)

---

## Risk Analysis

| Risk | Impact | Mitigation |
|------|--------|------------|
| Better Auth JWT configuration mismatch with backend | HIGH | Share secret via environment variables; test token format with backend early |
| Token expiration during user session | MEDIUM | Better Auth handles refresh; API client catches 401 and redirects to login |
| CORS issues between frontend and backend | MEDIUM | Backend already has CORS middleware configured (allow_origins: "*") |
| State sync issues between frontend and backend | LOW | Backend is source of truth; fetch fresh data on every page load |
| Over-engineering state management | MEDIUM | Use React Context only; avoid Redux/Zustand unless explicitly needed |

---

## Summary

All technical decisions align with:
- **Spec requirements**: Next.js 16+, Better Auth, REST API, responsive UI
- **Constitution principles**: Backend source of truth, thin UI, API-first, separation of concerns
- **Backend contracts**: JWT tokens with `sub` claim, REST endpoints, user isolation via user_id

**Key Takeaways**:
1. Use Next.js 16+ App Router for modern React framework
2. Configure Better Auth to issue JWT tokens matching backend expectations
3. Use React Context for minimal state management (auth, tasks)
4. Use Tailwind CSS for styling with shadcn/ui for complex components (optional)
5. Build custom API client with JWT injection for REST communication
6. Implement responsive mobile-first design with Tailwind breakpoints

No blockers or clarifications needed. Ready for Phase 1 design (data model, API contracts, quickstart).
