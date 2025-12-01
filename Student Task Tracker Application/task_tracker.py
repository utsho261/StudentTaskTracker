import json
import random
from datetime import datetime

class Task:
    def __init__(self, task_id, title, description, created_at):
        self.id = task_id
        self.title = title
        self.description = description
        self.created_at = created_at

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "created_at": self.created_at
        }

class TaskManager:
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = []
        self.load_from_file()

    def load_from_file(self):
        try:
            with open(self.filename, 'r') as file:
                data = json.load(file)
                for t in data:
                    task = Task(t["id"], t["title"], t["description"], t["created_at"])
                    self.tasks.append(task)
        except FileNotFoundError:
            with open(self.filename, 'w') as file:
                json.dump([], file)
        except json.JSONDecodeError:
            print("⚠️ JSON decode error: File corrupted. Starting with an empty task list.")
            self.tasks = []

    def save_to_file(self):
        try:
            with open(self.filename, 'w') as file:
                json.dump([task.to_dict() for task in self.tasks], file, indent=4)
        except Exception as e:
            print(f"❌ Error saving file: {e}")


    def add_task(self):
        title = input("Enter task title: ")
        description = input("Enter task description: ")
        task_id = random.randint(100, 9999)
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        task = Task(task_id, title, description, created_at)
        self.tasks.append(task)
        print(f"✅ Task added successfully with ID {task_id}!\n")

    def view_tasks(self):
        if not self.tasks:
            print("📭 No tasks available.\n")
            return
        print("\n===== All Tasks =====")
        for idx, task in enumerate(self.tasks, start=1):
            print(f"{idx}. [{task.id}] {task.title} - {task.description} (Created: {task.created_at})")
        print()

    def update_task(self):
        self.view_tasks()
        if not self.tasks:
            return
        try:
            index = int(input("Enter the task number to update: ")) - 1
            if index < 0 or index >= len(self.tasks):
                raise IndexError
            new_title = input("Enter new title: ")
            new_description = input("Enter new description: ")
            self.tasks[index].title = new_title
            self.tasks[index].description = new_description
            print("✅ Task updated successfully!\n")
        except ValueError:
            print("❌ Invalid input. Please enter a number.\n")
        except IndexError:
            print("❌ Task number out of range.\n")

    def delete_task(self):
        self.view_tasks()
        if not self.tasks:
            return
        try:
            index = int(input("Enter the task number to delete: ")) - 1
            if index < 0 or index >= len(self.tasks):
                raise IndexError
            deleted_task = self.tasks.pop(index)
            print(f"🗑️ Task '{deleted_task.title}' deleted successfully!\n")
        except ValueError:
            print("❌ Invalid input. Please enter a number.\n")
        except IndexError:
            print("❌ Task number out of range.\n")


    def run(self):
        while True:
            print("===== Student Task Tracker =====")
            print("1. Add New Task")
            print("2. View All Tasks")
            print("3. Update Task")
            print("4. Delete Task")
            print("5. Exit")

            choice = input("Enter your choice (1-5): ")

            if choice == '1':
                self.add_task()
            elif choice == '2':
                self.view_tasks()
            elif choice == '3':
                self.update_task()
            elif choice == '4':
                self.delete_task()
            elif choice == '5':
                print("💾 Saving tasks to file... Bye!\n")
                self.save_to_file()
                break
            else:
                print("❌ Invalid choice. Please try again.\n")


manager = TaskManager()
manager.run()