# Implementation Tasks: Phase III – Part B: AI Agent & Chat Orchestration

## Feature: AI Agent & Chat Orchestration
**Objective**: Implement an AI agent that interprets natural language todo commands, selects appropriate MCP tools, and confirms actions clearly to the user while maintaining stateless operation.

---

## Phase 1: Project Setup & Dependencies

- [x] T001 Create directory structure for AI agent components in Phase-3-todo-ai-chatbot/backend/src/ai/
- [x] T002 [P] Install OpenAI SDK and Google Gemini dependencies in backend
- [x] T003 [P] Update environment variables in .env with GEMINI_API_KEY and OPENAI_BASE_URL
- [x] T004 [P] Create configuration module for AI provider settings in Phase-3-todo-ai-chatbot/backend/src/config/ai_config.py
- [x] T005 Update pyproject.toml with new AI-related dependencies

## Phase 2: Foundational Components

- [x] T006 Create ToolCallLog SQLModel in Phase-3-todo-ai-chatbot/backend/src/models/tool_call_log.py
- [x] T007 [P] Implement database migration for tool_call_logs table
- [x] T008 [P] Create Pydantic schemas for AI request/response in Phase-3-todo-ai-chatbot/backend/src/schemas/ai_schemas.py
- [x] T009 Implement utility functions for JWT validation from Better Auth in Phase-3-todo-ai-chatbot/backend/src/utils/auth_utils.py
- [x] T010 Create base exception classes for AI agent in Phase-3-todo-ai-chatbot/backend/src/exceptions/ai_exceptions.py

## Phase 3: [US1] Core AI Agent Service

**Goal**: Implement the core AI agent service that processes natural language commands and maps them to MCP tools.

**Independent Test Criteria**: The AI agent service can receive a natural language command and determine which MCP tool to call without errors.

- [x] T011 [US1] Create AI agent service class in Phase-3-todo-ai-chatbot/backend/src/ai/agent_service.py
- [x] T012 [P] [US1] Implement Google Gemini client initialization in Phase-3-todo-ai-chatbot/backend/src/ai/gemini_client.py
- [x] T013 [P] [US1] Create MCP tool adapter functions in Phase-3-todo-ai-chatbot/backend/src/ai/mcp_adapters.py
- [x] T014 [US1] Implement tool definitions for OpenAI Assistant API that map to MCP tools
- [x] T015 [US1] Create natural language processing function that determines appropriate MCP tool
- [x] T016 [US1] Implement tool call execution and result formatting

## Phase 4: [US2] Context Reconstruction

**Goal**: Implement conversation context reconstruction from database per request while maintaining stateless operation.

**Independent Test Criteria**: The system can fetch and reconstruct conversation context for a user without server-side state storage.

- [x] T017 [US2] Create context reconstruction service in Phase-3-todo-ai-chatbot/backend/src/ai/context_reconstructor.py
- [x] T018 [P] [US2] Implement database queries to fetch user's task history for context
- [x] T019 [US2] Create function to format conversation history for AI model context
- [x] T020 [US2] Implement logic to limit context size to prevent model limits exceeded
- [ ] T021 [US2] Add caching layer to optimize context retrieval (optional but recommended)

## Phase 5: [US3] MCP Tool Orchestration

**Goal**: Develop orchestrator that validates user permissions and executes appropriate MCP tools.

**Independent Test Criteria**: The system can validate user permissions and execute MCP tools safely on behalf of the user.

- [x] T022 [US3] Create MCP tool orchestrator in Phase-3-todo-ai-chatbot/backend/src/ai/tool_orchestrator.py
- [x] T023 [P] [US3] Implement user permission validation for each tool call
- [x] T024 [P] [US3] Create wrapper functions for each MCP tool (add_task, list_tasks, update_task, complete_task, delete_task)
- [x] T025 [US3] Implement result mapping from MCP tools to AI agent format
- [x] T026 [US3] Add error handling for MCP tool execution failures

## Phase 6: [US4] Audit Logging

**Goal**: Implement comprehensive logging for all AI-initiated tool calls.

**Independent Test Criteria**: All tool calls made by the AI agent are logged with complete metadata in the database.

- [x] T027 [US4] Create audit logger service in Phase-3-todo-ai-chatbot/backend/src/ai/audit_logger.py
- [x] T028 [P] [US4] Implement function to create ToolCallLog entries in database
- [x] T029 [US4] Add logging for all MCP tool calls made by AI agent
- [x] T030 [US4] Implement log querying function for retrieving audit history
- [x] T031 [US4] Add log rotation/cleanup logic for performance management

## Phase 7: [US5] API Endpoint Implementation

**Goal**: Create the main AI chat API endpoint that integrates all components.

**Independent Test Criteria**: The endpoint can receive a natural language command and return an appropriate response with tool calls.

- [x] T032 [US5] Create AI chat router in Phase-3-todo-ai-chatbot/backend/src/api/routes/ai_chat.py
- [x] T033 [P] [US5] Implement POST /api/ai/chat endpoint with JWT authentication
- [x] T034 [US5] Add request validation for AI chat endpoint using Pydantic schemas
- [x] T035 [US5] Integrate AI agent service, context reconstruction, and tool orchestration
- [x] T036 [US5] Implement response formatting for the AI chat endpoint
- [x] T037 [US5] Add rate limiting to the AI chat endpoint

## Phase 8: [US6] User Confirmation Flows

**Goal**: Implement confirmation prompts for potentially destructive operations.

**Independent Test Criteria**: The AI agent prompts for confirmation before executing potentially destructive operations like task deletion.

- [x] T038 [US6] Update AI agent service to detect destructive operations requiring confirmation
- [x] T039 [P] [US6] Implement confirmation logic in Phase-3-todo-ai-chatbot/backend/src/ai/confirmation_handler.py
- [x] T040 [US6] Add confirmation status to API response schema
- [x] T041 [US6] Create endpoint for handling user confirmations
- [x] T042 [US6] Implement safety checks for critical operations

## Phase 9: [US7] Error Handling & User Experience

**Goal**: Implement comprehensive error handling and user-friendly responses.

**Independent Test Criteria**: The system gracefully handles errors and provides clear feedback to users.

- [x] T043 [US7] Implement error handling in AI agent service for API failures
- [x] T044 [P] [US7] Create error response schemas for different failure modes
- [x] T045 [US7] Add user-friendly error messages for various failure scenarios
- [x] T046 [US7] Implement retry logic for transient failures
- [x] T047 [US7] Add input sanitization to prevent harmful inputs

## Phase 10: [US8] Additional Endpoints & Monitoring

**Goal**: Implement auxiliary endpoints for audit logs and health checks.

**Independent Test Criteria**: Additional endpoints for monitoring and audit trail are functional.

- [x] T048 [US8] Implement GET /api/ai/tool-call-log endpoint for audit retrieval
- [x] T049 [P] [US8] Create query parameters handling for audit log endpoint
- [x] T050 [US8] Implement GET /api/ai/health endpoint for service monitoring
- [x] T051 [US8] Add health checks for MCP tool availability
- [x] T052 [US8] Implement metrics collection for AI agent usage

## Phase 11: Testing & Validation

- [x] T053 [P] Create unit tests for AI agent service
- [x] T054 [P] Create unit tests for context reconstruction module
- [x] T055 [P] Create unit tests for tool orchestration service
- [x] T056 [P] Create integration tests for AI chat endpoint
- [x] T057 Create end-to-end tests for complete AI interaction flow
- [x] T058 Implement functional tests for all user scenarios
- [x] T059 Add performance tests to validate response times < 3s
- [x] T060 Update documentation for AI agent usage and integration

## Phase 12: Security & Optimization

- [x] T061 [P] Add input validation and sanitization to prevent prompt injection
- [x] T062 [P] Implement content moderation for AI responses
- [x] T063 Optimize database queries for context reconstruction
- [x] T064 Add proper error logging for debugging
- [x] T065 Implement proper shutdown handling for AI services

## Dependencies Between User Stories

1. Phase 1 (Setup) → All other phases
2. Phase 2 (Foundational) → All other phases
3. Phase 3 (Core AI Service) → Phase 5, 6, 7, 8
4. Phase 4 (Context) → Phase 5, 7
5. Phase 5 (Orchestration) → Phase 6, 7
6. Phase 8 (Endpoints) uses components from previous phases

## Parallel Execution Opportunities

- Tasks T002, T003, T004, T005 in Phase 1 can run in parallel
- Tasks T006, T007, T008, T009, T010 in Phase 2 can run in parallel
- Tasks T012, T013 in Phase 3 can run in parallel
- Tasks T018, T023, T024 in Phases 4 and 5 can run in parallel
- Tasks in Phase 11 (testing) can run in parallel once respective components are implemented

## Implementation Strategy

**MVP Scope**: Complete Phases 1, 2, 3, 5, and 7 to have a basic AI agent that can process commands and call MCP tools.

**Incremental Delivery**:
1. MVP: Core AI agent with basic tool calling
2. Iteration 2: Context reconstruction and user isolation
3. Iteration 3: Audit logging and confirmation flows
4. Iteration 4: Additional endpoints and optimizations