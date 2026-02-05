#!/usr/bin/env python3
"""
Test script to verify the functionality of the todo app.
"""

from src.todo.models import Todo
from src.todo.repository.memory_repository import MemoryTodoRepository
from src.todo.service.todo_service import TodoService

def test_todo_functionality():
    print('Starting test...')
    
    # Test creating a todo
    repo = MemoryTodoRepository()
    service = TodoService(repo)
    print('Repository and service created')
    
    # Create a new todo
    new_todo = service.create_todo('Test todo', 'This is a test')
    print(f'Created todo: {new_todo.title}')
    
    # Get the todo
    retrieved = service.get_todo(new_todo.id)
    print(f'Retrieved todo: {retrieved.title}')
    
    # Update the todo
    updated = service.update_todo(retrieved.id, title='Updated todo')
    print(f'Updated todo: {updated.title}')
    
    # Mark as complete
    completed = service.mark_todo_complete(updated.id)
    print(f'Marked as complete: {completed.status}')
    
    # List all todos
    all_todos = service.get_all_todos()
    print(f'Total todos: {len(all_todos)}')
    
    # Delete the todo
    deleted = service.delete_todo(completed.id)
    print(f'Todo deleted: {deleted}')
    
    print('Test completed successfully')

if __name__ == "__main__":
    test_todo_functionality()