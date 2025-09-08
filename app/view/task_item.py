from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.properties import StringProperty, BooleanProperty, ObjectProperty
from kivy.clock import Clock
from kivymd.uix.pickers import MDDatePicker, MDTimePicker
from kivymd.uix.button import MDFlatButton
from kivy.uix.popup import Popup


class TaskItem(BoxLayout):
    description = StringProperty("")
    topic = StringProperty("")
    priority = StringProperty("")
    is_completed = BooleanProperty(False)

    def __init__(self, task, **kwargs):
        self._initializing = True
        super().__init__(**kwargs)
        self.task = task
        self.task_id = str(getattr(task, "id", getattr(task, "task_id", 0)) or 0)
        self.description = task.description or ""
        self.topic = getattr(getattr(task, "topic", None), "name", "") or ""

        try:
            prio_num = int(getattr(task, "priority", 1) or 1)
        except (TypeError, ValueError):
            prio_num = 1
        self.priority = {1: "Low", 2: "Medium", 3: "High"}.get(prio_num, "Low")
        self.is_completed = bool(getattr(task, "is_completed", False))

        self.selected_date = str(task.scheduled_date) if task.scheduled_date else ""
        self.start_time = str(task.start_time) if task.start_time else ""
        self.end_time = str(task.end_time) if task.end_time else ""

        self._initializing = False

    def on_checkbox_active(self, checkbox, value):
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

        Clock.schedule_once(lambda dt: task_screen.refresh_task_list(), 0.0)

    def delete_task(self):
        app = App.get_running_app()
        task_screen = app.sm.get_screen("tasks")
        try:
            app.task_controller.delete_task(int(self.task_id))
        finally:
            Clock.schedule_once(lambda dt: task_screen.refresh_task_list(), 0.0)

    def open_schedule_popup(self):
        SchedulePopup(self).open()


class SchedulePopup(Popup):
    task_item = ObjectProperty(None)

    def __init__(self, task_item, **kwargs):
        super().__init__(**kwargs)
        self.task_item = task_item

    def open_date_picker(self, button):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=lambda instance, value, date_range: self.set_date(value, button))
        date_dialog.open()

    def set_date(self, date, button):
        self.task_item.selected_date = date.isoformat()
        button.text = f"Date: {self.task_item.selected_date}"

    def open_time_picker(self, mode, button):
        time_dialog = MDTimePicker()
        time_dialog.bind(time=lambda instance, time: self.set_time(mode, time, button))
        time_dialog.open()

    def set_time(self, mode, time, button):
        formatted = time.strftime("%H:%M")
        if mode == "start":
            self.task_item.start_time = formatted
            button.text = f"Start: {self.task_item.start_time}"
        else:
            self.task_item.end_time = formatted
            button.text = f"End: {self.task_item.end_time}"

    def save_schedule(self):
        app = App.get_running_app()
        app.task_controller.set_time_slot(
            int(self.task_item.task_id),
            self.task_item.selected_date.strip(),
            self.task_item.start_time.strip(),
            self.task_item.end_time.strip()
        )
        self.dismiss()

        task_screen = app.sm.get_screen("tasks")
        Clock.schedule_once(lambda dt: task_screen.refresh_task_list(), 0.0)
