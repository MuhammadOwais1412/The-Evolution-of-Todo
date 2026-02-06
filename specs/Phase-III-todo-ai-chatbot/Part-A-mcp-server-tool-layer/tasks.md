# Implementation Tasks: Phase III Part A - MCP Server & Tool Layer

## Feature Overview
This document contains implementation tasks for the MCP (Model Context Protocol) server that exposes todo operations as stateless, database-backed tools. The system provides 5 core tools (add_task, list_tasks, update_task, complete_task, delete_task) that operate on Neon PostgreSQL data with user isolation through user_id parameters. This creates the exclusive interface layer between AI agents and the todo management system while maintaining stateless architecture.

**Priority Order**: All tasks should be completed in sequential order within each phase. User stories follow priority sequence from the specification.

## Dependencies
- Phase II Full-Stack Web Application components (FastAPI + SQLModel + Neon PostgreSQL + Better Auth)
- Anthropic MCP SDK installation and configuration
- Neon PostgreSQL database connection
- Better Auth authentication service

## Implementation Strategy
- MVP approach: Implement one tool at a time, starting with add_task
- Incremental delivery: Each user story builds upon previous functionality
- Test-driven development: Implement tests alongside each tool
- Follow existing Phase II patterns for consistency

## Phase 1: Setup Tasks (Project Initialization)

- [X] T001 Create MCP directory structure in backend/src/mcp with subdirectories (server.py, tools/, schemas/)
- [X] T002 Add MCP SDK dependency to backend/pyproject.toml and run poetry install
- [X] T003 Set up environment variables in backend/.env for MCP server configuration
- [X] T004 Create basic MCP server skeleton in backend/src/mcp/server.py with placeholder imports
- [X] T005 [P] Create empty module files in backend/src/mcp/tools/__init__.py
- [X] T006 [P] Create empty module files in backend/src/mcp/schemas/__init__.py

## Phase 2: Foundational Tasks (Blocking Prerequisites)

- [X] T010 Implement JWT validation utilities in backend/src/mcp/tools/auth_validation.py
- [X] T011 Create MCP-specific task schemas in backend/src/mcp/schemas/task_schemas.py
- [X] T012 Verify existing Task model from Phase II is accessible for MCP tools
- [X] T013 Create base error response structure in backend/src/mcp/schemas/task_schemas.py
- [X] T014 [P] Create test directory structure backend/tests/mcp/ with subdirs

## Phase 3: [US1] Implement Core Task Operations (User Story 1 - Add Task)

**Goal**: As an authenticated user, I want to add tasks through AI chatbot using MCP tools so that I can leverage conversational interface for task creation.

**Independent Test Criteria**:
- User can successfully add a task using the add_task MCP tool
- Task is persisted to the database with correct user association
- Authentication is validated properly
- Tool returns structured response with created task details

- [X] T020 [US1] Create add_task function in backend/src/mcp/tools/task_operations.py with proper parameters
- [X] T021 [US1] Implement user_id validation in add_task using JWT validation utilities
- [X] T022 [US1] Implement database persistence logic for new tasks using SQLModel
- [X] T023 [US1] Add proper validation for task title and other parameters in add_task
- [X] T024 [US1] Implement success response formatting for add_task
- [X] T025 [US1] Implement error handling for add_task with structured responses
- [X] T026 [P] [US1] Write unit tests for add_task in backend/tests/mcp/test_tools/test_add_task.py
- [X] T027 [P] [US1] Test user isolation enforcement in add_task with different user contexts
- [X] T028 [US1] Register add_task with MCP server in backend/src/mcp/server.py

## Phase 4: [US2] Implement Task Listing (User Story 2 - List Tasks)

**Goal**: As an authenticated user, I want to list my tasks exclusively (no other users' tasks visible) so that I can see only my own tasks.

**Independent Test Criteria**:
- User can successfully list their own tasks using the list_tasks MCP tool
- Only tasks belonging to the authenticated user are returned
- Authentication is validated properly
- Tool returns structured response with task array

- [X] T030 [US2] Create list_tasks function in backend/src/mcp/tools/task_operations.py with proper parameters
- [X] T031 [US2] Implement user_id validation in list_tasks using JWT validation utilities
- [X] T032 [US2] Implement database query logic to fetch user's tasks using SQLModel
- [X] T033 [US2] Add proper filtering to ensure only user's tasks are returned
- [X] T034 [US2] Implement success response formatting for list_tasks
- [X] T035 [US2] Implement error handling for list_tasks with structured responses
- [X] T036 [P] [US2] Write unit tests for list_tasks in backend/tests/mcp/test_tools/test_list_tasks.py
- [X] T037 [P] [US2] Test user isolation enforcement in list_tasks with different user contexts
- [X] T038 [US2] Register list_tasks with MCP server in backend/src/mcp/server.py

## Phase 5: [US3] Implement Task Updates (User Story 3 - Update Task)

**Goal**: As an authenticated user, I want to update task properties via natural language commands so that I can modify my tasks through the AI interface.

**Independent Test Criteria**:
- User can successfully update their tasks using the update_task MCP tool
- Only user's own tasks can be updated
- Authentication is validated properly
- Tool returns structured response with updated task details

- [X] T040 [US3] Create update_task function in backend/src/mcp/tools/task_operations.py with proper parameters
- [X] T041 [US3] Implement user_id validation in update_task using JWT validation utilities
- [X] T042 [US3] Implement database update logic for tasks using SQLModel
- [X] T043 [US3] Add proper validation to ensure user owns the task being updated
- [X] T044 [US3] Implement success response formatting for update_task
- [X] T045 [US3] Implement error handling for update_task with structured responses
- [X] T046 [P] [US3] Write unit tests for update_task in backend/tests/mcp/test_tools/test_update_task.py
- [X] T047 [P] [US3] Test user isolation enforcement in update_task with different user contexts
- [X] T048 [US3] Register update_task with MCP server in backend/src/mcp/server.py

## Phase 6: [US4] Implement Task Completion (User Story 4 - Complete Task)

**Goal**: As an authenticated user, I want to mark tasks complete/incomplete through AI interaction so that I can update task status via the AI interface.

**Independent Test Criteria**:
- User can successfully mark their tasks complete/incomplete using the complete_task MCP tool
- Only user's own tasks can be marked complete/incomplete
- Authentication is validated properly
- Tool returns structured response with updated task details

- [X] T050 [US4] Create complete_task function in backend/src/mcp/tools/task_operations.py with proper parameters
- [X] T051 [US4] Implement user_id validation in complete_task using JWT validation utilities
- [ ] T052 [US4] Implement database update logic for task completion status using SQLModel
- [ ] T053 [US4] Add proper validation to ensure user owns the task being completed
- [ ] T054 [US4] Implement success response formatting for complete_task
- [ ] T055 [US4] Implement error handling for complete_task with structured responses
- [ ] T056 [P] [US4] Write unit tests for complete_task in backend/tests/mcp/test_tools/test_complete_task.py
- [ ] T057 [P] [US4] Test user isolation enforcement in complete_task with different user contexts
- [ ] T058 [US4] Register complete_task with MCP server in backend/src/mcp/server.py

## Phase 7: [US5] Implement Task Deletion (User Story 5 - Delete Task)

**Goal**: As an authenticated user, I want to delete tasks using conversational commands so that I can remove tasks via the AI interface.

**Independent Test Criteria**:
- User can successfully delete their tasks using the delete_task MCP tool
- Only user's own tasks can be deleted
- Authentication is validated properly
- Tool returns structured response confirming deletion

- [ ] T060 [US5] Create delete_task function in backend/src/mcp/tools/task_operations.py with proper parameters
- [ ] T061 [US5] Implement user_id validation in delete_task using JWT validation utilities
- [ ] T062 [US5] Implement database deletion logic for tasks using SQLModel
- [ ] T063 [US5] Add proper validation to ensure user owns the task being deleted
- [ ] T064 [US5] Implement success response formatting for delete_task
- [ ] T065 [US5] Implement error handling for delete_task with structured responses
- [ ] T066 [P] [US5] Write unit tests for delete_task in backend/tests/mcp/test_tools/test_delete_task.py
- [ ] T067 [P] [US5] Test user isolation enforcement in delete_task with different user contexts
- [ ] T068 [US5] Register delete_task with MCP server in backend/src/mcp/server.py

## Phase 8: [US6] Implement Error Handling & Validation (User Story 6 - Error Handling)

**Goal**: As a system, I want to handle error cases gracefully with informative responses so that AI agents receive meaningful feedback when operations fail.

**Independent Test Criteria**:
- Authentication failures return appropriate error codes indicating invalid JWT or user mismatch
- Database operation failures return structured error responses
- Validation errors return clear indication of which parameters were invalid
- Error responses follow the defined error response format

- [ ] T070 [US6] Create common error response schemas in backend/src/mcp/schemas/task_schemas.py
- [ ] T071 [US6] Implement centralized error handling for all MCP tools
- [ ] T072 [US6] Add validation error handling for all parameter validation in each tool
- [ ] T073 [US6] Implement database error handling with structured responses
- [ ] T074 [US6] Write comprehensive error handling tests in backend/tests/mcp/
- [ ] T075 [US6] Validate all error responses conform to defined structure

## Phase 9: [US7] Complete MCP Server Configuration (User Story 7 - Server Configuration)

**Goal**: As a developer, I want to configure the MCP server to run properly so that AI agents can connect to and use the tools.

**Independent Test Criteria**:
- MCP server starts successfully and registers all 5 tools
- Server runs on configured port (default localhost:8000/mcp)
- All tools are accessible and functional
- Server follows stateless architecture principles

- [ ] T080 [US7] Complete MCP server configuration in backend/src/mcp/server.py
- [ ] T081 [US7] Implement proper startup and shutdown logic for MCP server
- [ ] T082 [US7] Add configuration for server port and endpoint settings
- [ ] T083 [US7] Verify stateless operation principles are maintained
- [ ] T084 [US7] Write server integration tests in backend/tests/mcp/test_server.py
- [ ] T085 [US7] Test server restart resilience and stateless operation

## Phase 10: Integration & Testing Tasks

- [ ] T090 Create comprehensive integration tests for MCP tools in backend/tests/mcp/
- [ ] T091 Test end-to-end user isolation across all tools
- [ ] T092 Test authentication validation across all tools
- [ ] T093 Test database persistence and ACID compliance across all tools
- [ ] T094 Run all MCP tests to ensure full functionality
- [ ] T095 [P] Document API usage examples for each MCP tool

## Phase 11: Polish & Cross-Cutting Concerns

- [ ] T100 Add performance monitoring to tool execution for sub-second response time
- [ ] T101 Implement logging for tool usage and audit trail
- [ ] T102 Optimize database queries for efficient read/write operations
- [ ] T103 Review and refine error messages for AI agent consumption
- [ ] T104 Update quickstart documentation with complete MCP server setup
- [ ] T105 Verify all 5 MCP tools (add_task, list_tasks, update_task, complete_task, delete_task) are fully functional
- [ ] T106 Run final acceptance tests matching specification criteria
- [ ] T107 Prepare final MCP server for integration with AI agents

## Parallel Execution Opportunities

### Per User Story:
- Tests can be developed in parallel with implementation ([P] tasks)
- Schema definitions can be created ahead of implementation
- Multiple developers can work on different tools simultaneously

### Across User Stories:
- All tool functions can be implemented in parallel once foundational components are complete
- Unit tests for each tool can be developed independently
- Error handling can be applied across all tools in parallel

## Success Criteria Validation

Each user story will be validated against the acceptance criteria from the specification:
- [ ] 100% of todo operations (CRUD) available through MCP tools
- [ ] Successful user isolation - no cross-user data access
- [ ] All operations persist to Neon PostgreSQL database
- [ ] Sub-second response time for 95% of tool executions
- [ ] Complete statelessness verified through server restart resilience