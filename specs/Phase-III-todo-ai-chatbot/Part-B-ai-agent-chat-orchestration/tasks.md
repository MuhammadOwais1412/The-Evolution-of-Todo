# Implementation Tasks: Phase III – Part B: AI Agent & Chat Orchestration

## Feature: AI Agent & Chat Orchestration
**Objective**: Implement an AI agent that interprets natural language todo commands, selects appropriate MCP tools, and confirms actions clearly to the user while maintaining stateless operation.

---

## Phase 1: Project Setup & Dependencies

- [x] T001 Create directory structure for AI agent components in Phase-3-todo-ai-chatbot/backend/src/ai/
- [ ] T002 [P] Install OpenAI SDK and Google Gemini dependencies in backend
- [x] T003 [P] Update environment variables in .env with GEMINI_API_KEY and OPENAI_BASE_URL
- [x] T004 [P] Create configuration module for AI provider settings in Phase-3-todo-ai-chatbot/backend/src/config/ai_config.py
- [ ] T005 Update pyproject.toml with new AI-related dependencies

## Phase 2: Foundational Components

- [ ] T006 Create ToolCallLog SQLModel in Phase-3-todo-ai-chatbot/backend/src/models/tool_call_log.py
- [ ] T007 [P] Implement database migration for tool_call_logs table
- [ ] T008 [P] Create Pydantic schemas for AI request/response in Phase-3-todo-ai-chatbot/backend/src/schemas/ai_schemas.py
- [ ] T009 Implement utility functions for JWT validation from Better Auth in Phase-3-todo-ai-chatbot/backend/src/utils/auth_utils.py
- [ ] T010 Create base exception classes for AI agent in Phase-3-todo-ai-chatbot/backend/src/exceptions/ai_exceptions.py

## Phase 3: [US1] Core AI Agent Service

**Goal**: Implement the core AI agent service that processes natural language commands and maps them to MCP tools.

**Independent Test Criteria**: The AI agent service can receive a natural language command and determine which MCP tool to call without errors.

- [ ] T011 [US1] Create AI agent service class in Phase-3-todo-ai-chatbot/backend/src/ai/agent_service.py
- [ ] T012 [P] [US1] Implement Google Gemini client initialization in Phase-3-todo-ai-chatbot/backend/src/ai/gemini_client.py
- [ ] T013 [P] [US1] Create MCP tool adapter functions in Phase-3-todo-ai-chatbot/backend/src/ai/mcp_adapters.py
- [ ] T014 [US1] Implement tool definitions for OpenAI Assistant API that map to MCP tools
- [ ] T015 [US1] Create natural language processing function that determines appropriate MCP tool
- [ ] T016 [US1] Implement tool call execution and result formatting

## Phase 4: [US2] Context Reconstruction

**Goal**: Implement conversation context reconstruction from database per request while maintaining stateless operation.

**Independent Test Criteria**: The system can fetch and reconstruct conversation context for a user without server-side state storage.

- [ ] T017 [US2] Create context reconstruction service in Phase-3-todo-ai-chatbot/backend/src/ai/context_reconstructor.py
- [ ] T018 [P] [US2] Implement database queries to fetch user's task history for context
- [ ] T019 [US2] Create function to format conversation history for AI model context
- [ ] T020 [US2] Implement logic to limit context size to prevent model limits exceeded
- [ ] T021 [US2] Add caching layer to optimize context retrieval (optional but recommended)

## Phase 5: [US3] MCP Tool Orchestration

**Goal**: Develop orchestrator that validates user permissions and executes appropriate MCP tools.

**Independent Test Criteria**: The system can validate user permissions and execute MCP tools safely on behalf of the user.

- [ ] T022 [US3] Create MCP tool orchestrator in Phase-3-todo-ai-chatbot/backend/src/ai/tool_orchestrator.py
- [ ] T023 [P] [US3] Implement user permission validation for each tool call
- [ ] T024 [P] [US3] Create wrapper functions for each MCP tool (add_task, list_tasks, update_task, complete_task, delete_task)
- [ ] T025 [US3] Implement result mapping from MCP tools to AI agent format
- [ ] T026 [US3] Add error handling for MCP tool execution failures

## Phase 6: [US4] Audit Logging

**Goal**: Implement comprehensive logging for all AI-initiated tool calls.

**Independent Test Criteria**: All tool calls made by the AI agent are logged with complete metadata in the database.

- [ ] T027 [US4] Create audit logger service in Phase-3-todo-ai-chatbot/backend/src/ai/audit_logger.py
- [ ] T028 [P] [US4] Implement function to create ToolCallLog entries in database
- [ ] T029 [US4] Add logging for all MCP tool calls made by AI agent
- [ ] T030 [US4] Implement log querying function for retrieving audit history
- [ ] T031 [US4] Add log rotation/cleanup logic for performance management

## Phase 7: [US5] API Endpoint Implementation

**Goal**: Create the main AI chat API endpoint that integrates all components.

**Independent Test Criteria**: The endpoint can receive a natural language command and return an appropriate response with tool calls.

- [ ] T032 [US5] Create AI chat router in Phase-3-todo-ai-chatbot/backend/src/api/routes/ai_chat.py
- [ ] T033 [P] [US5] Implement POST /api/ai/chat endpoint with JWT authentication
- [ ] T034 [US5] Add request validation for AI chat endpoint using Pydantic schemas
- [ ] T035 [US5] Integrate AI agent service, context reconstruction, and tool orchestration
- [ ] T036 [US5] Implement response formatting for the AI chat endpoint
- [ ] T037 [US5] Add rate limiting to the AI chat endpoint

## Phase 8: [US6] User Confirmation Flows

**Goal**: Implement confirmation prompts for potentially destructive operations.

**Independent Test Criteria**: The AI agent prompts for confirmation before executing potentially destructive operations like task deletion.

- [ ] T038 [US6] Update AI agent service to detect destructive operations requiring confirmation
- [ ] T039 [P] [US6] Implement confirmation logic in Phase-3-todo-ai-chatbot/backend/src/ai/confirmation_handler.py
- [ ] T040 [US6] Add confirmation status to API response schema
- [ ] T041 [US6] Create endpoint for handling user confirmations
- [ ] T042 [US6] Implement safety checks for critical operations

## Phase 9: [US7] Error Handling & User Experience

**Goal**: Implement comprehensive error handling and user-friendly responses.

**Independent Test Criteria**: The system gracefully handles errors and provides clear feedback to users.

- [ ] T043 [US7] Implement error handling in AI agent service for API failures
- [ ] T044 [P] [US7] Create error response schemas for different failure modes
- [ ] T045 [US7] Add user-friendly error messages for various failure scenarios
- [ ] T046 [US7] Implement retry logic for transient failures
- [ ] T047 [US7] Add input sanitization to prevent harmful inputs

## Phase 10: [US8] Additional Endpoints & Monitoring

**Goal**: Implement auxiliary endpoints for audit logs and health checks.

**Independent Test Criteria**: Additional endpoints for monitoring and audit trail are functional.

- [ ] T048 [US8] Implement GET /api/ai/tool-call-log endpoint for audit retrieval
- [ ] T049 [P] [US8] Create query parameters handling for audit log endpoint
- [ ] T050 [US8] Implement GET /api/ai/health endpoint for service monitoring
- [ ] T051 [US8] Add health checks for MCP tool availability
- [ ] T052 [US8] Implement metrics collection for AI agent usage

## Phase 11: Testing & Validation

- [ ] T053 [P] Create unit tests for AI agent service
- [ ] T054 [P] Create unit tests for context reconstruction module
- [ ] T055 [P] Create unit tests for tool orchestration service
- [ ] T056 [P] Create integration tests for AI chat endpoint
- [ ] T057 Create end-to-end tests for complete AI interaction flow
- [ ] T058 Implement functional tests for all user scenarios
- [ ] T059 Add performance tests to validate response times < 3s
- [ ] T060 Update documentation for AI agent usage and integration

## Phase 12: Security & Optimization

- [ ] T061 [P] Add input validation and sanitization to prevent prompt injection
- [ ] T062 [P] Implement content moderation for AI responses
- [ ] T063 Optimize database queries for context reconstruction
- [ ] T064 Add proper error logging for debugging
- [ ] T065 Implement proper shutdown handling for AI services

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