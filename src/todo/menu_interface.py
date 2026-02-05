import sys
from typing import Optional

from .models import Todo
from .service.todo_service import TodoService
from .repository.memory_repository import MemoryTodoRepository


class TodoMenuInterface:
    """
    A menu-driven console interface for the Todo application.
    Provides a beginner-friendly numbered menu system.
    """
    
    def __init__(self):
        self.repository = MemoryTodoRepository()
        self.service = TodoService(self.repository)
        self.running = True

    def display_menu(self):
        """Display the main menu options."""
        print("\n--- Todo Application ---")
        print("1. Add Task")
        print("2. View All Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Mark Task Complete")
        print("6. Mark Task Incomplete")
        print("7. Exit")
        print("------------------------")

    def get_user_choice(self) -> int:
        """Get and validate user's menu choice."""
        while True:
            try:
                choice = input("Enter your choice (1-7): ").strip()
                choice_num = int(choice)
                if 1 <= choice_num <= 7:
                    return choice_num
                else:
                    print("Invalid choice. Please enter a number between 1 and 7.")
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 7.")

    def add_task(self):
        """Handle adding a new task."""
        print("\n--- Add New Task ---")
        title = input("Enter task title: ").strip()
        
        if not title:
            print("Task title cannot be empty!")
            return
        
        description = input("Enter task description (optional, press Enter to skip): ").strip()
        description = description if description else None
        
        try:
            new_todo = self.service.create_todo(title=title, description=description)
            print(f"\n✓ Task added successfully!")
            print(f"ID: {new_todo.id}")
            print(f"Title: {new_todo.title}")
            print(f"Description: {new_todo.description or 'None'}")
            print(f"Status: {new_todo.status}")
            print(f"Created: {new_todo.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        except ValueError as e:
            print(f"Error: {str(e)}")
            print("Hint: Title must be between 1 and 150 characters.")

    def view_tasks(self):
        """Handle viewing all tasks."""
        print("\n--- All Tasks ---")
        todos = self.service.get_all_todos()
        
        if not todos:
            print("No tasks found!")
            return
        
        # Sort by ID for consistent display
        todos.sort(key=lambda x: x.id)
        
        for todo in todos:
            status_symbol = "✓" if todo.status == "completed" else "○"
            print(f"{status_symbol} [{todo.id}] {todo.title}")
            print(f"   Description: {todo.description or 'None'}")
            print(f"   Status: {todo.status}")
            print(f"   Created: {todo.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"   Updated: {todo.updated_at.strftime('%Y-%m-%d %H:%M:%S')}")
            print("-" * 50)

    def update_task(self):
        """Handle updating an existing task."""
        print("\n--- Update Task ---")
        todos = self.service.get_all_todos()
        
        if not todos:
            print("No tasks found to update!")
            return
        
        print("Current tasks:")
        for todo in todos:
            status_symbol = "✓" if todo.status == "completed" else "○"
            print(f"  {status_symbol} [{todo.id}] {todo.title}")
        
        try:
            task_id = int(input("\nEnter the ID of the task to update: "))
        except ValueError:
            print("Invalid ID. Please enter a number.")
            return
        
        # Check if task exists
        try:
            existing_todo = self.service.get_todo(task_id)
        except KeyError:
            print(f"No task found with ID {task_id}.")
            return
        
        print(f"\nUpdating task: {existing_todo.title}")
        print(f"Current description: {existing_todo.description or 'None'}")
        print(f"Current status: {existing_todo.status}")
        
        # Get new values (or keep current if empty input)
        new_title = input(f"Enter new title (current: '{existing_todo.title}', press Enter to keep current): ").strip()
        if not new_title:
            new_title = existing_todo.title
        
        new_description = input(f"Enter new description (current: '{existing_todo.description or 'None'}', press Enter to keep current): ").strip()
        if new_description == "":
            new_description = existing_todo.description
        
        new_status_input = input(f"Enter new status (current: '{existing_todo.status}', press Enter to keep current): ").strip().lower()
        if not new_status_input:
            new_status = existing_todo.status
        elif new_status_input in ["completed", "complete", "done", "c"]:
            new_status = "completed"
        elif new_status_input in ["pending", "incomplete", "not done", "p"]:
            new_status = "pending"
        else:
            print("Invalid status. Keeping current status.")
            new_status = existing_todo.status
        
        try:
            updated_todo = self.service.update_todo(
                task_id, 
                title=new_title, 
                description=new_description, 
                status=new_status
            )
            print(f"\n✓ Task updated successfully!")
            print(f"ID: {updated_todo.id}")
            print(f"Title: {updated_todo.title}")
            print(f"Description: {updated_todo.description or 'None'}")
            print(f"Status: {updated_todo.status}")
            print(f"Updated: {updated_todo.updated_at.strftime('%Y-%m-%d %H:%M:%S')}")
        except ValueError as e:
            print(f"Error: {str(e)}")
            print("Hint: Title must be between 1 and 150 characters.")

    def delete_task(self):
        """Handle deleting a task."""
        print("\n--- Delete Task ---")
        todos = self.service.get_all_todos()
        
        if not todos:
            print("No tasks found to delete!")
            return
        
        print("Current tasks:")
        for todo in todos:
            status_symbol = "✓" if todo.status == "completed" else "○"
            print(f"  {status_symbol} [{todo.id}] {todo.title}")
        
        try:
            task_id = int(input("\nEnter the ID of the task to delete: "))
        except ValueError:
            print("Invalid ID. Please enter a number.")
            return
        
        try:
            success = self.service.delete_todo(task_id)
            if success:
                print(f"\n✓ Task with ID {task_id} deleted successfully!")
            else:
                print(f"No task found with ID {task_id}.")
        except Exception as e:
            print(f"Error deleting task: {str(e)}")

    def mark_complete(self):
        """Handle marking a task as complete."""
        print("\n--- Mark Task Complete ---")
        todos = self.service.get_all_todos()
        
        if not todos:
            print("No tasks found!")
            return
        
        pending_todos = [t for t in todos if t.status == "pending"]
        if not pending_todos:
            print("No pending tasks to mark as complete!")
            return
        
        print("Pending tasks:")
        for todo in pending_todos:
            print(f"  ○ [{todo.id}] {todo.title}")
        
        try:
            task_id = int(input("\nEnter the ID of the task to mark complete: "))
        except ValueError:
            print("Invalid ID. Please enter a number.")
            return
        
        try:
            todo = self.service.mark_todo_complete(task_id)
            print(f"\n✓ Task '{todo.title}' marked as complete!")
        except KeyError:
            print(f"No task found with ID {task_id}.")

    def mark_incomplete(self):
        """Handle marking a task as incomplete."""
        print("\n--- Mark Task Incomplete ---")
        todos = self.service.get_all_todos()
        
        if not todos:
            print("No tasks found!")
            return
        
        completed_todos = [t for t in todos if t.status == "completed"]
        if not completed_todos:
            print("No completed tasks to mark as incomplete!")
            return
        
        print("Completed tasks:")
        for todo in completed_todos:
            print(f"  ✓ [{todo.id}] {todo.title}")
        
        try:
            task_id = int(input("\nEnter the ID of the task to mark incomplete: "))
        except ValueError:
            print("Invalid ID. Please enter a number.")
            return
        
        try:
            todo = self.service.mark_todo_pending(task_id)
            print(f"\n✓ Task '{todo.title}' marked as incomplete!")
        except KeyError:
            print(f"No task found with ID {task_id}.")

    def run(self):
        """Main application loop."""
        print("Welcome to the Todo Application!")
        
        while self.running:
            self.display_menu()
            choice = self.get_user_choice()
            
            if choice == 1:
                self.add_task()
            elif choice == 2:
                self.view_tasks()
            elif choice == 3:
                self.update_task()
            elif choice == 4:
                self.delete_task()
            elif choice == 5:
                self.mark_complete()
            elif choice == 6:
                self.mark_incomplete()
            elif choice == 7:
                print("\nThank you for using the Todo Application!")
                print("Goodbye!")
                self.running = False
            
            # Pause before showing menu again
            if self.running:
                input("\nPress Enter to continue...")
        
        sys.exit(0)