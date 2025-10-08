from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.properties import StringProperty, BooleanProperty
from kivy.clock import Clock
from kivymd.uix.button import MDFlatButton
from kivymd.uix.pickers import MDDatePicker, MDTimePicker
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout

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
        app.task_controller.delete_task(int(self.task_id))
        Clock.schedule_once(lambda dt: task_screen.refresh_task_list(), 0.0)
    
    def _to_date_text(self, v):
        if v is None:
            return ""
        if hasattr(v, "isoformat"):
            return v.isoformat()
        return str(v)

    def _to_time_text(self, v):
        if v is None:
            return ""
        if hasattr(v, "strftime"):
            return v.strftime("%H:%M")
        s = str(v)
        return s[:5] if len(s) >= 5 and s[2] == ":" else s

    def open_schedule_popup(self):
        layout = BoxLayout(orientation="vertical", spacing=10, padding=10)
        
        date_btn = MDFlatButton(
            text=f"Date: {self.selected_date or 'Select'}",
            on_release=lambda x: self.open_date_picker(date_btn)
        )
        start_btn = MDFlatButton(
            text=f"Start: {self.start_time or 'Select'}",
            on_release=lambda x: self.open_time_picker("start", start_btn)
        )
        end_btn = MDFlatButton(
            text=f"End: {self.end_time or 'Select'}",
            on_release=lambda x: self.open_time_picker("end", end_btn)
        )
        save_btn = MDFlatButton(text="Save", on_release=lambda x: self.save_schedule(popup))

        layout.add_widget(date_btn)
        layout.add_widget(start_btn)
        layout.add_widget(end_btn)
        layout.add_widget(save_btn)

        popup = Popup(title="Schedule Task", content=layout, size_hint=(0.7, 0.5))
        popup.open()

    def open_date_picker(self, button):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=lambda instance, value, date_range: self.set_date(value, button))
        date_dialog.open()

    def set_date(self, date, button):
        self.selected_date = str(date)
        button.text = f"Date: {self.selected_date}"

    def open_time_picker(self, mode, button):
        time_dialog = MDTimePicker()
        time_dialog.bind(time=lambda instance, time: self.set_time(mode, time, button))
        time_dialog.open()
    
    def set_time(self, mode, time, button):
        if mode == "start":
            self.start_time = str(time)
            button.text = f"Start: {self.start_time}"
        else:
            self.end_time = str(time)
            button.text = f"End: {self.end_time}"

    def save_schedule(self, popup):
        app = App.get_running_app()
        task_screen = app.sm.get_screen("tasks")
        app.task_controller.set_time_slot(
            int(self.task_id),
            self.selected_date.strip(),
            self.start_time.strip(),
            self.end_time.strip()
        )
        popup.dismiss()
        Clock.schedule_once(lambda dt: task_screen.refresh_task_list(), 0.0)