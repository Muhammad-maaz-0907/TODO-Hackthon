# Quickstart Guide: In-Memory Todo Console Application

## Prerequisites
- Python 3.13+
- UV package manager

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd todo-app
   ```

2. Install dependencies using UV:
   ```bash
   uv sync
   ```

3. Install the package in development mode:
   ```bash
   uv build
   uv install --editable .
   ```

## Usage

Once installed, you can use the `todo` command from anywhere in your terminal:

### Adding a new todo
```bash
todo add "Buy groceries" --description "Milk and bread"
```

### Listing all todos
```bash
todo list
```

Filter by status:
```bash
todo list --status pending
todo list --status completed
```

Sort the list:
```bash
todo list --sort created
todo list --sort title
```

### Viewing a specific todo
```bash
todo show 1
```

### Updating a todo
```bash
todo update 1 --title "Buy food" --description "Milk, bread, and eggs"
todo update 1 --status completed
```

### Marking a todo as complete
```bash
todo complete 1
```

### Deleting a todo
```bash
todo delete 1
```

### Getting help
```bash
todo --help
todo add --help
todo list --help
```

## Development

1. Set up the development environment:
   ```bash
   uv sync --dev
   ```

2. Run tests:
   ```bash
   uv run pytest
   ```

3. Format code:
   ```bash
   uv run black src/
   uv run ruff check src/ --fix
   ```

4. Type checking:
   ```bash
   uv run mypy src/
   ```

## Architecture Overview

The application follows a layered architecture:

- **Models** (`src/todo/models.py`): Defines the Todo dataclass
- **Repository** (`src/todo/repository/memory_repository.py`): Handles data storage and retrieval
- **Service** (`src/todo/service/todo_service.py`): Implements business logic
- **CLI** (`src/todo/cli/commands.py`): Handles user input and output formatting

This structure ensures separation of concerns and makes the application easy to test and maintain.