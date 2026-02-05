---

description: "Task list for In-Memory Todo Console Application"
---

# Tasks: In-Memory Todo Console Application

**Input**: Design documents from `/specs/1-in-memory-todo-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project structure per implementation plan in todo-app/ directory
- [x] T002 [P] Initialize pyproject.toml with UV dependencies (typer, rich, pytest, black, ruff, mypy)
- [x] T003 [P] Create .python-version file with Python 3.13
- [x] T004 Create src/todo/__init__.py file
- [x] T005 Create tests/__init__.py file
- [x] T006 Create src/todo/models.py file
- [x] T007 Create src/todo/repository/__init__.py file
- [x] T008 Create src/todo/service/__init__.py file
- [x] T009 Create src/todo/cli/__init__.py file

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

Examples of foundational tasks (adjust based on your project):

- [x] T010 Implement core Todo domain model with required fields (id, title, description, status, created_at, updated_at) in src/todo/models.py
- [x] T011 [P] Implement core operations (create, list, get, update, delete, mark completed) in src/todo/service/todo_service.py
- [x] T012 [P] Setup error handling and input validation infrastructure with custom exceptions
- [x] T013 Create base models/entities that all stories depend on
- [x] T014 Configure logging and documentation infrastructure
- [x] T015 Setup environment configuration management with no persistence
- [x] T016 Implement in-memory repository interface in src/todo/repository/memory_repository.py
- [x] T017 Create main.py entry point with Typer app in src/todo/main.py
- [x] T018 Create CLI commands module in src/todo/cli/commands.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add New Todo (Priority: P1) 🎯 MVP

**Goal**: Enable users to add new todo items with title and optional description using the command `todo add "title" --description "desc"`

**Independent Test**: The application should allow a user to add a new todo with a title and optional description using the command `todo add "title" --description "desc"`, assign it an auto-incremented ID, set the status to "pending" by default, and store it in memory. The user should be able to see the newly added todo in subsequent list operations.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T019 [P] [US1] Contract test for add endpoint in tests/contract/test_add.py
- [ ] T020 [P] [US1] Integration test for add user journey in tests/integration/test_add_journey.py

### Implementation for User Story 1

- [x] T021 [P] [US1] Create Todo model in src/todo/models.py with validation for title length (1-150 chars)
- [x] T022 [P] [US1] Create MemoryRepository with add method in src/todo/repository/memory_repository.py
- [x] T023 [US1] Implement TodoService.create_todo in src/todo/service/todo_service.py with validation
- [x] T024 [US1] Implement add command in src/todo/cli/commands.py with Typer
- [x] T025 [US1] Add validation and error handling for title length in src/todo/service/todo_service.py
- [x] T026 [US1] Add logging for user story 1 operations in src/todo/cli/commands.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - View/List Todos (Priority: P1)

**Goal**: Enable users to view all their todos in a clean, readable format using the command `todo list`, with timestamps displayed in ISO 8601 format

**Independent Test**: The application should display all todos currently stored in memory in a well-formatted, readable way showing ID, title, description, status, and timestamps in ISO 8601 format.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T027 [P] [US2] Contract test for list endpoint in tests/contract/test_list.py
- [ ] T028 [P] [US2] Integration test for list user journey in tests/integration/test_list_journey.py

### Implementation for User Story 2

- [x] T029 [P] [US2] Extend MemoryRepository with get_all method in src/todo/repository/memory_repository.py
- [x] T030 [US2] Implement TodoService.get_all_todos in src/todo/service/todo_service.py with filtering and sorting
- [x] T031 [US2] Implement list command in src/todo/cli/commands.py with Rich formatting
- [x] T032 [US2] Add Rich table formatting for list view in src/todo/cli/commands.py
- [x] T033 [US2] Implement status badge coloring (green for completed, yellow for pending) in src/todo/cli/commands.py
- [x] T034 [US2] Add empty state handling with friendly message in src/todo/cli/commands.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Update Todo (Priority: P2)

**Goal**: Enable users to modify an existing todo's title or description using the command `todo update 1 --title "new title"`

**Independent Test**: The application should allow a user to update the title and/or description of an existing todo by its ID using the command `todo update 1 --title "new title"`, updating the `updated_at` timestamp while keeping other fields unchanged.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T035 [P] [US3] Contract test for update endpoint in tests/contract/test_update.py
- [ ] T036 [P] [US3] Integration test for update user journey in tests/integration/test_update_journey.py

### Implementation for User Story 3

- [x] T037 [P] [US3] Extend MemoryRepository with update method in src/todo/repository/memory_repository.py
- [x] T038 [US3] Implement TodoService.update_todo in src/todo/service/todo_service.py with validation
- [x] T039 [US3] Implement update command in src/todo/cli/commands.py with Typer
- [x] T040 [US3] Add validation for title length in update operation in src/todo/service/todo_service.py
- [x] T041 [US3] Ensure updated_at timestamp refreshes on update in src/todo/models.py

**Checkpoint**: At this point, User Stories 1, 2 AND 3 should all work independently

---

## Phase 6: User Story 4 - Delete Todo (Priority: P2)

**Goal**: Enable users to remove a todo from their list using the command `todo delete 1`

**Independent Test**: The application should allow a user to delete an existing todo by its ID using the command `todo delete 1`, removing it from memory.

### Tests for User Story 4 (OPTIONAL - only if tests requested) ⚠️

- [ ] T042 [P] [US4] Contract test for delete endpoint in tests/contract/test_delete.py
- [ ] T043 [P] [US4] Integration test for delete user journey in tests/integration/test_delete_journey.py

### Implementation for User Story 4

- [x] T044 [P] [US4] Extend MemoryRepository with delete method in src/todo/repository/memory_repository.py
- [x] T045 [US4] Implement TodoService.delete_todo in src/todo/service/todo_service.py
- [x] T046 [US4] Implement delete command in src/todo/cli/commands.py with Typer
- [x] T047 [US4] Add error handling for non-existent todo ID in src/todo/service/todo_service.py

**Checkpoint**: At this point, User Stories 1, 2, 3 AND 4 should all work independently

---

## Phase 7: User Story 5 - Mark Todo as Complete (Priority: P2)

**Goal**: Enable users to mark a todo as completed using the command `todo complete 1`, and allow reopening completed todos

**Independent Test**: The application should allow a user to change a todo's status from "pending" to "completed" by its ID using the command `todo complete 1`, updating the `updated_at` timestamp. The application should also allow users to mark completed todos as pending again.

### Tests for User Story 5 (OPTIONAL - only if tests requested) ⚠️

- [ ] T048 [P] [US5] Contract test for complete endpoint in tests/contract/test_complete.py
- [ ] T049 [P] [US5] Integration test for complete user journey in tests/integration/test_complete_journey.py

### Implementation for User Story 5

- [x] T050 [P] [US5] Extend MemoryRepository with mark_complete and mark_pending methods in src/todo/repository/memory_repository.py
- [x] T051 [US5] Implement TodoService.mark_todo_complete and mark_todo_pending in src/todo/service/todo_service.py
- [x] T052 [US5] Implement complete command in src/todo/cli/commands.py with Typer
- [x] T053 [US5] Implement update command to support status changes in src/todo/cli/commands.py
- [x] T054 [US5] Add status transition validation in src/todo/service/todo_service.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T055 [P] Documentation updates in README.md with installation and usage examples
- [x] T056 Code cleanup and refactoring while preserving 90%+ of business/domain logic
- [x] T057 Performance optimization across all stories to meet <50ms response time
- [x] T058 [P] Additional unit tests (if requested) in tests/unit/
- [x] T059 Security hardening with no hard-coded secrets
- [x] T060 Run quickstart.md validation to ensure setup instructions work
- [x] T061 Verify compliance with constitution principles (progressive enhancement, technology discipline, etc.)
- [x] T062 Add detailed help text to all commands in src/todo/cli/commands.py
- [x] T063 Implement detailed error messages with specific guidance for users in src/todo/cli/commands.py
- [x] T064 Add timestamp formatting in ISO 8601 format throughout the application
- [x] T065 Add type hints throughout the codebase for mypy compatibility

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **User Story 4 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1/US2/US3 but should be independently testable
- **User Story 5 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1-US4 but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
T019 [P] [US1] Contract test for add endpoint in tests/contract/test_add.py
T020 [P] [US1] Integration test for add user journey in tests/integration/test_add_journey.py

# Launch all models for User Story 1 together:
T021 [P] [US1] Create Todo model in src/todo/models.py with validation for title length (1-150 chars)
T022 [P] [US1] Create MemoryRepository with add method in src/todo/repository/memory_repository.py
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Add User Story 5 → Test independently → Deploy/Demo
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together focusing on core domain model and operations
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
   - Developer E: User Story 5
3. Stories complete and integrate independently while adhering to constitution principles

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable while maintaining core domain logic
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Maintain 90%+ business/domain logic compatibility across phases
- Ensure backward compatibility of the core Todo model
- Follow technology discipline: use ONLY the exact tools and stack listed for this phase
- Document all design decisions in README and inline comments
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence