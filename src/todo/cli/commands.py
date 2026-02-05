import typer
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from datetime import datetime

from ..models import Todo
from ..service.todo_service import TodoService
from ..repository.memory_repository import MemoryTodoRepository

# Create service instance locally to avoid circular import
repository = MemoryTodoRepository()
service = TodoService(repository)

console = Console()

# Custom exceptions
class TodoNotFoundError(Exception):
    """Raised when a todo with a specified ID is not found."""
    pass

class ValidationError(Exception):
    """Raised when input validation fails."""
    pass

def create_todo_output(todo: Todo) -> str:
    """Create a formatted output string for a todo."""
    status_symbol = "X" if todo.status == "completed" else "O"
    return f"{status_symbol} [{todo.id}] {todo.title}\n   Description: {todo.description or 'None'}\n   Status: {todo.status}\n   Created: {todo.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n   Updated: {todo.updated_at.strftime('%Y-%m-%d %H:%M:%S')}"

app = typer.Typer(
    no_args_is_help=True,
    add_completion=False,
    help="A simple, in-memory todo application.\n\n"
         "Note: All todos are stored in memory only and will be lost when the command finishes.\n"
         "Each command runs independently, so data doesn't persist between commands."
)

@app.command(help="Add a new todo item to the in-memory list.")
def add(
    title: str = typer.Argument(..., help="The title of the new todo (1-150 characters)"),
    description: Optional[str] = typer.Option(None, "--description", "-d", help="Additional details about the todo")
):
    """
    Add a new todo item.

    Example: todo add "Buy groceries" --description "Milk and bread"

    Note: This todo will be stored in memory only and will be lost when the command finishes.
    Each command runs independently, so data doesn't persist between commands.
    """
    try:
        new_todo = service.create_todo(title=title, description=description)
        console.print(f"[green]SUCCESS: Todo added![/green]")
        console.print(create_todo_output(new_todo))
        console.print("\n[yellow]Note: This todo is stored in memory only and will be lost when the command finishes.[/yellow]")
        console.print("[yellow]Each command runs independently, so data doesn't persist between commands.[/yellow]")
    except ValueError as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        console.print("[yellow]Hint: Title must be between 1 and 150 characters.[/yellow]")
    except Exception as e:
        console.print(f"[red]Unexpected error: {str(e)}[/red]")

@app.command(help="List all todo items in the in-memory list.")
def list_todos(
    status: Optional[str] = typer.Option(None, "--status", help="Filter todos by status (pending, completed, all)"),
    sort: Optional[str] = typer.Option(None, "--sort", help="Sort todos by field (created, title, status)")
):
    """
    List all todo items.

    Example: todo list-todos
    Example: todo list-todos --status pending
    Example: todo list-todos --sort title

    Note: This shows todos stored in memory only. Each command runs independently,
    so data doesn't persist between commands.
    """
    try:
        todos = service.get_all_todos(status_filter=status, sort_field=sort)

        if not todos:
            console.print(Panel(
                "[yellow]No todos in memory![/yellow]\n\n"
                "Add a new todo with: [bold]todo add 'your task'[/bold]\n\n"
                "[dim]Note: Todos are stored in memory only and will be lost when the command finishes.[/dim]",
                title="Todo List"
            ))
            return

        table = Table(title="Todo List")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Title", style="magenta")
        table.add_column("Description", style="green")
        table.add_column("Status", style="bold")
        table.add_column("Created", style="blue")

        for todo in todos:
            status_style = "green" if todo.status == "completed" else "yellow"
            table.add_row(
                str(todo.id),
                todo.title,
                todo.description or "",
                f"[{status_style}]{todo.status}[/]",
                todo.created_at.strftime('%Y-%m-%d %H:%M:%S')
            )

        console.print(table)
        console.print("\n[dim]Note: Todos are stored in memory only and will be lost when the command finishes.[/dim]")
        console.print("[dim]Each command runs independently, so data doesn't persist between commands.[/dim]")
    except Exception as e:
        console.print(f"[red]Error listing todos: {str(e)}[/red]")
        console.print("[yellow]Note: This command runs independently, so data doesn't persist between commands.[/yellow]")

@app.command(help="Show details of a specific todo by ID.")
def show(todo_id: int = typer.Argument(..., help="The ID of the todo to show")):
    """
    Show details of a specific todo.

    Example: todo show 1

    Note: This shows todos stored in memory only. Each command runs independently,
    so data doesn't persist between commands.
    """
    try:
        todo = service.get_todo(todo_id)
        console.print(Panel(create_todo_output(todo), title=f"Todo #{todo.id}"))
        console.print("\n[dim]Note: Todos are stored in memory only and will be lost when the command finishes.[/dim]")
        console.print("[dim]Each command runs independently, so data doesn't persist between commands.[/dim]")
    except KeyError:
        console.print(f"[red]Error: Todo with ID {todo_id} not found in memory.[/red]")
        console.print("[yellow]Possible reasons:[/yellow]")
        console.print("[yellow]- The todo was never created[/yellow]")
        console.print("[yellow]- The todo was deleted[/yellow]")
        console.print("[yellow]- You're running a new command instance (data doesn't persist between commands)[/yellow]")
        console.print("[yellow]Use 'todo list-todos' to see available todos in current memory.[/yellow]")
    except Exception as e:
        console.print(f"[red]Error showing todo: {str(e)}[/red]")
        console.print("[yellow]Note: This command runs independently, so data doesn't persist between commands.[/yellow]")

@app.command(help="Update fields of an existing todo by ID.")
def update(
    todo_id: int = typer.Argument(..., help="The ID of the todo to update"),
    title: Optional[str] = typer.Option(None, "--title", help="New title for the todo (1-150 characters)"),
    description: Optional[str] = typer.Option(None, "--description", "-d", help="New description for the todo"),
    status: Optional[str] = typer.Option(None, "--status", help="New status for the todo (pending, completed)")
):
    """
    Update fields of an existing todo.

    Example: todo update 1 --title "New title" --description "New description"
    Example: todo update 1 --status completed

    Note: This updates todos stored in memory only. Each command runs independently,
    so data doesn't persist between commands.
    """
    try:
        updates = {}
        if title is not None:
            updates['title'] = title
        if description is not None:
            updates['description'] = description
        if status is not None:
            if status not in ["pending", "completed"]:
                console.print(f"[red]Error: Status must be 'pending' or 'completed', got '{status}'.[/red]")
                return
            updates['status'] = status

        if not updates:
            console.print("[yellow]Warning: No updates specified. Use --title, --description, or --status to update fields.[/yellow]")
            return

        updated_todo = service.update_todo(todo_id, **updates)
        console.print(f"[green]SUCCESS: Todo updated![/green]")
        console.print(create_todo_output(updated_todo))
        console.print("\n[dim]Note: Todos are stored in memory only and will be lost when the command finishes.[/dim]")
        console.print("[dim]Each command runs independently, so data doesn't persist between commands.[/dim]")
    except KeyError:
        console.print(f"[red]Error: Todo with ID {todo_id} not found in memory.[/red]")
        console.print("[yellow]Possible reasons:[/yellow]")
        console.print("[yellow]- The todo was never created[/yellow]")
        console.print("[yellow]- The todo was deleted[/yellow]")
        console.print("[yellow]- You're running a new command instance (data doesn't persist between commands)[/yellow]")
        console.print("[yellow]Use 'todo list-todos' to see available todos in current memory.[/yellow]")
    except ValueError as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        console.print("[yellow]Hint: Title must be between 1 and 150 characters.[/yellow]")
    except Exception as e:
        console.print(f"[red]Error updating todo: {str(e)}[/red]")
        console.print("[yellow]Note: This command runs independently, so data doesn't persist between commands.[/yellow]")

@app.command(help="Delete a specific todo by ID.")
def delete(todo_id: int = typer.Argument(..., help="The ID of the todo to delete")):
    """
    Delete a specific todo.

    Example: todo delete 1

    Note: This deletes todos stored in memory only. Each command runs independently,
    so data doesn't persist between commands.
    """
    try:
        success = service.delete_todo(todo_id)
        if success:
            console.print(f"[green]SUCCESS: Todo with ID {todo_id} deleted![/green]")
            console.print("\n[dim]Note: Todos are stored in memory only and will be lost when the command finishes.[/dim]")
            console.print("[dim]Each command runs independently, so data doesn't persist between commands.[/dim]")
        else:
            console.print(f"[red]Error: Todo with ID {todo_id} not found in memory.[/red]")
            console.print("[yellow]Possible reasons:[/yellow]")
            console.print("[yellow]- The todo was never created[/yellow]")
            console.print("[yellow]- The todo was deleted[/yellow]")
            console.print("[yellow]- You're running a new command instance (data doesn't persist between commands)[/yellow]")
            console.print("[yellow]Use 'todo list-todos' to see available todos in current memory.[/yellow]")
    except Exception as e:
        console.print(f"[red]Error deleting todo: {str(e)}[/red]")
        console.print("[yellow]Note: This command runs independently, so data doesn't persist between commands.[/yellow]")

@app.command(name="complete", help="Mark a specific todo as completed by ID.")
def mark_complete(todo_id: int = typer.Argument(..., help="The ID of the todo to mark as complete")):
    """
    Mark a specific todo as completed.

    Example: todo complete 1

    Note: This updates todos stored in memory only. Each command runs independently,
    so data doesn't persist between commands.
    """
    try:
        todo = service.mark_todo_complete(todo_id)
        console.print(f"[green]SUCCESS: Todo with ID {todo_id} marked as completed![/green]")
        console.print(create_todo_output(todo))
        console.print("\n[dim]Note: Todos are stored in memory only and will be lost when the command finishes.[/dim]")
        console.print("[dim]Each command runs independently, so data doesn't persist between commands.[/dim]")
    except KeyError:
        console.print(f"[red]Error: Todo with ID {todo_id} not found in memory.[/red]")
        console.print("[yellow]Possible reasons:[/yellow]")
        console.print("[yellow]- The todo was never created[/yellow]")
        console.print("[yellow]- The todo was deleted[/yellow]")
        console.print("[yellow]- You're running a new command instance (data doesn't persist between commands)[/yellow]")
        console.print("[yellow]Use 'todo list-todos' to see available todos in current memory.[/yellow]")
    except Exception as e:
        console.print(f"[red]Error marking todo as complete: {str(e)}[/red]")
        console.print("[yellow]Note: This command runs independently, so data doesn't persist between commands.[/yellow]")