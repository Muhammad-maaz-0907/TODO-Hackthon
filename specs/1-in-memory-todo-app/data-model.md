# Data Model: In-Memory Todo Console Application

## Todo Entity

### Fields
- **id**: int (auto-increment starting from 1)
  - Unique identifier for each todo
  - Generated automatically by the repository layer
- **title**: str (required, max 150 chars)
  - The main text of the todo
  - Must be provided when creating a new todo
- **description**: str (optional)
  - Additional details about the todo
  - Can be empty or None
- **status**: str (values: "pending" | "completed", default: "pending")
  - Current state of the todo
  - Default to "pending" when creating a new todo
- **created_at**: datetime
  - Timestamp when the todo was created
  - Set automatically when creating a new todo
- **updated_at**: datetime
  - Timestamp when the todo was last modified
  - Updated automatically when modifying a todo

### Relationships
- No relationships with other entities (standalone entity)

### Validation Rules
- Title must be provided and not empty
- Title length must be between 1 and 150 characters inclusive
- Status must be either "pending" or "completed"
- ID must be a positive integer
- created_at and updated_at must be valid datetime objects

### State Transitions
- From "pending" to "completed" (when marking as complete)
- From "completed" to "pending" (when reopening)
- Any field can be updated while maintaining the same ID
- updated_at timestamp is updated on any modification

## Repository Interface

### Methods
- **add(todo: Todo) -> Todo**
  - Adds a new todo to storage
  - Assigns a new ID if the todo doesn't have one
  - Sets created_at and updated_at timestamps
  - Returns the saved todo with assigned ID
- **get_by_id(todo_id: int) -> Todo | None**
  - Retrieves a todo by its ID
  - Returns None if not found
- **get_all() -> List[Todo]**
  - Retrieves all todos in storage
  - Returns an empty list if no todos exist
- **update(todo_id: int, **updates) -> Todo | None**
  - Updates fields of an existing todo
  - Updates the updated_at timestamp
  - Returns the updated todo or None if not found
- **delete(todo_id: int) -> bool**
  - Removes a todo from storage
  - Returns True if deletion was successful, False if not found
- **mark_complete(todo_id: int) -> Todo | None**
  - Marks a todo as completed
  - Updates the updated_at timestamp
  - Returns the updated todo or None if not found
- **mark_pending(todo_id: int) -> Todo | None**
  - Marks a completed todo as pending again
  - Updates the updated_at timestamp
  - Returns the updated todo or None if not found