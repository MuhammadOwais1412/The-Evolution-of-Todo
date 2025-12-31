# Tasks: Python Console Todo App

**Input**: Design documents from `/specs/1-python-todo-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), data-model.md, contracts/

**Tests**: Included - tests are explicitly required by the specification

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Initialize project with UV package manager - run `uv init` to create project structure and pyproject.toml
- [X] T002 Create project directory structure `src/` and `tests/` (UV already creates these, verify they exist)
- [X] T003 Create `src/__init__.py` to make src a Python package
- [X] T004 Create `tests/__init__.py` to make tests a Python package
- [X] T005 Configure `pyproject.toml` with Python 3.13+ requirement, project metadata, and hatchling build backend

**Checkpoint**: Project structure ready, Python can import from src/

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**CRITICAL**: No user story work can begin until this phase is complete

- [X] T006 [US1] [US2] [US3] [US4] Create Task dataclass in `src/task.py` with id, title, description, completed fields
- [X] T007 [US1] [US2] [US3] [US4] Create TaskService class in `src/task.py` with __init__, add, list, get methods
- [X] T008 [US1] [US2] [US3] [US4] Add TaskService update method in `src/task.py` for modifying task title and/or description
- [X] T009 [US1] [US2] [US3] [US4] Add TaskService delete method in `src/task.py` for removing tasks by ID
- [X] T010 [US1] [US2] [US3] [US4] Add TaskService toggle method in `src/task.py` for switching completion status

**Checkpoint**: Task model complete - all user stories can now proceed

---

## Phase 3: User Story 1 - Add and View Tasks (Priority: P1)

**Goal**: Users can add tasks with title/description and view all tasks in a formatted list

**Independent Test**: Run `python src/main.py`, select "Add Task" 3 times, verify all 3 tasks appear in "View Tasks" with correct IDs, titles, descriptions, and incomplete status

### Tests for User Story 1

> Write these tests FIRST, ensure they FAIL before implementation

- [X] T011 [P] [US1] Write unit test for TaskService.add() in `tests/test_task.py` - verify task creation with title and description, ID assignment, default incomplete status
- [X] T012 [P] [US1] Write unit test for TaskService.add() validation - verify empty title raises ValueError in `tests/test_task.py`
- [X] T013 [P] [US1] Write unit test for TaskService.list() in `tests/test_task.py` - verify empty list returns [], populated list returns all tasks
- [X] T014 [P] [US1] Write unit test for TaskService.get() in `tests/test_task.py` - verify task retrieval by ID, non-existent ID returns None

### Implementation for User Story 1

- [X] T015 [US1] Implement UI module in `src/ui.py` with show_menu() function displaying 7 menu options
- [X] T016 [US1] Implement get_choice() function in `src/ui.py` - reads menu choice, validates 1-7, handles invalid input
- [X] T017 [US1] Implement prompt_task_data() function in `src/ui.py` - prompts for title (validates non-empty) and optional description
- [X] T018 [US1] Implement show_tasks() function in `src/ui.py` - displays formatted table with ID, Title, Description, Status columns
- [X] T019 [US1] Implement Add Task operation in `src/main.py` - connects menu choice 1 to TaskService.add() and displays success message
- [X] T020 [US1] Implement View Tasks operation in `src/main.py` - connects menu choice 2 to TaskService.list() and shows formatted task list

**Checkpoint**: User Story 1 complete - can add tasks and view them

---

## Phase 4: User Story 2 - Update and Delete Tasks (Priority: P1)

**Goal**: Users can modify task details and remove tasks from the list

**Independent Test**: Add a task, update its title/description, verify changes in View Tasks, delete it, verify it's removed from list

### Tests for User Story 2

> Write these tests FIRST, ensure they FAIL before implementation

- [X] T021 [P] [US2] Write unit test for TaskService.update() in `tests/test_task.py` - verify title and description updates
- [X] T022 [P] [US2] Write unit test for TaskService.update() validation - verify empty title raises ValueError in `tests/test_task.py`
- [X] T023 [P] [US2] Write unit test for TaskService.delete() in `tests/test_task.py` - verify task removal, remaining tasks unaffected
- [X] T024 [P] [US2] Write unit test for TaskService.delete() error handling - verify non-existent ID raises KeyError

### Implementation for User Story 2

- [X] T025 [US2] Implement prompt_task_id() function in `src/ui.py` - prompts for task ID, validates positive integer
- [X] T026 [US2] Implement prompt_update_data() function in `src/ui.py` - prompts for new title/description (both optional)
- [X] T027 [US2] Implement Update Task operation in `src/main.py` - connects menu choice 3 to TaskService.update() with error handling for non-existent ID
- [X] T028 [US2] Implement Delete Task operation in `src/main.py` - connects menu choice 4 to TaskService.delete() with error handling for non-existent ID

**Checkpoint**: User Story 2 complete - can update and delete tasks

---

## Phase 5: User Story 3 - Manage Task Completion (Priority: P1)

**Goal**: Users can mark tasks as complete or incomplete

**Independent Test**: Add a task, mark it complete, verify status shows "Complete", mark it incomplete, verify status shows "Incomplete"

### Tests for User Story 3

> Write these tests FIRST, ensure they FAIL before implementation

- [X] T029 [P] [US3] Write unit test for TaskService.toggle() in `tests/test_task.py` - verify incomplete→complete and complete→incomplete transitions
- [X] T030 [P] [US3] Write unit test for TaskService.toggle() error handling - verify non-existent ID raises KeyError

### Implementation for User Story 3

- [X] T031 [US3] Implement Mark Complete operation in `src/main.py` - connects menu choice 5 to TaskService.toggle() with success message "marked as complete"
- [X] T032 [US3] Implement Mark Incomplete operation in `src/main.py` - connects menu choice 6 to TaskService.toggle() with success message "marked as incomplete"
- [X] T033 [US3] Update show_tasks() in `src/ui.py` to display "Complete" or "Incomplete" based on task.completed boolean

**Checkpoint**: User Story 3 complete - can toggle completion status

---

## Phase 6: User Story 4 - Error Handling (Priority: P2)

**Goal**: Users receive clear, helpful feedback for all error scenarios

**Independent Test**: Enter invalid menu choices, non-existent task IDs, empty titles - verify appropriate error messages without crashes

### Tests for User Story 4

> Write these tests FIRST, ensure they FAIL before implementation

- [X] T034 [P] [US4] Write integration test for invalid menu choice in `tests/test_ui.py` - verify "Invalid choice" message
- [X] T035 [P] [US4] Write integration test for empty task list view in `tests/test_ui.py` - verify "No tasks available" message
- [X] T036 [P] [US4] Write integration test for update on non-existent ID in `tests/test_ui.py` - verify "Task with ID X not found" message
- [X] T037 [P] [US4] Write integration test for delete on non-existent ID in `tests/test_ui.py` - verify "Task with ID X not found" message
- [X] T038 [P] [US4] Write integration test for toggle on non-existent ID in `tests/test_ui.py` - verify "Task with ID X not found" message
- [X] T039 [P] [US4] Write integration test for empty title validation in `tests/test_ui.py` - verify "Title cannot be empty" message and re-prompt

### Implementation for User Story 4

- [X] T040 [US4] Add ANSI color codes to `src/ui.py` - BLUE for headers, GREEN for success, RED for errors
- [X] T041 [US4] Implement success() function in `src/ui.py` - displays green success messages
- [X] T042 [US4] Implement error() function in `src/ui.py` - displays red error messages
- [X] T043 [US4] Implement header() function in `src/ui.py` - displays blue/bold section headers
- [X] T044 [US4] Add Exit operation in `src/main.py` - connects menu choice 7 to terminate application with "Goodbye!" message

**Checkpoint**: User Story 4 complete - all error scenarios handled gracefully

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final verification and documentation

- [X] T045 [P] Run full test suite with `pytest --cov` - verify >90% coverage on src/task.py
- [X] T046 [P] Run integration test - complete full workflow: add 3 tasks, mark 1 complete, update 1, delete 1, view remaining
- [X] T047 Verify `python -m py_compile src/*.py` passes without errors
- [X] T048 Verify application runs without crashes for all valid and invalid inputs
- [X] T049 Update README.md with setup instructions per quickstart.md

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phases 3-6)**: All depend on Foundational phase completion
  - User stories can proceed in parallel (if staffed) or sequentially
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Phase 2 - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Phase 2 - No dependencies on other stories
- **User Story 3 (P3)**: Can start after Phase 2 - No dependencies on other stories
- **User Story 4 (P2)**: Can start after Phase 2 - No dependencies on other stories

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- UI components can be implemented in any order within the story
- Story complete before moving to Polish phase

### Parallel Opportunities

- All Setup tasks (T001-T005) can run in parallel
- All Foundational tasks (T006-T010) can run in parallel (TaskService methods are in same file)
- Tests for different user stories can be written in parallel
- Once Foundational is complete, all user stories can start in parallel

---

## Parallel Example

```bash
# Run these tasks in parallel (different files, no dependencies):
Task T011: Write test for TaskService.add() in tests/test_task.py
Task T021: Write test for TaskService.update() in tests/test_task.py
Task T029: Write test for TaskService.toggle() in tests/test_task.py

# Then run these in parallel:
Task T015: Implement UI module show_menu() in src/ui.py
Task T016: Implement get_choice() in src/ui.py
Task T017: Implement prompt_task_data() in src/ui.py
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Add tasks and view them
5. Deploy/demo if ready for early feedback

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Polish → Final release

---

## Notes

- **[P] tasks**: Different files, no dependencies on incomplete tasks
- **[Story] label**: Maps task to specific user story for traceability
- Each user story should be independently completable and testable
- **Write tests FIRST** for each user story, ensure they fail, then implement
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
