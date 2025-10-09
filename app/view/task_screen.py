from kivy.uix.screenmanager import Screen
from kivy.app import App
from app.model.task import Task
from app.model.topic import Topic
from app.view.task_item import TaskItem
from app.view.add_task_popup import AddTaskPopup

class TaskScreen(Screen):
    # Main screen for managing tasks (viewing, creating, updating)

    def open_add_task_popup(self):
        # Open the popup window to create a new task
        popup = AddTaskPopup()
        popup.open()
    
    def on_enter(self):
        # Refresh the task list every time the screen is entered
        self.load_tasks()

    def load_tasks(self):
        # Load all tasks from the controller and display them in the UI
        app = App.get_running_app()
        self.ids.task_list.clear_widgets()
        tasks = app.task_controller.get_all_tasks()
        for task in tasks:
            task_item = TaskItem(task)
            self.ids.task_list.add_widget(task_item)
    
    def add_task_from_popup(self, desc, topic_name, prio, date, start, end, popup):
        # Handle task creation from the popup input fields
        app = App.get_running_app()
        if not desc:
            print("Missing required fields")
            return
        
        topic_id = None
        if topic_name and topic_name != "Select topic":
            topic_id = app.topic_controller.get_topic_id(topic_name)

        try:
            prio = int(prio)
        except ValueError:
            print("Priority must be an integer")
            return
        
        # Create Task object and save it
        task = Task(
            id=None,
            description=desc,
            topic=Topic(id=topic_id) if topic_id else None,
            priority=prio,
            is_completed=False,
            scheduled_date=date if date else None,
            start_time=start if start else None,
            end_time=end if end else None
        )
        task_id = app.task_controller.create_task(task)
        print(f"Task created with ID: {task_id}")
        popup.dismiss()

    def refresh_task_list(self):
        # Reload the list of tasks (e.g. after add/delete/update)
        app = App.get_running_app()
        task_screen = app.sm.get_screen("tasks")
        task_screen.load_tasks()