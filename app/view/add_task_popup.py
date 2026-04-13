from kivy.app import App
from kivy.uix.popup import Popup
from kivymd.uix.pickers.datepicker import MDModalDatePicker
from kivymd.uix.pickers.timepicker import MDTimePickerInput
from app.view.add_topic_popup import AddTopicPopup
from app.view.manage_topics_popup import ManageTopicsPopup
from datetime import datetime

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

    def open_date_picker(self, button):
        # Open a date picker dialog for selecting the task date
        date_dialog = MDModalDatePicker()
        date_dialog.bind(on_ok=lambda instance: self.set_date(instance, button))
        date_dialog.bind(on_cancel=lambda instance: instance.dismiss())
        date_dialog.open()

    def set_date(self, instance, button):
        # Set the selected date from the date picker
        # Get the selected dates from the instance directly
        # get_date() returns a list of datetime.date objects in KivyMD 2.0
        selection = instance.get_date()
        if selection:
            self.selected_date = selection[0].isoformat()
            button.text = f"Date: {self.selected_date}"
        
        instance.dismiss()

    def open_time_picker(self, mode, button):
        # Open a time picker dialog for selecting start or end time
        time_dialog = MDTimePickerInput()
        time_dialog.bind(on_ok=lambda instance: self.set_time(instance, mode, button))
        time_dialog.bind(on_cancel=lambda instance: instance.dismiss())
        time_dialog.open()

    def set_time(self, instance, mode, button):
        # Set the selected start or end time and validate them
        # Access the time from the instance (instance.time is a datetime.time object)
        selected_time = instance.time
        formatted = selected_time.strftime("%H:%M")
        
        if mode == "start":
            self.start_time = formatted
            button.text = f"Start: {self.start_time}"
        else:
            self.end_time = formatted
            button.text = f"End: {self.end_time}"

        self.validate_inputs()
        instance.dismiss()

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

    def open_manage_topics(self):
        # Open a popup for topic management directly from the task popup
        popup = ManageTopicsPopup(parent_popup=self)
        popup.open()