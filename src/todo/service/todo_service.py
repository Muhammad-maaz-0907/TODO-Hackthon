"""
Service layer for Todo operations.
Implements business logic and validation.
"""

from datetime import datetime
from typing import List, Optional
from ..models import Todo
from ..repository.memory_repository import MemoryTodoRepository


class TodoService:
    """
    Service class that implements business logic and validation for Todo operations.
    
    Responsibilities:
    - Implement business rules and validation
    - Coordinate between repository and presentation layers
    - Handle error cases appropriately
    """
    
    def __init__(self, repository: MemoryTodoRepository):
        self.repository = repository
    
    def create_todo(self, title: str, description: str = None) -> Todo:
        """
        Create a new todo.
        
        Args:
            title: The title of the new todo (required, 1-150 characters)
            description: Additional details about the todo (optional)
            
        Returns:
            The created Todo object
        """
        # Validate title length
        if not title or len(title) > 150:
            raise ValueError(f"Title must be between 1 and 150 characters. Provided: {len(title) if title else 0}")
        
        # Create a new Todo instance
        new_todo = Todo(
            id=0,  # Will be assigned by repository
            title=title,
            description=description,
            status="pending",  # Default status
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        # Save to repository
        return self.repository.add(new_todo)
    
    def get_todo(self, todo_id: int) -> Todo:
        """
        Get a specific todo by ID.
        
        Args:
            todo_id: The ID of the todo to retrieve
            
        Returns:
            The Todo object
            
        Raises:
            KeyError: If the todo with the given ID doesn't exist
        """
        todo = self.repository.get_by_id(todo_id)
        if todo is None:
            raise KeyError(f"Todo with ID {todo_id} not found")
        return todo
    
    def get_all_todos(self, status_filter: str = None, sort_field: str = None) -> List[Todo]:
        """
        Get all todos with optional filtering and sorting.
        
        Args:
            status_filter: Filter todos by status ("pending", "completed", "all", or None for all)
            sort_field: Sort todos by field ("created", "title", "status", or None for no sorting)
            
        Returns:
            A list of Todo objects
        """
        todos = self.repository.get_all()
        
        # Apply status filter if specified
        if status_filter and status_filter != "all":
            if status_filter in ["pending", "completed"]:
                todos = [todo for todo in todos if todo.status == status_filter]
        
        # Apply sorting if specified
        if sort_field == "created":
            # Sort by creation date (oldest first)
            todos.sort(key=lambda x: x.created_at)
        elif sort_field == "title":
            # Sort by title alphabetically
            todos.sort(key=lambda x: x.title.lower())
        elif sort_field == "status":
            # Sort by status (pending first, then completed)
            todos.sort(key=lambda x: x.status == "completed")  # False (pending) comes first
        
        return todos
    
    def update_todo(self, todo_id: int, **updates) -> Todo:
        """
        Update a todo.
        
        Args:
            todo_id: The ID of the todo to update
            **updates: The fields to update (title, description, status)
            
        Returns:
            The updated Todo object
            
        Raises:
            KeyError: If the todo with the given ID doesn't exist
            ValueError: If the update contains invalid values
        """
        # Check if the todo exists
        existing_todo = self.repository.get_by_id(todo_id)
        if existing_todo is None:
            raise KeyError(f"Todo with ID {todo_id} not found")
        
        # Validate title if it's being updated
        if 'title' in updates:
            title = updates['title']
            if title is not None and (not title or len(title) > 150):
                raise ValueError(f"Title must be between 1 and 150 characters. Provided: {len(title) if title else 0}")
        
        # Perform the update
        updated_todo = self.repository.update(todo_id, **updates)
        if updated_todo is None:
            raise KeyError(f"Todo with ID {todo_id} not found after update attempt")
        
        return updated_todo
    
    def delete_todo(self, todo_id: int) -> bool:
        """
        Delete a todo.
        
        Args:
            todo_id: The ID of the todo to delete
            
        Returns:
            True if deletion was successful, False if the todo didn't exist
        """
        return self.repository.delete(todo_id)
    
    def mark_todo_complete(self, todo_id: int) -> Todo:
        """
        Mark a todo as complete.
        
        Args:
            todo_id: The ID of the todo to mark as complete
            
        Returns:
            The updated Todo object
            
        Raises:
            KeyError: If the todo with the given ID doesn't exist
        """
        todo = self.repository.mark_complete(todo_id)
        if todo is None:
            raise KeyError(f"Todo with ID {todo_id} not found")
        return todo
    
    def mark_todo_pending(self, todo_id: int) -> Todo:
        """
        Mark a completed todo as pending again.
        
        Args:
            todo_id: The ID of the todo to mark as pending
            
        Returns:
            The updated Todo object
            
        Raises:
            KeyError: If the todo with the given ID doesn't exist
        """
        todo = self.repository.mark_pending(todo_id)
        if todo is None:
            raise KeyError(f"Todo with ID {todo_id} not found")
        return todo