import typer
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from datetime import datetime

from ..models import Todo
from ..main import service

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
    status_symbol = "✓" if todo.status == "completed" else "○"
    return f"{status_symbol} [{todo.id}] {todo.title}\n   Description: {todo.description or 'None'}\n   Status: {todo.status}\n   Created: {todo.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n   Updated: {todo.updated_at.strftime('%Y-%m-%d %H:%M:%S')}"

app = typer.Typer(no_args_is_help=True, add_completion=False)

@app.command()
def add(
    title: str = typer.Argument(..., help="The title of the new todo"),
    description: Optional[str] = typer.Option(None, "--description", "-d", help="Additional details about the todo")
):
    """
    Add a new todo item.

    Example: todo add "Buy groceries" --description "Milk and bread"
    """
    try:
        new_todo = service.create_todo(title=title, description=description)
        console.print(f"[green]✓ Todo added successfully![/green]")
        console.print(create_todo_output(new_todo))
    except ValueError as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        console.print("[yellow]Hint: Title must be between 1 and 150 characters.[/yellow]")
    except Exception as e:
        console.print(f"[red]Unexpected error: {str(e)}[/red]")

@app.command()
def list_todos(
    status: Optional[str] = typer.Option(None, "--status", help="Filter todos by status (pending, completed, all)"),
    sort: Optional[str] = typer.Option(None, "--sort", help="Sort todos by field (created, title, status)")
):
    """
    List all todo items.

    Example: todo list
    Example: todo list --status pending
    Example: todo list --sort title
    """
    try:
        todos = service.get_all_todos(status_filter=status, sort_field=sort)

        if not todos:
            console.print(Panel("[yellow]No todos yet![/yellow]\nAdd one with: [bold]todo add 'your task'[/bold]", title="Todo List"))
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
    except Exception as e:
        console.print(f"[red]Error listing todos: {str(e)}[/red]")

@app.command()
def show(todo_id: int = typer.Argument(..., help="The ID of the todo to show")):
    """
    Show details of a specific todo.

    Example: todo show 1
    """
    try:
        todo = service.get_todo(todo_id)
        console.print(Panel(create_todo_output(todo), title=f"Todo #{todo.id}"))
    except KeyError:
        console.print(f"[red]Error: Todo with ID {todo_id} not found.[/red]")
        console.print("[yellow]Use 'todo list' to see available todos.[/yellow]")
    except Exception as e:
        console.print(f"[red]Error showing todo: {str(e)}[/red]")

@app.command()
def update(
    todo_id: int = typer.Argument(..., help="The ID of the todo to update"),
    title: Optional[str] = typer.Option(None, "--title", help="New title for the todo"),
    description: Optional[str] = typer.Option(None, "--description", "-d", help="New description for the todo"),
    status: Optional[str] = typer.Option(None, "--status", help="New status for the todo (pending, completed)")
):
    """
    Update fields of an existing todo.

    Example: todo update 1 --title "New title" --description "New description"
    Example: todo update 1 --status completed
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
        console.print(f"[green]✓ Todo updated successfully![/green]")
        console.print(create_todo_output(updated_todo))
    except KeyError:
        console.print(f"[red]Error: Todo with ID {todo_id} not found.[/red]")
        console.print("[yellow]Use 'todo list' to see available todos.[/yellow]")
    except ValueError as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        console.print("[yellow]Hint: Title must be between 1 and 150 characters.[/yellow]")
    except Exception as e:
        console.print(f"[red]Error updating todo: {str(e)}[/red]")

@app.command()
def delete(todo_id: int = typer.Argument(..., help="The ID of the todo to delete")):
    """
    Delete a specific todo.

    Example: todo delete 1
    """
    try:
        success = service.delete_todo(todo_id)
        if success:
            console.print(f"[green]✓ Todo with ID {todo_id} deleted successfully![/green]")
        else:
            console.print(f"[red]Error: Todo with ID {todo_id} not found.[/red]")
            console.print("[yellow]Use 'todo list' to see available todos.[/yellow]")
    except Exception as e:
        console.print(f"[red]Error deleting todo: {str(e)}[/red]")

@app.command(name="complete")
def mark_complete(todo_id: int = typer.Argument(..., help="The ID of the todo to mark as complete")):
    """
    Mark a specific todo as completed.

    Example: todo complete 1
    """
    try:
        todo = service.mark_todo_complete(todo_id)
        console.print(f"[green]✓ Todo with ID {todo_id} marked as completed![/green]")
        console.print(create_todo_output(todo))
    except KeyError:
        console.print(f"[red]Error: Todo with ID {todo_id} not found.[/red]")
        console.print("[yellow]Use 'todo list' to see available todos.[/yellow]")
    except Exception as e:
        console.print(f"[red]Error marking todo as complete: {str(e)}[/red]")