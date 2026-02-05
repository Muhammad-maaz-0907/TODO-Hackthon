# API Contract: Todo Console Application

## Overview
This document outlines the functional contracts for the Todo Console Application. These represent the expected behaviors and interfaces that each component should implement.

## CLI Commands Contract

### `todo add`
**Purpose**: Add a new todo item
**Signature**: `todo add <title> [--description DESC]`
**Parameters**:
- `title` (required): The title of the new todo (string, 1-150 characters)
- `--description` (optional): Additional details about the todo (string)

**Returns**: Success message with the created todo's ID
**Errors**: 
- ValidationError if title exceeds 150 characters
- ValidationError if title is empty

### `todo list`
**Purpose**: List all todo items
**Signature**: `todo list [--status STATUS] [--sort SORT_FIELD]`
**Parameters**:
- `--status` (optional): Filter todos by status (values: "pending", "completed", "all")
- `--sort` (optional): Sort todos by field (values: "created", "title", "status")

**Returns**: Formatted table of todos or friendly message if no todos exist
**Errors**: None

### `todo show`
**Purpose**: Show details of a specific todo
**Signature**: `todo show <id>`
**Parameters**:
- `id` (required): The ID of the todo to show (integer)

**Returns**: Detailed information about the specified todo
**Errors**: 
- TodoNotFoundError if ID doesn't exist

### `todo update`
**Purpose**: Update fields of an existing todo
**Signature**: `todo update <id> [--title TITLE] [--description DESC] [--status STATUS]`
**Parameters**:
- `id` (required): The ID of the todo to update (integer)
- `--title` (optional): New title for the todo (string, 1-150 characters)
- `--description` (optional): New description for the todo (string)
- `--status` (optional): New status for the todo (values: "pending", "completed")

**Returns**: Success message with updated todo information
**Errors**:
- TodoNotFoundError if ID doesn't exist
- ValidationError if title exceeds 150 characters

### `todo delete`
**Purpose**: Delete a specific todo
**Signature**: `todo delete <id>`
**Parameters**:
- `id` (required): The ID of the todo to delete (integer)

**Returns**: Success message confirming deletion
**Errors**:
- TodoNotFoundError if ID doesn't exist

### `todo complete`
**Purpose**: Mark a specific todo as completed
**Signature**: `todo complete <id>`
**Parameters**:
- `id` (required): The ID of the todo to mark as complete (integer)

**Returns**: Success message confirming completion
**Errors**:
- TodoNotFoundError if ID doesn't exist

## Internal Component Contracts

### Todo Model Contract
**Responsibilities**:
- Represent a single todo item with all required fields
- Validate field constraints (title length, status values)
- Automatically manage timestamps (created_at, updated_at)

**Fields**:
- `id`: int (positive integer, auto-generated)
- `title`: str (1-150 characters, required)
- `description`: str (optional)
- `status`: str ("pending" or "completed", default: "pending")
- `created_at`: datetime (auto-set on creation)
- `updated_at`: datetime (auto-updated on modification)

### Repository Contract
**Responsibilities**:
- Manage storage and retrieval of todos
- Handle ID generation
- Provide CRUD operations
- Handle in-memory storage implementation

**Methods**:
- `add(todo: Todo) -> Todo`: Add a new todo
- `get_by_id(todo_id: int) -> Optional[Todo]`: Retrieve a todo by ID
- `get_all() -> List[Todo]`: Retrieve all todos
- `update(todo_id: int, **updates) -> Optional[Todo]`: Update a todo
- `delete(todo_id: int) -> bool`: Delete a todo
- `mark_complete(todo_id: int) -> Optional[Todo]`: Mark a todo as complete
- `mark_pending(todo_id: int) -> Optional[Todo]`: Mark a completed todo as pending again

### Service Contract
**Responsibilities**:
- Implement business logic and validation
- Coordinate between repository and presentation layers
- Handle error cases appropriately

**Methods**:
- `create_todo(title: str, description: str = None) -> Todo`: Create a new todo
- `get_todo(todo_id: int) -> Todo`: Get a specific todo
- `get_all_todos(status_filter: str = None, sort_field: str = None) -> List[Todo]`: Get all todos with optional filtering
- `update_todo(todo_id: int, **updates) -> Todo`: Update a todo
- `delete_todo(todo_id: int) -> bool`: Delete a todo
- `mark_todo_complete(todo_id: int) -> Todo`: Mark a todo as complete
- `mark_todo_pending(todo_id: int) -> Todo`: Mark a completed todo as pending again