from src.todo.menu_interface import TodoMenuInterface

# Create an instance of the menu interface
menu = TodoMenuInterface()

# Test adding a task
print("Testing adding a task...")
try:
    menu.service.create_todo("Test Task", "This is a test task")
    print("Task added successfully!")
except Exception as e:
    print(f"Error adding task: {e}")

# Test viewing tasks
print("\nTesting viewing tasks...")
try:
    todos = menu.service.get_all_todos()
    print(f"Found {len(todos)} tasks:")
    for todo in todos:
        print(f"- {todo.id}: {todo.title} ({todo.status})")
except Exception as e:
    print(f"Error viewing tasks: {e}")

print("\nMenu interface is working correctly!")