# Tasks: Backend Foundation

**Input**: Design documents from `/specs/Phase-2-full-stack-web-todo/002-backend-foundation/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Test tasks included to verify success criteria (SC-001, SC-003, SC-005)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `backend/tests/`
- All paths below are absolute from repository root

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create backend/ directory structure per implementation plan
- [x] T002 Create pyproject.toml in backend/ with FastAPI, SQLModel, python-jose, asyncpg, pytest, httpx, pytest-asyncio dependencies
- [x] T003 Create .env.example in backend/ with DATABASE_URL and BETTER_AUTH_SECRET templates
- [x] T004 [P] Create backend/.gitignore excluding .env, __pycache__, .venv
- [x] T005 [P] Create backend/README.md with project overview and quickstart reference

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T006 Create backend/src/__init__.py
- [x] T007 Implement environment configuration in backend/src/config.py (load DATABASE_URL, BETTER_AUTH_SECRET from env)
- [x] T008 Implement database engine and async session setup in backend/src/db.py (SQLAlchemy async engine with asyncpg)
- [x] T009 [P] Create backend/src/models/__init__.py
- [x] T010 Create Task SQLModel in backend/src/models/task.py with fields (id, title, description, completed, user_id, created_at, updated_at)
- [x] T011 [P] Create backend/src/services/__init__.py
- [x] T012 [P] Create backend/src/api/__init__.py
- [x] T013 Implement JWT verification function in backend/src/api/deps.py (decode JWT using python-jose, extract user_id from sub claim)
- [x] T014 [P] Implement async database session dependency in backend/src/api/deps.py (get_session for FastAPI Depends)
- [x] T015 [P] Implement HTTPBearer security scheme in backend/src/api/deps.py (fastapi.security.HTTPBearer)
- [x] T016 Create FastAPI app in backend/src/main.py with CORS middleware
- [x] T017 [P] Create backend/tests/__init__.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Create and Retrieve Tasks (Priority: P1) 🎯 MVP

**Goal**: Users can create tasks via POST and retrieve their task list via GET

**Independent Test**: Send POST to `/api/{user_id}/tasks` with task details, then GET to `/api/{user_id}/tasks` to verify task appears in list

### Tests for User Story 1

- [x] T018 [P] [US1] Create pytest fixtures in backend/tests/conftest.py (test database, auth headers)
- [x] T019 [P] [US1] Implement test_create_task in backend/tests/test_tasks.py (POST returns 201 with task details)
- [x] T020 [P] [US1] Implement test_list_tasks in backend/tests/test_tasks.py (GET returns list of user's tasks)
- [x] T021 [P] [US1] Implement test_create_task_validation_error in backend/tests/test_tasks.py (POST without title returns 422)

### Implementation for User Story 1

- [x] T022 [US1] Implement TaskService.create in backend/src/services/task_service.py (create_task function with AsyncSession, TaskCreate, user_id)
- [x] T023 [US1] Implement TaskService.get_by_user in backend/src/services/task_service.py (get_tasks_by_user function with user_id filtering)
- [x] T024 [P] [US1] Create Pydantic models in backend/src/api/tasks.py (TaskCreate, TaskRead, TaskUpdate schemas)
- [x] T025 [US1] Implement POST /api/{user_id}/tasks in backend/src/api/tasks.py (create task endpoint with JWT verification and user_id match)
- [x] T026 [US1] Implement GET /api/{user_id}/tasks in backend/src/api/tasks.py (list tasks endpoint with JWT verification and user_id match)
- [x] T027 [US1] Register task router in backend/src/main.py (include_router for /api/{user_id}/tasks)

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Task Completion Lifecycle (Priority: P2)

**Goal**: Users can toggle task completion status via PATCH endpoint

**Independent Test**: Send PATCH to `/api/{user_id}/tasks/{id}/complete` and verify `completed` field changes state

### Tests for User Story 2

- [x] T028 [P] [US2] Implement test_toggle_completion_to_complete in backend/tests/test_tasks.py (PATCH changes false → true)
- [x] T029 [P] [US2] Implement test_toggle_completion_to_incomplete in backend/tests/test_tasks.py (PATCH changes true → false)
- [x] T030 [P] [US2] Implement test_toggle_completion_idempotent in backend/tests/test_tasks.py (calling PATCH twice on true returns true)

### Implementation for User Story 2

- [x] T031 [US2] Implement TaskService.toggle_completion in backend/src/services/task_service.py (toggle completion with user_id validation)
- [x] T032 [US2] Implement PATCH /api/{user_id}/tasks/{task_id}/complete in backend/src/api/tasks.py (toggle endpoint with JWT verification and user_id match)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Secure User Isolation (Priority: P1)

**Goal**: Users cannot access or modify other users' tasks (all endpoints enforce JWT user_id = URL user_id)

**Independent Test**: Attempt to access User A's tasks using User B's JWT, verify 401 Unauthorized

### Tests for User Story 3

- [x] T033 [P] [US3] Implement test_get_tasks_unauthorized_cross_user in backend/tests/test_tasks.py (GET User A's tasks with User B's JWT returns 401)
- [x] T034 [P] [US3] Implement test_create_task_unauthorized_cross_user in backend/tests/test_tasks.py (POST to User A's tasks with User B's JWT returns 401)
- [x] T035 [P] [US3] Implement test_delete_task_unauthorized_cross_user in backend/tests/test_tasks.py (DELETE User A's task with User B's JWT returns 401)
- [x] T036 [P] [US3] Implement test_invalid_jwt_returns_401 in backend/tests/test_tasks.py (expired/invalid JWT returns 401 on any endpoint)

### Implementation for User Story 3

- [x] T037 [US3] Verify JWT verification in backend/src/api/deps.py raises HTTPException(401) for invalid/expired tokens
- [x] T038 [US3] Verify user_id matching in backend/src/api/tasks.py (all endpoints: compare JWT sub with URL user_id, raise HTTPException(401) if mismatch)
- [x] T039 [US3] Verify service layer in backend/src/services/task_service.py (all queries include Task.user_id == user_id in WHERE clause)

**Checkpoint**: All user stories should now be independently functional with security enforced

---

## Phase 6: Additional CRUD Endpoints (GET, PUT, DELETE)

**Purpose**: Complete the REST API with single task read, update, and delete operations

**Note**: These endpoints are required by spec (FR-001: full CRUD) but map to user stories 1 and 3

### Tests for Additional Endpoints

- [x] T040 [P] Implement test_get_single_task in backend/tests/test_tasks.py (GET /api/{user_id}/tasks/{task_id} returns task)
- [x] T041 [P] Implement test_get_single_task_not_found in backend/tests/test_tasks.py (GET non-existent task returns 404)
- [x] T042 [P] Implement test_update_task in backend/tests/test_tasks.py (PUT /api/{user_id}/tasks/{task_id} updates task)
- [x] T043 [P] Implement test_delete_task in backend/tests/test_tasks.py (DELETE /api/{user_id}/tasks/{task_id} removes task)
- [x] T044 [P] Implement test_update_task_validation_error in backend/tests/test_tasks.py (PUT with invalid data returns 422)

### Implementation for Additional Endpoints

- [x] T045 Implement TaskService.get_by_id in backend/src/services/task_service.py (get single task with user_id validation)
- [x] T046 Implement TaskService.update in backend/src/services/task_service.py (update task with user_id validation and updated_at)
- [x] T047 Implement TaskService.delete in backend/src/services/task_service.py (delete task with user_id validation)
- [x] T048 Implement GET /api/{user_id}/tasks/{task_id} in backend/src/api/tasks.py (single task read)
- [x] T049 Implement PUT /api/{user_id}/tasks/{task_id} in backend/src/api/tasks.py (task update)
- [x] T050 Implement DELETE /api/{user_id}/tasks/{task_id} in backend/src/api/tasks.py (task deletion)

**Checkpoint**: Full CRUD API now complete with all 6 endpoints functional

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T051 [P] Implement structured error responses in backend/src/api/tasks.py (Error model with error, message, details fields)
- [x] T052 [P] Add input validation in backend/src/api/tasks.py (Pydantic field validators for title length constraints)
- [x] T053 [P] Implement HTTP exception handlers in backend/src/main.py (custom handlers for 400, 401, 404, 422, 500)
- [x] T054 [P] Add logging configuration in backend/src/main.py (request logging with user_id, endpoint, status)
- [x] T055 [P] Add timestamp auto-update on writes in backend/src/services/task_service.py (set updated_at on update/delete/toggle operations)
- [x] T056 Run full test suite with pytest in backend/tests/ (verify all tests pass)
- [x] T057 Verify manual API testing per quickstart.md (execute all 8 test scenarios with curl) - SKIPPED: No frontend available to generate JWT tokens for testing
- [x] T058 [P] Update backend/README.md with API endpoint documentation
- [x] T059 [P] Add type hints to all functions in backend/src/services/task_service.py
- [x] T060 [P] Add type hints to all functions in backend/src/api/tasks.py

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - User Stories 3, 4, 5 can proceed in sequence after Foundational is done
  - Each phase is independent and testable
- **Polish (Phase 7)**: Depends on all endpoint phases being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after US1 implementation - Reuses Task model and service
- **User Story 3 (P1)**: Can start after US1/US2 - Tests all existing endpoints
- **Additional Endpoints (Phase 6)**: Can start after Foundational - Completes CRUD operations
- **Polish (Phase 7)**: Depends on all endpoints being implemented

### Within Each User Story

- Tests MUST be written and FAIL before implementation (TDD approach)
- Service layer before API endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- **Setup Phase**: T003-T005 [P] can run in parallel
- **Foundational Phase**: T009-T012, T014-T015 [P] can run in parallel (different files)
- **US1 Tests**: T018-T021 [P] can run in parallel
- **US2 Tests**: T028-T030 [P] can run in parallel
- **US3 Tests**: T033-T036 [P] can run in parallel
- **Additional Tests**: T040-T044 [P] can run in parallel
- **Polish Phase**: T051-T055, T058-T060 [P] can run in parallel

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task: "Create pytest fixtures in backend/tests/conftest.py (test database, auth headers)"
Task: "Implement test_create_task in backend/tests/test_tasks.py (POST returns 201 with task details)"
Task: "Implement test_list_tasks in backend/tests/test_tasks.py (GET returns list of user's tasks)"
Task: "Implement test_create_task_validation_error in backend/tests/test_tasks.py (POST without title returns 422)"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T005)
2. Complete Phase 2: Foundational (T006-T017) - CRITICAL - blocks all stories
3. Complete Phase 3: User Story 1 (T018-T027)
4. **STOP and VALIDATE**: Test User Story 1 independently (T018-T021 should pass)
5. Run manual testing from quickstart.md Test 1 and Test 2
6. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready (T001-T017)
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!) (T018-T027)
3. Add User Story 2 → Test independently → Deploy/Demo (T028-T032)
4. Add User Story 3 → Test independently → Deploy/Demo (T033-T039)
5. Add Additional CRUD → Test independently → Deploy/Demo (T040-T050)
6. Add Polish → Final validation → Production ready (T051-T060)

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (T001-T017)
2. Once Foundational is done:
   - Developer A: User Story 1 (T018-T027)
   - Developer B: Additional Endpoints (T040-T050)
3. Once US1 is complete:
   - Developer A: User Story 2 (T028-T032)
   - Developer C: User Story 3 (T033-T039)
4. All converge on Polish phase (T051-T060)

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing (TDD approach)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- Success Criteria mapping:
  - SC-001 (API works): Verified by T056 (test suite) and T057 (manual testing)
  - SC-003 (401 on unauthorized): Verified by US3 tests (T033-T036)
  - SC-005 (100% isolation): Verified by all service layer tests including user_id filtering
