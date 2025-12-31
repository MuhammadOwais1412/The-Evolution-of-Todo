"""Main entry point for the Todo application."""

from src.task import TaskService
from src.ui import (
    show_menu,
    get_choice,
    show_tasks,
    prompt_task_data,
    prompt_task_id,
    prompt_update_data,
    success,
    error,
    info,
    confirm_action,
    show_separator,
)


def main() -> None:
    """Run the Todo application."""
    service = TaskService()

    while True:
        show_menu()
        choice = get_choice()

        if choice == 1:  # Add Task
            title, description = prompt_task_data()
            task = service.add(title, description)
            success(f"Task #{task.id} created successfully")

        elif choice == 2:  # View Tasks
            tasks = service.list()
            show_tasks(tasks)

        elif choice == 3:  # Update Task
            task_id = prompt_task_id()
            title, description = prompt_update_data()
            try:
                service.update(task_id, title, description)
                success(f"Task #{task_id} updated successfully")
            except KeyError:
                error(f"Task with ID {task_id} not found.")
            except ValueError as e:
                error(str(e))

        elif choice == 4:  # Delete Task
            task_id = prompt_task_id()
            if confirm_action("delete", task_id):
                try:
                    service.delete(task_id)
                    success(f"Task #{task_id} deleted successfully")
                except KeyError:
                    error(f"Task with ID {task_id} not found.")
            else:
                info("Delete cancelled.")

        elif choice == 5:  # Mark Complete
            task_id = prompt_task_id()
            try:
                task = service.get(task_id)
                if task is None:
                    error(f"Task with ID {task_id} not found.")
                elif task.completed:
                    info(f"Task #{task_id} is already complete.")
                else:
                    task.completed = True
                    success(f"Task #{task_id} marked as complete")
            except KeyError:
                error(f"Task with ID {task_id} not found.")

        elif choice == 6:  # Mark Incomplete
            task_id = prompt_task_id()
            try:
                task = service.get(task_id)
                if task is None:
                    error(f"Task with ID {task_id} not found.")
                elif not task.completed:
                    info(f"Task #{task_id} is already incomplete.")
                else:
                    task.completed = False
                    success(f"Task #{task_id} marked as incomplete")
            except KeyError:
                error(f"Task with ID {task_id} not found.")

        elif choice == 7:  # Exit
            show_separator()
            info("Thank you for using Todo Application!")
            print()
            break


if __name__ == "__main__":
    main()
