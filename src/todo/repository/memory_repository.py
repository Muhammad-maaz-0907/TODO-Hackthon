"""
In-memory repository implementation for Todo items.
Handles data storage and retrieval in memory with ID generation.
"""

from typing import Dict, List, Optional
from ..models import Todo


class MemoryTodoRepository:
    """
    In-memory implementation of the Todo repository.
    
    Responsibilities:
    - Manage storage and retrieval of todos
    - Handle ID generation
    - Provide CRUD operations
    - Handle in-memory storage implementation
    """
    
    def __init__(self):
        self._todos: Dict[int, Todo] = {}
        self._next_id: int = 1
    
    def add(self, todo: Todo) -> Todo:
        """
        Add a new todo to storage.
        
        Args:
            todo: The todo to add
            
        Returns:
            The saved todo with assigned ID
        """
        # If the todo doesn't have an ID, assign the next available one
        if todo.id == 0 or todo.id is None:
            todo.id = self._next_id
            self._next_id += 1
        elif todo.id >= self._next_id:
            # If a higher ID was provided, update the next_id accordingly
            self._next_id = todo.id + 1
        
        self._todos[todo.id] = todo
        return todo
    
    def get_by_id(self, todo_id: int) -> Optional[Todo]:
        """
        Retrieve a todo by its ID.
        
        Args:
            todo_id: The ID of the todo to retrieve
            
        Returns:
            The todo if found, None otherwise
        """
        return self._todos.get(todo_id)
    
    def get_all(self) -> List[Todo]:
        """
        Retrieve all todos in storage.
        
        Returns:
            A list of all todos, or an empty list if no todos exist
        """
        return list(self._todos.values())
    
    def update(self, todo_id: int, **updates) -> Optional[Todo]:
        """
        Update fields of an existing todo.
        
        Args:
            todo_id: The ID of the todo to update
            **updates: The fields to update
            
        Returns:
            The updated todo if found, None if not found
        """
        if todo_id not in self._todos:
            return None
        
        todo = self._todos[todo_id]
        
        # Update the fields that were provided
        for field, value in updates.items():
            if hasattr(todo, field):
                setattr(todo, field, value)
        
        # Update the updated_at timestamp
        from datetime import datetime
        todo.updated_at = datetime.now()
        
        return todo
    
    def delete(self, todo_id: int) -> bool:
        """
        Remove a todo from storage.
        
        Args:
            todo_id: The ID of the todo to remove
            
        Returns:
            True if deletion was successful, False if not found
        """
        if todo_id in self._todos:
            del self._todos[todo_id]
            return True
        return False
    
    def mark_complete(self, todo_id: int) -> Optional[Todo]:
        """
        Mark a todo as completed.
        
        Args:
            todo_id: The ID of the todo to mark as complete
            
        Returns:
            The updated todo if found, None if not found
        """
        if todo_id not in self._todos:
            return None
        
        todo = self._todos[todo_id]
        todo.mark_completed()
        return todo
    
    def mark_pending(self, todo_id: int) -> Optional[Todo]:
        """
        Mark a completed todo as pending again.
        
        Args:
            todo_id: The ID of the todo to mark as pending
            
        Returns:
            The updated todo if found, None if not found
        """
        if todo_id not in self._todos:
            return None
        
        todo = self._todos[todo_id]
        todo.mark_pending()
        return todo