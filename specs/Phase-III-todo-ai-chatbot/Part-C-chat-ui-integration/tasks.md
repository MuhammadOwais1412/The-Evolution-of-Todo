# Tasks: Chat UI & End-to-End Integration

**Input**: Design documents from `specs/Phase-III-todo-ai-chatbot/Part-C-chat-ui-integration/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Tests are NOT included as they were not explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `Phase-3-todo-ai-chatbot/backend/src/`
- **Frontend**: `Phase-3-todo-ai-chatbot/frontend/src/`
- Paths shown below follow the monorepo structure from plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Database schema and dependency installation

- [ ] T001 Create database migration for conversations and messages tables in Phase-3-todo-ai-chatbot/backend/alembic/versions/003_add_chat_tables.py
- [ ] T002 Run database migration to create conversations and messages tables
- [ ] T003 [P] Install OpenAI ChatKit in frontend: npm install @openai/chatkit in Phase-3-todo-ai-chatbot/frontend/
- [ ] T004 [P] Verify SQLModel models can be imported and migration succeeded

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core data models, schemas, and services that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T005 [P] Create Conversation model in Phase-3-todo-ai-chatbot/backend/src/models/conversation.py
- [ ] T006 [P] Create Message model with MessageRole enum in Phase-3-todo-ai-chatbot/backend/src/models/message.py
- [ ] T007 [P] Create chat request/response schemas in Phase-3-todo-ai-chatbot/backend/src/schemas/chat_schemas.py
- [ ] T008 Create ConversationService with create_conversation method in Phase-3-todo-ai-chatbot/backend/src/services/conversation_service.py
- [ ] T009 Add add_message method to ConversationService in Phase-3-todo-ai-chatbot/backend/src/services/conversation_service.py
- [ ] T010 Add get_conversation_messages method with pagination to ConversationService in Phase-3-todo-ai-chatbot/backend/src/services/conversation_service.py
- [ ] T011 Add get_user_conversations method to ConversationService in Phase-3-todo-ai-chatbot/backend/src/services/conversation_service.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Authenticated Chat Access (Priority: P1) 🎯 MVP

**Goal**: Users can access a chat interface after logging in with JWT authentication, and unauthenticated users are redirected to login

**Independent Test**: Log in with valid credentials and verify chat interface loads. Attempt access without authentication and confirm redirect to login page. Try with expired JWT token and verify authentication error.

### Implementation for User Story 1

- [ ] T012 [P] [US1] Create chat page route in Phase-3-todo-ai-chatbot/frontend/src/app/chat/page.tsx with 'use client' directive
- [ ] T013 [P] [US1] Create authentication guard component in Phase-3-todo-ai-chatbot/frontend/src/components/AuthGuard.tsx
- [ ] T014 [US1] Integrate AuthGuard with chat page to redirect unauthenticated users in Phase-3-todo-ai-chatbot/frontend/src/app/chat/page.tsx
- [ ] T015 [P] [US1] Create axios client with JWT interceptor in Phase-3-todo-ai-chatbot/frontend/src/services/apiClient.ts
- [ ] T016 [US1] Add 401 response interceptor for token expiration handling in Phase-3-todo-ai-chatbot/frontend/src/services/apiClient.ts
- [ ] T017 [US1] Create basic ChatInterface component skeleton in Phase-3-todo-ai-chatbot/frontend/src/components/ChatInterface.tsx
- [ ] T018 [US1] Verify authentication flow: login → chat access, no auth → redirect, expired token → error

**Checkpoint**: At this point, authenticated users can access the chat interface, and authentication is properly enforced

---

## Phase 4: User Story 2 - Natural Language Task Management (Priority: P1) 🎯 MVP

**Goal**: Users can send natural language commands to create, view, update, and complete tasks through the chat interface

**Independent Test**: Send commands like "Add a task to buy groceries", "Show my tasks", "Mark the first task as complete" and verify correct actions are taken and AI responds appropriately.

### Implementation for User Story 2

- [ ] T019 [P] [US2] Create chat endpoint POST /api/{user_id}/chat in Phase-3-todo-ai-chatbot/backend/src/api/routes/chat.py
- [ ] T020 [US2] Add JWT token validation to chat endpoint in Phase-3-todo-ai-chatbot/backend/src/api/routes/chat.py
- [ ] T021 [US2] Add user_id authorization check (URL matches JWT) in Phase-3-todo-ai-chatbot/backend/src/api/routes/chat.py
- [ ] T022 [US2] Implement message persistence logic in chat endpoint in Phase-3-todo-ai-chatbot/backend/src/api/routes/chat.py
- [ ] T023 [US2] Integrate AI Agent service call with context reconstruction in Phase-3-todo-ai-chatbot/backend/src/api/routes/chat.py
- [ ] T024 [US2] Add rate limiting (10 messages/minute) to chat endpoint in Phase-3-todo-ai-chatbot/backend/src/api/routes/chat.py
- [ ] T025 [P] [US2] Create chatService with sendMessage method in Phase-3-todo-ai-chatbot/frontend/src/services/chatService.ts
- [ ] T026 [P] [US2] Create useChat hook for chat state management in Phase-3-todo-ai-chatbot/frontend/src/hooks/useChat.ts
- [ ] T027 [US2] Implement optimistic UI updates in useChat hook in Phase-3-todo-ai-chatbot/frontend/src/hooks/useChat.ts
- [ ] T028 [P] [US2] Create MessageList component with ChatKit in Phase-3-todo-ai-chatbot/frontend/src/components/MessageList.tsx
- [ ] T029 [P] [US2] Create MessageInput component with send button in Phase-3-todo-ai-chatbot/frontend/src/components/MessageInput.tsx
- [ ] T030 [US2] Integrate MessageList and MessageInput into ChatInterface in Phase-3-todo-ai-chatbot/frontend/src/components/ChatInterface.tsx
- [ ] T031 [US2] Add message sending logic with API call in ChatInterface in Phase-3-todo-ai-chatbot/frontend/src/components/ChatInterface.tsx
- [ ] T032 [US2] Verify natural language task management: add task, list tasks, update task, complete task, delete task with confirmation

**Checkpoint**: At this point, users can manage tasks through natural language in the chat interface

---

## Phase 5: User Story 3 - Conversation Persistence (Priority: P2)

**Goal**: Chat conversations are saved and users can return later to see previous interactions and continue where they left off

**Independent Test**: Have a conversation, log out, log back in, and verify previous conversation history is displayed. Refresh page and verify history remains.

### Implementation for User Story 3

- [ ] T033 [P] [US3] Create conversation history endpoint GET /api/{user_id}/conversations/{conversation_id}/messages in Phase-3-todo-ai-chatbot/backend/src/api/routes/chat.py
- [ ] T034 [US3] Add JWT token validation and user authorization to history endpoint in Phase-3-todo-ai-chatbot/backend/src/api/routes/chat.py
- [ ] T035 [US3] Implement pagination (limit, offset) in history endpoint in Phase-3-todo-ai-chatbot/backend/src/api/routes/chat.py
- [ ] T036 [P] [US3] Add getConversationHistory method to chatService in Phase-3-todo-ai-chatbot/frontend/src/services/chatService.ts
- [ ] T037 [US3] Add conversation_id management to useChat hook (localStorage) in Phase-3-todo-ai-chatbot/frontend/src/hooks/useChat.ts
- [ ] T038 [US3] Implement history loading on chat interface mount in Phase-3-todo-ai-chatbot/frontend/src/components/ChatInterface.tsx
- [ ] T039 [US3] Add auto-scroll to latest message functionality in Phase-3-todo-ai-chatbot/frontend/src/components/MessageList.tsx
- [ ] T040 [US3] Verify conversation persistence: send messages, refresh page, verify history loads, log out/in, verify history persists

**Checkpoint**: At this point, conversations persist across sessions and page refreshes

---

## Phase 6: User Story 4 - Real-time Feedback and Error Handling (Priority: P2)

**Goal**: Users receive immediate feedback on commands and clear error messages when something goes wrong

**Independent Test**: Send valid command and verify loading indicator + confirmation within 3 seconds. Send invalid command and verify clear error message. Simulate network error and verify retry logic.

### Implementation for User Story 4

- [ ] T041 [P] [US4] Add loading state management to useChat hook in Phase-3-todo-ai-chatbot/frontend/src/hooks/useChat.ts
- [ ] T042 [P] [US4] Add error state management with error types to useChat hook in Phase-3-todo-ai-chatbot/frontend/src/hooks/useChat.ts
- [ ] T043 [US4] Implement typing indicator in MessageList component in Phase-3-todo-ai-chatbot/frontend/src/components/MessageList.tsx
- [ ] T044 [US4] Add "Sending..." indicator to MessageInput component in Phase-3-todo-ai-chatbot/frontend/src/components/MessageInput.tsx
- [ ] T045 [US4] Implement error message display in ChatInterface in Phase-3-todo-ai-chatbot/frontend/src/components/ChatInterface.tsx
- [ ] T046 [US4] Add retry logic with exponential backoff to chatService in Phase-3-todo-ai-chatbot/frontend/src/services/chatService.ts
- [ ] T047 [US4] Implement user-friendly error messages mapping in Phase-3-todo-ai-chatbot/frontend/src/services/chatService.ts
- [ ] T048 [US4] Add retry button for failed messages in MessageList in Phase-3-todo-ai-chatbot/frontend/src/components/MessageList.tsx
- [ ] T049 [US4] Add input validation (max 1000 chars) to MessageInput in Phase-3-todo-ai-chatbot/frontend/src/components/MessageInput.tsx
- [ ] T050 [US4] Verify feedback and error handling: loading states, error messages, retry logic, validation errors

**Checkpoint**: At this point, users receive clear feedback and can recover from errors

---

## Phase 7: User Story 5 - Multi-device Conversation Sync (Priority: P3)

**Goal**: Conversations sync across devices so users can start on one device and continue on another

**Independent Test**: Start conversation on one device (or browser), log in on another device (or browser), and verify conversation history is synchronized.

### Implementation for User Story 5

- [ ] T051 [US5] Verify conversation sync works across devices (already implemented via database persistence in US3)
- [ ] T052 [US5] Test multi-device scenario: send message on device A, verify appears on device B after login

**Checkpoint**: All user stories are now independently functional

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and final validation

- [ ] T053 [P] Add responsive design styles for mobile viewport in Phase-3-todo-ai-chatbot/frontend/src/components/ChatInterface.tsx
- [ ] T054 [P] Add message timestamps with relative formatting in Phase-3-todo-ai-chatbot/frontend/src/components/MessageList.tsx
- [ ] T055 [P] Implement multi-line text support in MessageInput in Phase-3-todo-ai-chatbot/frontend/src/components/MessageInput.tsx
- [ ] T056 [P] Add confirmation dialog for destructive operations in Phase-3-todo-ai-chatbot/frontend/src/components/ChatInterface.tsx
- [ ] T057 [P] Add input sanitization for XSS prevention in Phase-3-todo-ai-chatbot/backend/src/api/routes/chat.py
- [ ] T058 [P] Optimize database queries with proper indexing verification in Phase-3-todo-ai-chatbot/backend/src/services/conversation_service.py
- [ ] T059 [P] Add logging for chat operations in Phase-3-todo-ai-chatbot/backend/src/api/routes/chat.py
- [ ] T060 Run quickstart.md validation: all setup steps, manual tests, performance checks
- [ ] T061 Update API documentation with new chat endpoints in Phase-3-todo-ai-chatbot/backend/docs/
- [ ] T062 Code review and cleanup: remove debug code, ensure consistent formatting

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - User Story 1 (P1): Can start after Foundational - No dependencies on other stories
  - User Story 2 (P1): Can start after Foundational - No dependencies on other stories (but logically builds on US1)
  - User Story 3 (P2): Can start after Foundational - Enhances US2 but independently testable
  - User Story 4 (P2): Can start after Foundational - Enhances US2 but independently testable
  - User Story 5 (P3): Can start after Foundational - Leverages US3 implementation
- **Polish (Phase 8)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Authentication and chat access - Foundation for all other stories
- **User Story 2 (P1)**: Natural language task management - Core functionality, builds on US1
- **User Story 3 (P2)**: Conversation persistence - Independent but enhances US2
- **User Story 4 (P2)**: Error handling and feedback - Independent but enhances US2
- **User Story 5 (P3)**: Multi-device sync - Leverages US3 persistence

### Within Each User Story

- Backend endpoints before frontend integration
- Models and services before endpoints
- Core functionality before error handling
- Story complete before moving to next priority

### Parallel Opportunities

- **Phase 1**: T003 and T004 can run in parallel with T001-T002 (different concerns)
- **Phase 2**: T005, T006, T007 can all run in parallel (different files)
- **Phase 3 (US1)**: T012, T013, T015, T017 can run in parallel (different files)
- **Phase 4 (US2)**: T019, T025, T026, T028, T029 can run in parallel (different files)
- **Phase 5 (US3)**: T033, T036 can run in parallel (backend vs frontend)
- **Phase 6 (US4)**: T041, T042, T043, T044 can run in parallel (different files)
- **Phase 8**: Most polish tasks (T053-T059) can run in parallel (different files)

---

## Parallel Example: User Story 2

```bash
# Launch backend and frontend tasks together:
Task T019: "Create chat endpoint POST /api/{user_id}/chat"
Task T025: "Create chatService with sendMessage method"
Task T026: "Create useChat hook for chat state management"
Task T028: "Create MessageList component with ChatKit"
Task T029: "Create MessageInput component with send button"

# Then integrate sequentially:
Task T020-T024: Backend endpoint implementation
Task T027: Optimistic updates in useChat
Task T030-T032: Frontend integration and verification
```

---

## Implementation Strategy

### MVP First (User Stories 1 + 2 Only)

1. Complete Phase 1: Setup (T001-T004)
2. Complete Phase 2: Foundational (T005-T011) - CRITICAL
3. Complete Phase 3: User Story 1 (T012-T018) - Authentication
4. Complete Phase 4: User Story 2 (T019-T032) - Core functionality
5. **STOP and VALIDATE**: Test US1 and US2 independently
6. Deploy/demo if ready - this is a functional MVP!

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Users can access chat
3. Add User Story 2 → Test independently → Users can manage tasks (MVP!)
4. Add User Story 3 → Test independently → Conversations persist
5. Add User Story 4 → Test independently → Better UX with error handling
6. Add User Story 5 → Test independently → Multi-device support
7. Add Polish → Final refinements
8. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (T001-T011)
2. Once Foundational is done:
   - Developer A: User Story 1 (T012-T018)
   - Developer B: User Story 2 backend (T019-T024)
   - Developer C: User Story 2 frontend (T025-T032)
3. After US1 and US2 complete:
   - Developer A: User Story 3 (T033-T040)
   - Developer B: User Story 4 (T041-T050)
   - Developer C: User Story 5 (T051-T052)
4. All developers: Polish (T053-T062)

---

## Notes

- [P] tasks = different files, no dependencies, can run in parallel
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- MVP = User Stories 1 + 2 (authentication + core functionality)
- User Stories 3-5 are enhancements that can be added incrementally
- No test tasks included as tests were not explicitly requested in specification
- All tasks follow constitution principles: stateless server, MCP-first AI, API-first architecture
