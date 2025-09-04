from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.uix.popup import Popup
from view.task_item import TaskItem
from kivymd.uix.pickers import MDDatePicker, MDTimePicker

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
    
    def add_task_from_popup(self, desc, topic, prio, date, start, end, popup):
        app = App.get_running_app()
        if not desc or not topic or prio == "":
            print("Missing required fields")
            return

        try:
            prio = int(prio)
        except ValueError:
            print("Priority must be an integer")
            return

        task_id = app.task_controller.create_task(
            description=desc,
            topic_name=topic,
            priority=prio,
            date=date if date else None,
            start_time=start if start else None,
            end_time=end if end else None
        )
        print(f"Task created with ID: {task_id}")
        popup.dismiss()
    
    def refresh_task_list(self):
        app = App.get_running_app()
        task_screen = app.sm.get_screen("tasks")
        task_screen.load_tasks()


class AddTaskPopup(Popup):
    selected_date = ""
    start_time = ""
    end_time = ""

    def on_open(self):
        app = App.get_running_app()
        topics = app.topic_controller.get_all_topics()
        topic_names = [t["name"] if isinstance(t, dict) else t.name for t in topics]
        self.ids.topic_spinner.values = topic_names

    def open_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.set_date)
        date_dialog.open()

    def set_date(self, instance, value, date_range=None):
        formatted = value.isoformat()
        self.selected_date = formatted
        self.ids.date_btn.text = f"Date: {formatted}"

    def open_time_picker(self, mode):
        time_dialog = MDTimePicker()
        time_dialog.bind(time=lambda inst, time: self.set_time(mode, time))
        time_dialog.open()

    def set_time(self, mode, time):
        formatted = time.strftime("%H:%M")
        if mode == "start":
            self.start_time = formatted
            self.ids.start_btn.text = f"Start: {formatted}"
        else:
            self.end_time = formatted
            self.ids.end_btn.text = f"End: {formatted}"

    def add_task(self):
        desc = self.ids.desc_input.text.strip()
        topic = self.ids.topic_spinner.text.strip()
        prio_label = self.ids.priority_spinner.text.strip()

        date = self.selected_date if hasattr(self, "selected_date") else None
        start = self.start_time if hasattr(self, "start_time") else None
        end = self.end_time if hasattr(self, "end_time") else None

        priority_map = {"Low": 1, "Medium": 2, "High": 3}
        prio = priority_map.get(prio_label)

        app = App.get_running_app()
        task_screen = app.sm.get_screen("tasks")

        task_screen.add_task_from_popup(desc, topic, prio, date, start, end, self)
        task_screen.refresh_task_list()

    def add_new_topic(self):
        from kivy.uix.textinput import TextInput
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.button import Button

        content = BoxLayout(orientation="vertical", spacing=10, padding=10)
        input_field = TextInput(hint_text="New topic name", multiline=False)
        btn_layout = BoxLayout(size_hint_y=None, height="44dp", spacing=10)
        btn_cancel = Button(text="Cancel")
        btn_add = Button(text="Add")

        btn_layout.add_widget(btn_cancel)
        btn_layout.add_widget(btn_add)

        content.add_widget(input_field)
        content.add_widget(btn_layout)

        popup = Popup(title="Add Topic", content=content, size_hint=(0.8, 0.4), auto_dismiss=False)

        btn_cancel.bind(on_release=popup.dismiss)

        def save_topic(_):
            new_topic = input_field.text.strip()
            if new_topic:
                app = App.get_running_app()
                app.topic_controller.create_topic(new_topic)
                self.on_open()
                popup.dismiss()

        btn_add.bind(on_release=save_topic)
        popup.open()
