from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.uix.popup import Popup
from view.task_item import TaskItem
from kivymd.uix.pickers import MDDatePicker, MDTimePicker
from view.add_topic_popup import AddTopicPopup
from model.task import Task
from model.topic import Topic

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
        if not desc or not topic_name or prio == "":
            print("Missing required fields")
            return
        
        if topic_name != "Select topic":
            topic_id = app.topic_controller.get_topic_id(topic_name)

        try:
            prio = int(prio)
        except ValueError:
            print("Priority must be an integer")
            return
        
        task = Task(
            task_id = None,
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
        popup = AddTopicPopup(parent_popup=self)
        popup.open()