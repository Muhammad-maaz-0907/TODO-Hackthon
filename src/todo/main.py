import typer

from .repository.memory_repository import MemoryTodoRepository
from .service.todo_service import TodoService

# Create global instances
repository = MemoryTodoRepository()
service = TodoService(repository)

# Import the app after initializing service to avoid circular import
from .cli.commands import app