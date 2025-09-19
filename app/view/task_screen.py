from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.uix.popup import Popup
from view.task_item import TaskItem
from kivymd.uix.pickers import MDDatePicker, MDTimePicker
from view.add_topic_popup import AddTopicPopup
from model.task import Task
from model.topic import Topic

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
            task_id=None,
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


class AddTaskPopup(Popup):
    # Popup for creating a new task (includes fields, validation, and save logic)

    selected_date = ""
    start_time = ""
    end_time = ""
    prio_valid = False  # track priority validation

    def on_open(self):
        # Load topics into the spinner when the popup is opened
        app = App.get_running_app()
        topics = app.topic_controller.get_all_topics()
        topic_names = [t["name"] if isinstance(t, dict) else t.name for t in topics]
        self.ids.topic_spinner.values = topic_names

    def open_date_picker(self):
        # Open a date picker dialog for selecting the task date
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.set_date)
        date_dialog.open()

    def set_date(self, instance, value, date_range=None):
        # Set the selected date from the date picker
        formatted = value.isoformat()
        self.selected_date = formatted
        self.ids.date_btn.text = f"Date: {formatted}"

    def open_time_picker(self, mode):
        # Open a time picker dialog for selecting start or end time
        time_dialog = MDTimePicker()
        time_dialog.bind(time=lambda inst, time: self.set_time(mode, time))
        time_dialog.open()

    def set_time(self, mode, time):
        # Set the selected start or end time and validate them
        formatted = time.strftime("%H:%M")
        if mode == "start":
            self.start_time = formatted
            self.ids.start_btn.text = f"Start: {formatted}"
        else:
            self.end_time = formatted
            self.ids.end_btn.text = f"End: {formatted}"

        # Validate times after every change
        self.validate_inputs()

    def validate_inputs(self):
        # Validate description, priority and time consistency

        # Check description
        if not self.ids.desc_input.text.strip():
            self.ids.error_label.text = "Description cannot be empty"
            self.ids.add_btn.disabled = True
            return

        # Check priority
        # Ensure that a priority is selected before saving
        prio_label = self.ids.priority_spinner.text.strip()
        if prio_label not in {"Low", "Medium", "High"}:
            self.ids.error_label.text = "Please select a priority"
            self.ids.add_btn.disabled = True
            self.prio_valid = False
            return

        self.prio_valid = True

        # Check time
        # Ensure that end time is later than start time, otherwise disable save
        if self.start_time and self.end_time:
            from datetime import datetime
            fmt = "%H:%M"
            try:
                start_dt = datetime.strptime(self.start_time, fmt)
                end_dt = datetime.strptime(self.end_time, fmt)
            except ValueError:
                self.ids.error_label.text = "Invalid time format"
                self.ids.add_btn.disabled = True
                return

            if end_dt <= start_dt:
                self.ids.error_label.text = "End time must be later than start time"
                self.ids.add_btn.disabled = True
                return

        # If everything is valid
        self.ids.error_label.text = ""
        self.ids.add_btn.disabled = False

    def add_task(self):
        # Final check before saving
        if not self.prio_valid:
            self.ids.error_label.text = "Please select a priority"
            return

        # Collect input data and send task creation request to the TaskScreen
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

        self.validate_inputs()
        # blocks saving if sme input is invalid
        if self.ids.add_btn.disabled:
            return  

    def add_new_topic(self):
        # Open a popup to create a new topic directly from the task popup
        popup = AddTopicPopup(parent_popup=self)
        popup.open()
