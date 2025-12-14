from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.properties import StringProperty, BooleanProperty
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from app.view.schedule_popup import SchedulePopup

class TaskItem(BoxLayout):
    # Properties bound to the UI
    description = StringProperty("")
    topic = StringProperty("")
    priority = StringProperty("")
    is_completed = BooleanProperty(False)

    def __init__(self, task, **kwargs):
        # Initialize TaskItem widget with task data
        self._initializing = True
        super().__init__(**kwargs)
        self.task = task
        self.task_id = str(getattr(task, "id", getattr(task, "task_id", 0)) or 0)
        self.description = task.description or ""
        self.topic = getattr(getattr(task, "topic", None), "name", "") or ""

        # Map numeric priority to human-readable label
        try:
            prio_num = int(getattr(task, "priority", 1) or 1)
        except (TypeError, ValueError):
            prio_num = 1
        self.priority = {1: "Low", 2: "Medium", 3: "High"}.get(prio_num, "Low")

        self.is_completed = bool(getattr(task, "is_completed", False))

        # Scheduling info (if available)
        self.selected_date = str(task.scheduled_date) if task.scheduled_date else ""
        self.start_time = str(task.start_time) if task.start_time else ""
        self.end_time = str(task.end_time) if task.end_time else ""

        # Mark initialization complete; this flag prevents property callbacks (e.g., on_checkbox_active) from running prematurely during __init__
        self._initializing = False

    def on_checkbox_active(self, checkbox, value):
        # Handle checkbox toggle: mark task as completed or not
        if getattr(self, "_initializing", False):
            return

        app = App.get_running_app()
        task_screen = app.sm.get_screen("tasks")
        try:
            if value:
                app.task_controller.mark_completed(int(self.task_id))
            else:
                app.task_controller.mark_notcompleted(int(self.task_id))
        except Exception as e:
            print("Error updating completion status:", e)

        # Refresh task list after update
        Clock.schedule_once(lambda dt: task_screen.refresh_task_list(), 0.0)

    def delete_task(self):
        # Delete this task and refresh task list
        app = App.get_running_app()
        task_screen = app.sm.get_screen("tasks")
        try:
            app.task_controller.delete_task(int(self.task_id))
        finally:
            Clock.schedule_once(lambda dt: task_screen.refresh_task_list(), 0.0)

    def open_schedule_popup(self):
        # Open popup for scheduling task date and time
        SchedulePopup(self).open()