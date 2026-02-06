# Implementation Plan: Phase III Part A - MCP Server & Tool Layer

**Branch**: `main` | **Date**: 2026-02-06 | **Spec**: [link](./spec.md)
**Input**: Feature specification from `/specs/Phase-III-todo-ai-chatbot/Part-A-mcp-server-tool-layer/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of an MCP (Model Context Protocol) server that exposes todo operations as stateless, database-backed tools. The system will provide 5 core tools (add_task, list_tasks, update_task, complete_task, delete_task) that operate on Neon PostgreSQL data with user isolation through user_id parameters. This creates the exclusive interface layer between AI agents and the todo management system while maintaining stateless architecture. The MCP server integrates with the existing Phase II Full-Stack Web Application architecture (FastAPI + SQLModel + Neon PostgreSQL + Better Auth) to provide AI agents with standardized access to task operations through the Official MCP SDK.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: FastAPI, SQLModel, Neon PostgreSQL, Anthropic MCP SDK, Better Auth JWT integration
**Storage**: Neon PostgreSQL (via SQLModel ORM) - leveraging existing Phase II database schema with Task entity:
  - `id`: UUID (primary key) - Unique identifier for each task
  - `user_id`: UUID (foreign key) - Links task to authenticated user
  - `title`: String (required) - Task title/description (max 255 chars)
  - `description`: String (optional) - Detailed task description (max 1000 chars)
  - `completed`: Boolean - Completion status (default: false)
  - `created_at`: DateTime - Timestamp of creation
  - `updated_at`: DateTime - Timestamp of last update
  - `priority`: String (optional) - Priority level (enum: low, medium, high)
**Testing**: pytest for unit/integration testing of MCP tools with comprehensive test suite covering:
  - Individual tool functions (add_task, list_tasks, update_task, complete_task, delete_task)
  - Authentication validation layers
  - Database integration and transaction handling
  - Error handling and edge cases
**Target Platform**: Linux server (backend service)
**Project Type**: Web backend service with MCP integration extending Phase II architecture
**Performance Goals**: <2 second response time for 95% of tool executions, support 100 concurrent requests
**Constraints**:
- Stateless operations (MCP server must not maintain conversation state)
- User data isolation via user_id parameters in all MCP tools (validation against JWT token)
- All data persisted to existing Neon PostgreSQL database from Phase II using SQLModel ORM
- MCP tools must be the exclusive interface for AI agents to access task operations
- No server-side conversation caching or session state
- MCP tools must validate JWT tokens from Better Auth and enforce user_id matching
**Scale/Scope**: Support 10k users with isolated data access, building upon existing Phase II infrastructure

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] I. Persistence & State Ownership: Neon PostgreSQL used, backend is source of truth?
- [x] II. Clean Architecture: Domain logic in backend, UI thin?
- [x] V. API-First & Validation: Interaction only via REST, structured errors?
- [x] VII. API-First Architecture: Clear request/response contracts?
- [x] VIII. Separation of Concerns: No business logic in UI?
- [x] IX. Stateless AI Architecture: MCP server remains stateless with conversation context reconstructed per request?
- [x] X. MCP-First AI Design: AI agents interact only through MCP tools, never directly with database?
- [x] XI. Tool-Driven Intelligence: Natural language maps to tool selection with no hidden side effects?
- [x] XII. Safety & Determinism: AI responses deterministic and auditable?

## Project Structure

### Documentation (this feature)

```text
specs/Phase-III-todo-ai-chatbot/Part-A-mcp-server-tool-layer/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (extending Phase II backend structure)

```text
# Web application (Phase 2 Standard extended for Phase 3)
backend/
├── src/
│   ├── models/          # Existing Phase II models (task, user, etc.)
│   ├── services/        # Existing Phase II services, extended for MCP
│   ├── api/             # Existing Phase II REST API, maintained for frontend compatibility
│   └── mcp/             # NEW: MCP Server module for Phase III
│       ├── server.py                # MCP server implementation with tool registration
│       ├── tools/
│       │   ├── __init__.py
│       │   ├── task_operations.py   # Core task operation tools (add_task, list_tasks, etc.)
│       │   └── auth_validation.py   # Authentication validation using Better Auth JWT
│       └── schemas/
│           ├── __init__.py
│           └── task_schemas.py      # MCP-specific schemas for task operations
└── tests/
    └── mcp/              # NEW: MCP-specific tests
        ├── test_server.py
        └── test_tools/
            ├── test_add_task.py
            ├── test_list_tasks.py
            ├── test_update_task.py
            ├── test_complete_task.py
            └── test_delete_task.py
```

**Structure Decision**: Extending the existing Phase II backend structure (FastAPI + SQLModel + Neon PostgreSQL) to include an MCP module that provides the required tools. The MCP module leverages existing database models and authentication mechanisms while providing a new interface specifically designed for AI agent consumption. This maintains consistency with Phase II architecture while enabling Phase III AI functionality. The server will run on localhost:8000/mcp by default, implementing the Model Context Protocol to provide standardized tools (add_task, list_tasks, update_task, complete_task, delete_task) that AI agents can access.

## Phase 0: Research & Exploration

### Step 0.1: MCP SDK Integration Research
**Purpose**: Understand the Anthropic MCP SDK requirements and best practices, and how to integrate with existing Phase II architecture
**What is created or verified**: Research document with MCP SDK usage patterns, tool definition, authentication handling, and integration with FastAPI/SQLModel
**Expected outcome**: Clear understanding of MCP server setup and how to register tools that work with existing database models and authentication system

### Step 0.2: Better Auth JWT Integration with MCP Tools
**Purpose**: Determine how Better Auth JWT tokens from Phase II integrate with MCP tools for user authentication
**What is created or verified**: Authentication flow documentation showing how JWT tokens are validated in MCP tools to ensure user isolation
**Expected outcome**: Clear protocol for extracting user_id from JWT tokens in MCP tools to ensure proper user data isolation

### Step 0.3: Database Integration Patterns
**Purpose**: Define patterns for MCP tools to access existing Phase II database models using SQLModel with proper authentication
**What is created or verified**: Patterns for stateless database operations that maintain ACID properties while ensuring user data isolation
**Expected outcome**: Reliable database access patterns that allow MCP tools to operate on existing task models while enforcing user boundaries

### Step 0.4: Phase II Architecture Assessment
**Purpose**: Review existing Phase II components (database models, services, authentication) to identify reuse opportunities
**What is created or verified**: Assessment of existing FastAPI routes, SQLModel models, and Better Auth integration for potential reuse in MCP tools
**Expected outcome**: Understanding of which Phase II components can be reused and which need adaptation for MCP usage

## Phase 1: Design & Architecture

### Step 1.1: MCP Server Setup
**Purpose**: Create the foundational MCP server structure that integrates with existing Phase II backend
**What is created or verified**: MCP server instance with proper configuration that can coexist with existing FastAPI application
**Expected outcome**: Running MCP server ready to accept tool definitions and integrated with existing deployment infrastructure

### Step 1.2: Task Operation Tool Definitions
**Purpose**: Implement the 5 required MCP tools (add_task, list_tasks, update_task, complete_task, delete_task) that interface with existing Phase II database models
**What is created or verified**: Each tool is defined with proper parameters, return types, and integrates with existing Task model from Phase II:
  - add_task: Accepts user_id (required), title (required), description (optional), priority (optional); returns created task object with all properties
  - list_tasks: Accepts user_id (required) and optional status filter; returns array of task objects for the authenticated user
  - update_task: Accepts user_id (required), task_id (required), and optional fields (title, description, priority, completed); returns updated task object
  - complete_task: Accepts user_id (required), task_id (required), completed (required boolean); returns updated task object
  - delete_task: Accepts user_id (required), task_id (required); returns confirmation object with deleted task ID
**Expected outcome**: 5 functional MCP tools that map to corresponding database operations using existing Phase II data models, with proper authentication validation and error handling

### Step 1.3: Better Auth JWT Validation Layer
**Purpose**: Ensure all MCP tools validate user authentication through Better Auth JWT tokens and enforce user isolation
**What is created or verified**: Authentication validation utilities that extract and verify user_id from JWT tokens consistent with Phase II authentication
**Expected outcome**: Secure tools that prevent cross-user data access by validating JWT tokens and matching user_id to requested operations

### Step 1.4: Database Integration Layer
**Purpose**: Connect MCP tools to existing Neon PostgreSQL database with proper transaction handling using existing SQLModel models from Phase II
**What is created or verified**: Transaction-safe database operations for all tool functions that reuse existing Phase II models and services
**Expected outcome**: All tool operations properly persist to existing database with ACID compliance while maintaining user data isolation

### Step 1.5: Error Handling Framework
**Purpose**: Establish consistent error reporting for MCP tools that provides clear feedback to AI agents
**What is created or verified**: Structured error responses that follow MCP specification and provide actionable feedback to AI agents:
  - All tools return structured error object with error_code (string identifier), message (human-readable description), and optional details
  - Authentication failures return appropriate error codes indicating invalid JWT or user mismatch
  - Database operation failures return structured error responses
  - Validation errors return clear indication of which parameters were invalid
**Expected outcome**: Reliable error handling that maintains tool functionality and provides useful feedback while adhering to MCP protocol standards

### Step 1.6: MCP-REST API Bridge Design
**Purpose**: Design how MCP tools relate to existing Phase II REST API endpoints to maintain consistency
**What is created or verified**: Mapping between MCP tools and existing REST API functionality to ensure consistent behavior
**Expected outcome**: Clear relationship between MCP tools and existing API endpoints so both interfaces behave consistently

## Phase 2: Implementation Preparation

### Step 2.1: Task Generation
**Purpose**: Generate implementation tasks based on the design that integrate with existing Phase II infrastructure
**What is created or verified**: Detailed tasks.md with testable requirements that account for integration with existing Phase II components
**Expected outcome**: Ready-to-execute task list that guides implementation of MCP tools while maintaining compatibility with existing architecture

### Step 2.2: MCP Protocol Contract Definition
**Purpose**: Define formal contracts for MCP tool interfaces according to the Model Context Protocol specification
**What is created or verified**: MCP tool specifications with proper input/output schemas and behavior definitions:
  - Tool specifications with JSON schemas for all parameters and return types
  - Authentication validation requirements for each tool
  - Error response formats and codes
  - MCP protocol compliance for tool registration and invocation
**Expected outcome**: Formal specification of MCP tool interfaces that comply with official MCP protocol for AI agent consumption

### Step 2.3: Integration Testing Strategy
**Purpose**: Plan comprehensive testing approach that validates MCP tools work with existing Phase II components
**What is created or verified**: Testing strategy that covers unit tests for tools, integration tests with existing models, and end-to-end validation
**Expected outcome**: Complete testing approach that ensures MCP tools function correctly with existing authentication and database infrastructure

### Step 2.4: Quickstart Guide Creation
**Purpose**: Document how to run and test the MCP server in the context of existing Phase II application
**What is created or verified**: Comprehensive quickstart guide with setup, integration testing, and validation instructions:
  - Prerequisites: Python 3.11+, Poetry, Neon PostgreSQL access, Better Auth service
  - Installation steps: navigating to backend, installing dependencies with poetry install
  - Environment configuration: setting up DATABASE_URL and AUTH_JWT_SECRET
  - Server startup: running the MCP server via poetry run python src/mcp/server.py
  - Testing procedures: using pytest to run the test suite
  - Manual testing examples: using requests to test MCP endpoints
  - Development guidelines: adding new tools, using auth validation utilities, following existing SQLModel patterns
**Expected outcome**: Clear documentation enabling quick deployment, testing, and validation of MCP tools alongside existing Phase II application