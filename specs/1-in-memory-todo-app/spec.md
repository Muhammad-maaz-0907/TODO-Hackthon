# Feature Specification: In-Memory Todo Console Application

**Feature Branch**: `1-in-memory-todo-app`
**Created**: 2026-02-05
**Status**: Draft
**Input**: User description: "Project: Phase I - In-Memory Todo Console Application Objective: Build a clean, user-friendly, command-line based Todo app that stores all data in memory (no files, no database). Target: Basic Level Functionality (MVP) Core Requirements: Must implement **all 5 features** perfectly: - Add a new todo - View / List all todos - Update a todo (title + description) - Delete a todo by ID - Mark todo as Complete Domain Model (Todo Item): - id: int (auto-increment starting from 1) - title: str (required, max 150 chars) - description: str (optional) - status: str → \"pending\" | \"completed\" (default: \"pending\") - created_at: datetime - updated_at: datetime (auto-updated on change) Technical Constraints: - Python 3.13+ - Package manager: UV only - Use modern Python project structure (`src/` layout) - Dependencies allowed: **Typer** + **Rich** (for beautiful CLI) - No other external dependencies - No file I/O, no database, no pickle — pure in-memory only Development Approach (Mandatory): Follow strict **Agentic Dev Stack** workflow: 1. Write detailed spec 2. Create implementation plan 3. Break into small tasks 4. Generate code iteratively using Claude Code → Zero manual coding allowed Project Structure: Use clean, scalable structure:"

## Clarifications

### Session 2026-02-05

- Q: What CLI command format should be used? → A: Standard format: `todo add "title" --description "desc"`, `todo list`, `todo update 1 --title "new title"`, `todo delete 1`, `todo complete 1`
- Q: How should errors be handled? → A: Detailed error messages with specific guidance for users (e.g., "Error: Todo with ID 5 not found. Use 'todo list' to see available todos.")
- Q: How should empty states be displayed? → A: Friendly message with guidance on how to add a new todo (e.g., "No todos yet! Add one with: todo add 'your task'")
- Q: Should users be able to mark completed todos as pending again? → A: Allow users to mark completed todos as pending again (reopening functionality)
- Q: What format should be used for timestamps? → A: ISO 8601 format (YYYY-MM-DD HH:MM:SS) for consistency and readability

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Add New Todo (Priority: P1)

A user wants to add a new todo item to their list. They run the application and use the add command to create a new todo with a title and optional description.

**Why this priority**: This is the foundational functionality that allows users to create todos, which is the core purpose of the application.

**Independent Test**: The application should allow a user to add a new todo with a title and optional description using the command `todo add "title" --description "desc"`, assign it an auto-incremented ID, set the status to "pending" by default, and store it in memory. The user should be able to see the newly added todo in subsequent list operations.

**Acceptance Scenarios**:

1. **Given** a fresh application with no todos, **When** a user runs `todo add "Buy groceries"`, **Then** a new todo with ID 1, title "Buy groceries", status "pending", and current timestamps in ISO 8601 format is stored in memory
2. **Given** an application with existing todos, **When** a user runs `todo add "Complete project" --description "Finish the todo app"`, **Then** a new todo with incremented ID, title "Complete project", description "Finish the todo app", status "pending", and current timestamps in ISO 8601 format is stored in memory

---

### User Story 2 - View/List Todos (Priority: P1)

A user wants to view all their todos in a clean, readable format. They run the list command to see all todos with their details.

**Why this priority**: This is essential for users to see their todos and track their tasks, making it equally important as adding todos.

**Independent Test**: The application should display all todos currently stored in memory in a well-formatted, readable way showing ID, title, description, status, and timestamps in ISO 8601 format.

**Acceptance Scenarios**:

1. **Given** an application with multiple todos in memory, **When** a user runs `todo list`, **Then** all todos are displayed with their ID, title, description, status, and timestamps in ISO 8601 format in a clean format
2. **Given** an application with no todos in memory, **When** a user runs `todo list`, **Then** a friendly message is displayed indicating no todos exist with guidance on how to add a new todo (e.g., "No todos yet! Add one with: todo add 'your task'")

---

### User Story 3 - Update Todo (Priority: P2)

A user wants to modify an existing todo's title or description. They run the update command specifying the todo ID and the new values.

**Why this priority**: Allows users to refine and modify their todos as their plans change, improving the utility of the application.

**Independent Test**: The application should allow a user to update the title and/or description of an existing todo by its ID using the command `todo update 1 --title "new title"`, updating the `updated_at` timestamp while keeping other fields unchanged.

**Acceptance Scenarios**:

1. **Given** a todo with ID 1 and title "Old title", **When** a user runs `todo update 1 --title "New title"`, **Then** the todo's title is updated to "New title" and the `updated_at` timestamp in ISO 8601 format is refreshed
2. **Given** a todo with ID 2 and description "Old description", **When** a user runs `todo update 2 --description "New description"`, **Then** the todo's description is updated to "New description" and the `updated_at` timestamp in ISO 8601 format is refreshed

---

### User Story 4 - Delete Todo (Priority: P2)

A user wants to remove a todo from their list. They run the delete command specifying the todo ID.

**Why this priority**: Essential for managing the todo list by removing completed or unwanted items.

**Independent Test**: The application should allow a user to delete an existing todo by its ID using the command `todo delete 1`, removing it from memory.

**Acceptance Scenarios**:

1. **Given** a todo with ID 1 exists in memory, **When** a user runs `todo delete 1`, **Then** the todo is removed from memory and subsequent list operations do not show it
2. **Given** no todo with ID 99 exists in memory, **When** a user runs `todo delete 99`, **Then** a detailed error message is displayed with specific guidance for users (e.g., "Error: Todo with ID 99 not found. Use 'todo list' to see available todos.")

---

### User Story 5 - Mark Todo as Complete (Priority: P2)

A user wants to mark a todo as completed. They run the complete command specifying the todo ID.

**Why this priority**: Allows users to track their progress and mark tasks as done, which is a core functionality of any todo application.

**Independent Test**: The application should allow a user to change a todo's status from "pending" to "completed" by its ID using the command `todo complete 1`, updating the `updated_at` timestamp. The application should also allow users to mark completed todos as pending again.

**Acceptance Scenarios**:

1. **Given** a todo with ID 1 and status "pending", **When** a user runs `todo complete 1`, **Then** the todo's status is updated to "completed" and the `updated_at` timestamp in ISO 8601 format is refreshed
2. **Given** a todo with ID 2 and status "completed", **When** a user runs `todo complete 2`, **Then** the todo's status remains "completed" and the `updated_at` timestamp in ISO 8601 format is refreshed
3. **Given** a todo with ID 3 and status "completed", **When** a user runs `todo update 3 --status pending` (or equivalent command to reopen), **Then** the todo's status is updated to "pending" and the `updated_at` timestamp in ISO 8601 format is refreshed

---

### Edge Cases

- What happens when trying to update/delete/mark complete a non-existent todo ID? (Should show detailed error message with specific guidance for users)
- How does the system handle titles longer than 150 characters? (Should show appropriate error message)
- What happens when the application is restarted? (Should be no data persisted since it's in-memory only)
- How does the system handle invalid date/time formats? (Should show appropriate error message)
- How should empty states be displayed? (Should show friendly message with guidance on how to add a new todo)
- Should users be able to mark completed todos as pending again? (Yes, reopening functionality should be available)

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST implement the core Todo domain model with required fields (id, title, description, status, created_at, updated_at)
- **FR-002**: System MUST support all core operations (create, list, get, update, delete, mark completed)
- **FR-003**: System MUST maintain 90%+ of business/domain logic compatibility with previous phases
- **FR-004**: System MUST follow the technology stack specified for this phase without deviations
- **FR-005**: System MUST implement proper error handling and input validation
- **FR-006**: System MUST document all design decisions in README and inline comments
- **FR-007**: System MUST maintain consistent user mental model with familiar core commands/operations
- **FR-008**: System MUST store all data in memory only with no file I/O, database, or pickle
- **FR-009**: System MUST use auto-incrementing integer IDs starting from 1 for todos
- **FR-010**: System MUST set default status to "pending" for new todos
- **FR-011**: System MUST update the `updated_at` timestamp whenever a todo is modified
- **FR-012**: System MUST validate that titles are no longer than 150 characters
- **FR-013**: System MUST use only Typer and Rich dependencies as specified
- **FR-014**: System MUST use standard CLI command format: `todo add "title" --description "desc"`, `todo list`, `todo update 1 --title "new title"`, `todo delete 1`, `todo complete 1`
- **FR-015**: System MUST display detailed error messages with specific guidance for users
- **FR-016**: System MUST display friendly message with guidance on how to add a new todo when no todos exist
- **FR-017**: System MUST allow users to mark completed todos as pending again (reopening functionality)
- **FR-018**: System MUST display timestamps in ISO 8601 format (YYYY-MM-DD HH:MM:SS)

### Key Entities *(include if feature involves data)*

- **Todo**: Represents a single todo item with id (int), title (str, max 150 chars), description (str, optional), status (str: "pending"|"completed", default: "pending"), created_at (datetime), updated_at (datetime)

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can add new todos with title and optional description in under 5 seconds using `todo add "title" --description "desc"`
- **SC-002**: Users can view all todos in a well-formatted, readable list within 2 seconds using `todo list`, with timestamps displayed in ISO 8601 format
- **SC-003**: Users can update existing todos (title/description) in under 5 seconds using `todo update 1 --title "new title"`
- **SC-004**: Users can delete todos by ID in under 3 seconds using `todo delete 1`
- **SC-005**: Users can mark todos as complete in under 3 seconds using `todo complete 1`
- **SC-006**: 95% of user operations (add/update/delete/complete) complete successfully without errors
- **SC-007**: All data remains in memory during application runtime and is lost upon restart (as intended)
- **SC-008**: All error conditions are handled gracefully with detailed error messages that provide specific guidance for users
- **SC-009**: When no todos exist, a friendly message with guidance on how to add a new todo is displayed
- **SC-010**: Users can mark completed todos as pending again (reopening functionality) with `todo update 1 --status pending` (or equivalent command)