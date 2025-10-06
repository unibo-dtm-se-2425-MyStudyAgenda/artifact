from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.properties import StringProperty, BooleanProperty
from kivy.clock import Clock

class TaskItem(BoxLayout):
    description = StringProperty("")
    topic = StringProperty("")
    priority = StringProperty("")
    is_completed = BooleanProperty(False)

    def __init__(self, task, **kwargs):
        super().__init__(**kwargs)
        self.task_id = str(getattr(task, "task_id", getattr(task, "id", None)))
        self.description = task.description or ""
        self.topic = str(task.topic.name) if (task.topic and getattr(task.topic, "name", None)) else ""
        self.priority = {1: "Low", 2: "Medium", 3: "High"}.get(task.priority, "Low")
        self.is_completed = bool(getattr(task, "is_completed", False))

    def on_checkbox_active(self, checkbox, value):
        if getattr(self, "_initializing", False):
            return

        app = App.get_running_app()
        try:
            if value:
                app.task_controller.mark_completed(int(self.task_id))
            else:
                app.task_controller.mark_notcompleted(int(self.task_id))
        except Exception as e:
            print("Error updating completion status:", e)

        Clock.schedule_once(lambda dt: app.refresh_task_list(), 0.0)

    def delete_task(self):
        app = App.get_running_app()
        task_screen = app.sm.get_screen("tasks")
        app.task_controller.delete_task(int(self.task_id))
        Clock.schedule_once(lambda dt: task_screen.refresh_task_list(), 0.0)

    def open_schedule_popup(self):
        from kivy.uix.popup import Popup
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.textinput import TextInput
        from kivy.uix.button import Button

        layout = BoxLayout(orientation="vertical", spacing=10, padding=10)
        date_input = TextInput(hint_text="YYYY-MM-DD")
        start_input = TextInput(hint_text="HH:MM start")
        end_input = TextInput(hint_text="HH:MM end")
        save_btn = Button(text="Save")

        layout.add_widget(date_input)
        layout.add_widget(start_input)
        layout.add_widget(end_input)
        layout.add_widget(save_btn)

        popup = Popup(title="Schedule Task", content=layout, size_hint=(0.5, 0.5))

        def save_schedule(instance):
            app = App.get_running_app()
            app.task_controller.set_time_slot(
                int(self.task_id),
                date_input.text.strip(),
                start_input.text.strip(),
                end_input.text.strip()
            )
            popup.dismiss()
            task_screen = app.sm.get_screen("tasks")
            Clock.schedule_once(lambda dt: task_screen.refresh_task_list(), 0.0)

        save_btn.bind(on_release=save_schedule)
        popup.open()
