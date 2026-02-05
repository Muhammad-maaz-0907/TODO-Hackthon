import pytest
from datetime import datetime
from src.todo.models import Todo
from src.todo.repository.memory_repository import MemoryTodoRepository
from src.todo.service.todo_service import TodoService


class TestTodoModel:
    """Test cases for the Todo model."""
    
    def test_create_valid_todo(self):
        """Test creating a valid todo."""
        todo = Todo(id=1, title="Test todo", description="A test todo item")
        
        assert todo.id == 1
        assert todo.title == "Test todo"
        assert todo.description == "A test todo item"
        assert todo.status == "pending"
        assert isinstance(todo.created_at, datetime)
        assert isinstance(todo.updated_at, datetime)
    
    def test_title_validation(self):
        """Test that title validation works correctly."""
        # Test empty title
        with pytest.raises(ValueError):
            Todo(id=1, title="")
        
        # Test title too long
        with pytest.raises(ValueError):
            Todo(id=1, title="x" * 151)  # 151 characters is over the limit
        
        # Test valid title
        todo = Todo(id=1, title="Valid title")
        assert todo.title == "Valid title"
    
    def test_status_validation(self):
        """Test that status validation works correctly."""
        # Test invalid status
        with pytest.raises(ValueError):
            Todo(id=1, title="Test", status="invalid")
        
        # Test valid statuses
        pending_todo = Todo(id=1, title="Test", status="pending")
        assert pending_todo.status == "pending"
        
        completed_todo = Todo(id=2, title="Test", status="completed")
        assert completed_todo.status == "completed"


class TestMemoryRepository:
    """Test cases for the MemoryTodoRepository."""
    
    def setup_method(self):
        """Set up a fresh repository for each test."""
        self.repo = MemoryTodoRepository()
    
    def test_add_todo(self):
        """Test adding a todo to the repository."""
        todo = Todo(id=0, title="Test todo")
        saved_todo = self.repo.add(todo)
        
        assert saved_todo.id > 0  # ID should be assigned
        assert saved_todo.title == "Test todo"
        
        # Verify it can be retrieved
        retrieved = self.repo.get_by_id(saved_todo.id)
        assert retrieved is not None
        assert retrieved.id == saved_todo.id
    
    def test_get_by_id(self):
        """Test retrieving a todo by ID."""
        todo = Todo(id=0, title="Test todo")
        saved_todo = self.repo.add(todo)
        
        retrieved = self.repo.get_by_id(saved_todo.id)
        assert retrieved is not None
        assert retrieved.id == saved_todo.id
        assert retrieved.title == "Test todo"
    
    def test_get_nonexistent_todo(self):
        """Test retrieving a non-existent todo."""
        result = self.repo.get_by_id(999)
        assert result is None
    
    def test_get_all_todos(self):
        """Test retrieving all todos."""
        # Add a few todos
        todo1 = Todo(id=0, title="Todo 1")
        todo2 = Todo(id=0, title="Todo 2")
        self.repo.add(todo1)
        self.repo.add(todo2)
        
        all_todos = self.repo.get_all()
        assert len(all_todos) == 2
        
        titles = {todo.title for todo in all_todos}
        assert "Todo 1" in titles
        assert "Todo 2" in titles
    
    def test_update_todo(self):
        """Test updating a todo."""
        todo = Todo(id=0, title="Original title")
        saved_todo = self.repo.add(todo)
        
        updated = self.repo.update(saved_todo.id, title="Updated title")
        assert updated is not None
        assert updated.title == "Updated title"
        assert updated.id == saved_todo.id
    
    def test_delete_todo(self):
        """Test deleting a todo."""
        todo = Todo(id=0, title="To delete")
        saved_todo = self.repo.add(todo)
        
        # Verify it exists
        assert self.repo.get_by_id(saved_todo.id) is not None
        
        # Delete it
        result = self.repo.delete(saved_todo.id)
        assert result is True
        
        # Verify it's gone
        assert self.repo.get_by_id(saved_todo.id) is None
    
    def test_mark_complete_and_pending(self):
        """Test marking todos as complete and pending."""
        todo = Todo(id=0, title="Test todo")
        saved_todo = self.repo.add(todo)
        
        # Initially should be pending
        assert saved_todo.status == "pending"
        
        # Mark as complete
        completed = self.repo.mark_complete(saved_todo.id)
        assert completed is not None
        assert completed.status == "completed"
        
        # Mark as pending again
        pending = self.repo.mark_pending(saved_todo.id)
        assert pending is not None
        assert pending.status == "pending"


class TestTodoService:
    """Test cases for the TodoService."""
    
    def setup_method(self):
        """Set up a service with a fresh repository for each test."""
        self.repo = MemoryTodoRepository()
        self.service = TodoService(self.repo)
    
    def test_create_todo(self):
        """Test creating a todo through the service."""
        todo = self.service.create_todo("Test title", "Test description")
        
        assert todo.id > 0
        assert todo.title == "Test title"
        assert todo.description == "Test description"
        assert todo.status == "pending"
    
    def test_get_todo(self):
        """Test getting a todo by ID."""
        created = self.service.create_todo("Test title")
        retrieved = self.service.get_todo(created.id)
        
        assert retrieved.id == created.id
        assert retrieved.title == "Test title"
    
    def test_get_nonexistent_todo(self):
        """Test getting a non-existent todo raises KeyError."""
        with pytest.raises(KeyError):
            self.service.get_todo(999)
    
    def test_get_all_todos(self):
        """Test getting all todos."""
        self.service.create_todo("Todo 1")
        self.service.create_todo("Todo 2")
        
        all_todos = self.service.get_all_todos()
        assert len(all_todos) == 2
    
    def test_update_todo(self):
        """Test updating a todo."""
        created = self.service.create_todo("Original title")
        
        updated = self.service.update_todo(created.id, title="Updated title")
        assert updated.title == "Updated title"
    
    def test_delete_todo(self):
        """Test deleting a todo."""
        created = self.service.create_todo("To delete")
        
        # Verify it exists
        retrieved = self.service.get_todo(created.id)
        assert retrieved is not None
        
        # Delete it
        result = self.service.delete_todo(created.id)
        assert result is True
        
        # Verify it's gone
        with pytest.raises(KeyError):
            self.service.get_todo(created.id)
    
    def test_mark_todo_complete(self):
        """Test marking a todo as complete."""
        created = self.service.create_todo("Test todo")
        assert created.status == "pending"
        
        completed = self.service.mark_todo_complete(created.id)
        assert completed.status == "completed"
    
    def test_mark_todo_pending(self):
        """Test marking a completed todo as pending."""
        created = self.service.create_todo("Test todo")
        completed = self.service.mark_todo_complete(created.id)
        assert completed.status == "completed"
        
        pending = self.service.mark_todo_pending(created.id)
        assert pending.status == "pending"