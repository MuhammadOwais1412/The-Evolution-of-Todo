# Tasks: Frontend Application with Better Auth

**Input**: Design documents from `/specs/Phase-2-full-stack-web-todo/003-frontend-better-auth/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/

**Tests**: Tests are NOT included - feature specification did not explicitly request TDD approach

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `Phase-2-web-todo/frontend/src/`
- Paths below follow web app structure from plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create Phase-2-web-todo/frontend directory structure
- [X] T002 Initialize Next.js 16+ project with TypeScript and App Router in Phase-2-web-todo/frontend
- [X] T003 [P] Install dependencies: better-auth, @types/node in Phase-2-web-todo/frontend
- [X] T004 [P] Configure package.json scripts (dev, build, start, lint)
- [X] T005 [P] Create .env.local file with backend API URL and Better Auth configuration in Phase-2-web-todo/frontend

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T006 Configure TypeScript (tsconfig.json) for strict mode and path aliases in Phase-2-web-todo/frontend
- [X] T007 [P] Configure Next.js (next.config.js) with App Router settings in Phase-2-web-todo/frontend
- [X] T008 [P] Create Tailwind CSS configuration (tailwind.config.ts) in Phase-2-web-todo/frontend
- [X] T009 Create TypeScript types directory and api.ts types file in Phase-2-web-todo/frontend/src/types
- [X] T010 [P] Create lib directory and auth.ts Better Auth configuration in Phase-2-web-todo/frontend/src/lib
- [X] T011 Create lib/api-client.ts with fetch wrapper and JWT injection in Phase-2-web-todo/frontend/src/lib
- [X] T012 [P] Create context directory and AuthContext in Phase-2-web-todo/frontend/src/context
- [X] T013 Update root layout (app/layout.tsx) with AuthProvider wrapper in Phase-2-web-todo/frontend/src/app
- [X] T014 Create .gitignore for node_modules, .env.local, .next, build artifacts in Phase-2-web-todo/frontend

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Authentication (Priority: P1) 🎯 MVP

**Goal**: Users can create accounts, log in, log out, and persist sessions across page refreshes

**Independent Test**: Sign up for account, receive JWT token, verify API request succeeds, refresh page and confirm session persists

### Implementation for User Story 1

- [X] T015 [P] Create signup page (app/(auth)/signup/page.tsx) with email/password form in Phase-2-web-todo/frontend/src/app/(auth)/signup
- [X] T016 [P] Create login page (app/(auth)/login/page.tsx) with email/password form in Phase-2-web-todo/frontend/src/app/(auth)/login
- [X] T017 [US1] Implement signup form with client-side validation (email format, password min length) in Phase-2-web-todo/frontend/src/app/(auth)/signup/page.tsx
- [X] T018 [US1] Implement login form with Better Auth integration (auth.api.signIn.email) in Phase-2-web-todo/frontend/src/app/(auth)/login/page.tsx
- [X] T019 [US1] Implement signup with Better Auth (auth.api.signUp.email) in Phase-2-web-todo/frontend/src/app/(auth)/signup/page.tsx
- [X] T020 [US1] Implement logout functionality (auth.api.signOut) in Phase-2-web-todo/frontend/src/context/auth-context.tsx
- [X] T021 [US1] Add loading states during auth operations in signup and login pages in Phase-2-web-todo/frontend/src/app/(auth)/signup/page.tsx, Phase-2-web-todo/frontend/src/app/(auth)/login/page.tsx
- [X] T022 [US1] Add error handling and display for auth failures (invalid credentials, network errors) in Phase-2-web-todo/frontend/src/app/(auth)/signup/page.tsx, Phase-2-web-todo/frontend/src/app/(auth)/login/page.tsx
- [X] T023 [US1] Add redirect after successful signup to login page in Phase-2-web-todo/frontend/src/app/(auth)/signup/page.tsx
- [X] T024 [US1] Add redirect after successful login to tasks dashboard in Phase-2-web-todo/frontend/src/app/(auth)/login/page.tsx
- [X] T025 [US1] Verify JWT token is stored and accessible via Better Auth session utilities in Phase-2-web-todo/frontend/src/context/auth-context.tsx

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Task List View (Priority: P1) 🎯 MVP

**Goal**: Authenticated users can view all their tasks in a responsive list with loading and empty states

**Independent Test**: Log in, navigate to tasks page, verify all tasks display with title/completion status/date, verify empty state shows when no tasks exist

### Implementation for User Story 2

- [X] T026 [P] Create tasks directory structure (app/(dashboard)/tasks) in Phase-2-web-todo/frontend/src/app
- [X] T027 [P] Create TaskContext for managing task list state in Phase-2-web-todo/frontend/src/context
- [X] T028 [US2] Create tasks dashboard page (app/(dashboard)/tasks/page.tsx) with list layout in Phase-2-web-todo/frontend/src/app/(dashboard)/tasks
- [X] T029 [US2] Implement loading state while fetching tasks from backend API in Phase-2-web-todo/frontend/src/app/(dashboard)/tasks/page.tsx
- [X] T030 [US2] Implement empty state message when user has no tasks in Phase-2-web-todo/frontend/src/app/(dashboard)/tasks/page.tsx
- [X] T031 [US2] Implement task list display with title, completion status, and creation date in Phase-2-web-todo/frontend/src/app/(dashboard)/tasks/page.tsx
- [X] T032 [US2] Add useAuth hook to redirect unauthenticated users to login in Phase-2-web-todo/frontend/src/app/(dashboard)/tasks/page.tsx
- [X] T033 [US2] Add error handling for failed task list fetch in Phase-2-web-todo/frontend/src/app/(dashboard)/tasks/page.tsx
- [X] T034 [US2] Call apiClient.listTasks(userId) on page mount in Phase-2-web-todo/frontend/src/app/(dashboard)/tasks/page.tsx
- [X] T035 [US2] Apply responsive Tailwind styles (mobile vertical layout, desktop cards) in Phase-2-web-todo/frontend/src/app/(dashboard)/tasks/page.tsx

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Create Task (Priority: P1) 🎯 MVP

**Goal**: Users can create new tasks via a form with validation (required title, optional description, character limits)

**Independent Test**: Create a task with valid title, verify it appears in task list; attempt to create task without title, verify validation error; create task with >200 char title, verify validation

### Implementation for User Story 3

- [X] T036 [P] Create TaskForm component for inputting task title and description in Phase-2-web-todo/frontend/src/components/tasks
- [X] T037 [US3] Add task creation form to tasks dashboard page in Phase-2-web-todo/frontend/src/app/(dashboard)/tasks/page.tsx
- [X] T038 [US3] Implement client-side validation (title required 1-200 chars, description max 5000 chars) in Phase-2-web-todo/frontend/src/components/tasks/TaskForm.tsx
- [X] T039 [US3] Handle form submission with apiClient.createTask(userId, taskData) in Phase-2-web-todo/frontend/src/app/(dashboard)/tasks/page.tsx
- [X] T040 [US3] Update task list state with new task after successful creation in Phase-2-web-todo/frontend/src/app/(dashboard)/tasks/page.tsx
- [X] T041 [US3] Display field-level validation errors from backend (422 response) in Phase-2-web-todo/frontend/src/components/tasks/TaskForm.tsx
- [X] T042 [US3] Add loading state while task is being created (disable submit button, show spinner) in Phase-2-web-todo/frontend/src/app/(dashboard)/tasks/page.tsx
- [X] T043 [US3] Clear form fields after successful task creation in Phase-2-web-todo/frontend/src/app/(dashboard)/tasks/page.tsx

**Checkpoint**: All P1 MVP features (Auth, Task List, Create Task) now complete

---

## Phase 6: User Story 4 - Toggle Task Completion (Priority: P2)

**Goal**: Users can toggle task completion status with immediate UI update and backend persistence

**Independent Test**: Click completion toggle on incomplete task, verify it shows as complete and API reflects change; toggle complete task, verify it shows as incomplete

### Implementation for User Story 4

- [X] T044 [P] Create TaskItem component for individual task display in Phase-2-web-todo/frontend/src/components/tasks
- [X] T045 [US4] Add completion checkbox/toggle button to TaskItem component in Phase-2-web-todo/frontend/src/components/tasks/TaskItem.tsx
- [X] T046 [US4] Implement click handler for completion toggle with apiClient.toggleCompletion(userId, taskId) in Phase-2-web-todo/frontend/src/components/tasks/TaskItem.tsx
- [X] T047 [US4] Update task state locally (optimistic update) while API call is in flight in Phase-2-web-todo/frontend/src/components/tasks/TaskItem.tsx
- [X] T048 [US4] Add visual distinction for completed tasks (strikethrough, gray color, checkmark) in Phase-2-web-todo/frontend/src/components/tasks/TaskItem.tsx
- [X] T049 [US4] Handle API errors for toggle operation (404 not found, 401 unauthorized) in Phase-2-web-todo/frontend/src/components/tasks/TaskItem.tsx
- [X] T050 [US4] Refactor task list to use TaskItem component instead of inline rendering in Phase-2-web-todo/frontend/src/app/(dashboard)/tasks/page.tsx

**Checkpoint**: User Stories 1, 2, 3, and 4 should all work independently

---

## Phase 7: User Story 5 - Edit Task (Priority: P2)

**Goal**: Users can edit task title and description with validation

**Independent Test**: Edit task title, verify change persists and displays; attempt to edit with empty title, verify validation error

### Implementation for User Story 5

- [X] T051 [P] Create EditTaskModal component for editing task details in Phase-2-web-todo/frontend/src/components/tasks
- [X] T052 [US5] Add edit button to TaskItem component that opens modal in Phase-2-web-todo/frontend/src/components/tasks/TaskItem.tsx
- [X] T053 [US5] Implement edit form with current task values pre-populated in Phase-2-web-todo/frontend/src/components/tasks/EditTaskModal.tsx
- [X] T054 [US5] Handle form submission with apiClient.updateTask(userId, taskId, taskData) in Phase-2-web-todo/frontend/src/components/tasks/EditTaskModal.tsx
- [X] T055 [US5] Add client-side validation (title required 1-200 chars, description max 5000 chars) in Phase-2-web-todo/frontend/src/components/tasks/EditTaskModal.tsx
- [X] T056 [US5] Update task in list after successful edit in Phase-2-web-todo/frontend/src/app/(dashboard)/tasks/page.tsx
- [X] T057 [US5] Display field-level validation errors from backend in Phase-2-web-todo/frontend/src/components/tasks/EditTaskModal.tsx
- [X] T058 [US5] Add cancel button to close modal without saving in Phase-2-web-todo/frontend/src/components/tasks/EditTaskModal.tsx
- [X] T059 [US5] Handle API errors for edit operation (404, 401, 422) in Phase-2-web-todo/frontend/src/components/tasks/EditTaskModal.tsx
- [X] T060 [US5] Close modal on successful save in Phase-2-web-todo/frontend/src/components/tasks/EditTaskModal.tsx

**Checkpoint**: User Stories 1-5 should all work independently

---

## Phase 8: User Story 6 - Delete Task (Priority: P3)

**Goal**: Users can delete tasks with confirmation dialog

**Independent Test**: Click delete, confirm deletion, verify task removed from list; cancel deletion, verify task remains

### Implementation for User Story 6

- [X] T061 [P] Create DeleteConfirmModal component for deletion confirmation in Phase-2-web-todo/frontend/src/components/tasks
- [X] T062 [US6] Add delete button to TaskItem component that opens confirmation modal in Phase-2-web-todo/frontend/src/components/tasks/TaskItem.tsx
- [X] T063 [US6] Implement confirmation dialog with warning message and confirm/cancel buttons in Phase-2-web-todo/frontend/src/components/tasks/DeleteConfirmModal.tsx
- [X] T064 [US6] Handle confirmed deletion with apiClient.deleteTask(userId, taskId) in Phase-2-web-todo/frontend/src/app/(dashboard)/tasks/page.tsx
- [X] T065 [US6] Remove task from local state immediately (optimistic update) after confirmation in Phase-2-web-todo/frontend/src/app/(dashboard)/tasks/page.tsx
- [X] T066 [US6] Handle API errors for delete operation (404, 401) in Phase-2-web-todo/frontend/src/app/(dashboard)/tasks/page.tsx
- [X] T067 [US6] Handle cancellation (close modal without deleting) in Phase-2-web-todo/frontend/src/components/tasks/DeleteConfirmModal.tsx

**Checkpoint**: All user stories should now be independently functional

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T068 [P] Add navigation header with logo and logout button to root layout in Phase-2-web-todo/frontend/src/app/layout.tsx
- [X] T069 [P] Create consistent color palette and typography system using Tailwind in Phase-2-web-todo/frontend/src/app/globals.css
- [X] T070 [P] Add proper meta tags and SEO metadata to root layout in Phase-2-web-todo/frontend/src/app/layout.tsx
- [X] T071 [P] Implement responsive design across all breakpoints (mobile <768px, tablet 768-1024px, desktop >1024px) in Phase-2-web-todo/frontend/src/app/(dashboard)/tasks/page.tsx
- [X] T072 [P] Ensure touch-friendly targets (min 44x44px) for mobile buttons in Phase-2-web-todo/frontend/src/components/tasks
- [X] T073 [P] Add visual feedback for all interactions (button states, loading indicators) in Phase-2-web-todo/frontend/src/components
- [X] T074 [P] Add accessibility attributes (ARIA labels, keyboard navigation support) to all forms and buttons in Phase-2-web-todo/frontend/src/components
- [X] T075 [P] Handle 401 Unauthorized errors globally with redirect to login in Phase-2-web-todo/frontend/src/lib/api-client.ts
- [X] T076 [P] Handle network errors with retry options across all components in Phase-2-web-todo/frontend/src/app/(dashboard)/tasks/page.tsx
- [X] T077 [P] Add timeout handling for API requests (>5s) with user feedback in Phase-2-web-todo/frontend/src/lib/api-client.ts
- [X] T078 Create landing page (app/page.tsx) with app description and links to login/signup in Phase-2-web-todo/frontend/src/app
- [X] T079 Update README.md with setup instructions and environment variables in Phase-2-web-todo/frontend
- [X] T080 Verify application runs successfully with `npm run dev` in Phase-2-web-todo/frontend
- [X] T081 Verify production build works with `npm run build` in Phase-2-web-todo/frontend
- [X] T082 Manual testing: Test all user stories and acceptance scenarios from spec.md in Phase-2-web-todo/frontend

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-8)**: All depend on Foundational phase completion
  - User Story 1 (P1): Authentication - No dependencies on other stories
  - User Story 2 (P1): Task List View - Depends on US1 (requires auth)
  - User Story 3 (P1): Create Task - Depends on US1, US2 (requires auth + list)
  - User Story 4 (P2): Toggle Completion - Depends on US2 (requires list display)
  - User Story 5 (P2): Edit Task - Depends on US2 (requires list display)
  - User Story 6 (P3): Delete Task - Depends on US2 (requires list display)
- **Polish (Phase 9)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1) - Authentication**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1) - Task List View**: Can start after Foundational (Phase 2) - Depends on US1 for auth redirection
- **User Story 3 (P1) - Create Task**: Can start after Foundational (Phase 2) - Depends on US1 (auth), US2 (list)
- **User Story 4 (P2) - Toggle Completion**: Can start after Foundational (Phase 2) - Depends on US2 (list display)
- **User Story 5 (P2) - Edit Task**: Can start after Foundational (Phase 2) - Depends on US2 (list display)
- **User Story 6 (P3) - Delete Task**: Can start after Foundational (Phase 2) - Depends on US2 (list display)

### Within Each User Story

- Setup before user stories
- Foundational before any story implementation
- Components before page integration
- Page implementation before Polish phase
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks (Phase 1) marked [P] can run in parallel (T001-T005)
- All Foundational tasks (Phase 2) marked [P] can run in parallel (T006-T014)
- Once Foundational phase completes, user stories can proceed in parallel by priority:
  - US1 (T015-T025) can be worked on in parallel with US2 (T026-T035)
  - US4 (T044-T050) and US5 (T051-T060) can be worked on in parallel after US3
  - US6 (T061-T067) can be worked on in parallel with US5
- All Polish tasks (Phase 9) marked [P] can run in parallel (T068-T079)

---

## Parallel Example: User Story 1

```bash
# Launch all UI components for User Story 1 together:
Task: "T015 Create signup page (app/(auth)/signup/page.tsx) with email/password form"
Task: "T016 Create login page (app/(auth)/login/page.tsx) with email/password form"

# Launch form implementation for User Story 1 together:
Task: "T017 Implement signup form with client-side validation"
Task: "T018 Implement login form with Better Auth integration"
Task: "T020 Implement logout functionality"
```

---

## Implementation Strategy

### MVP First (User Stories 1, 2, 3 Only)

1. Complete Phase 1: Setup (T001-T005)
2. Complete Phase 2: Foundational (T006-T014) - **CRITICAL - blocks all stories**
3. Complete Phase 3: User Story 1 - Authentication (T015-T025)
4. Complete Phase 4: User Story 2 - Task List View (T026-T035)
5. Complete Phase 5: User Story 3 - Create Task (T036-T043)
6. **STOP and VALIDATE**: Test all P1 stories independently
7. Deploy/demo if ready - **MVP COMPLETE**

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Validate auth flow
3. Add User Story 2 → Test independently → Validate task listing
4. Add User Story 3 → Test independently → Validate task creation
5. Deploy/Demo (MVP with P1 stories complete!)
6. Add User Story 4 → Test independently → Validate completion toggle
7. Add User Story 5 → Test independently → Validate task editing
8. Add User Story 6 → Test independently → Validate task deletion
9. Complete Phase 9: Polish → Final production-ready application
10. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (Phase 1-2)
2. Once Foundational is done:
   - Developer A: User Story 1 (Authentication)
   - Developer B: User Story 2 (Task List View) - can start after US1 auth is integrated
   - Developer C: User Story 3 (Create Task) - waits for US2 component
3. After P1 stories complete:
   - Developer A: User Story 4 (Toggle Completion)
   - Developer B: User Story 5 (Edit Task)
4. P3 story (Delete Task) can be worked on independently by Developer C
5. Polish phase completed by team

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- No tests included - feature spec did not explicitly request TDD approach
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- MVP includes P1 stories (US1, US2, US3)
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- Total tasks: 82
- Total phases: 9
- P1 MVP tasks: 43 (T001-T043)
- P2 tasks: 17 (T044-T060)
- P3 tasks: 7 (T061-T067)
- Polish tasks: 15 (T068-T082)
