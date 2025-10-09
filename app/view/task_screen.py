from kivy.uix.screenmanager import Screen
from kivy.app import App
from app.model.task import Task
from app.model.topic import Topic
from app.view.task_item import TaskItem
from app.view.add_task_popup import AddTaskPopup

class TaskScreen(Screen):
    def open_add_task_popup(self):
        popup = AddTaskPopup()
        popup.open()
    
    def on_enter(self):
        self.load_tasks()

    def load_tasks(self):
        app = App.get_running_app()
        self.ids.task_list.clear_widgets()
        tasks = app.task_controller.get_all_tasks()
        for task in tasks:
            task_item = TaskItem(task)
            self.ids.task_list.add_widget(task_item)
    
    def add_task_from_popup(self, desc, topic_name, prio, date, start, end, popup):
        app = App.get_running_app()
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
        app = App.get_running_app()
        task_screen = app.sm.get_screen("tasks")
        task_screen.load_tasks()