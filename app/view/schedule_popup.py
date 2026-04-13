from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivymd.uix.pickers.datepicker import MDModalDatePicker
from kivymd.uix.pickers.timepicker import MDTimePickerInput
from kivy.uix.popup import Popup

class SchedulePopup(Popup):
    # Popup to schedule a task
    
    task_item = ObjectProperty(None)

    def __init__(self, task_item, **kwargs):
        super().__init__(**kwargs)
        self.task_item = task_item

    def open_date_picker(self, button):
        # Open date picker and bind result to set_date
        date_dialog = MDModalDatePicker()
        date_dialog.bind(on_ok=lambda instance: self.set_date(instance, button))
        date_dialog.bind(on_cancel=lambda instance: instance.dismiss())
        date_dialog.open()

    def set_date(self, instance, button):
        # Update task date after selection
        # Get the selected dates from the instance directly
        # get_date() returns a list of datetime.date objects
        selection = instance.get_date()
        if selection:
            self.task_item.selected_date = selection[0].isoformat()
            button.text = f"Date: {self.task_item.selected_date}"
        
        instance.dismiss()

    def open_time_picker(self, mode, button):
        # Open time picker (for start or end time)
        time_dialog = MDTimePickerInput()
        time_dialog.bind(on_ok=lambda instance: self.set_time(instance, mode, button))
        time_dialog.bind(on_cancel=lambda instance: instance.dismiss())
        time_dialog.open()

    def set_time(self, instance, mode, button):
        # Update task start/end time after selection
        # Access the time from the instance (instance.time is a datetime.time object)
        selected_time = instance.time
        formatted = selected_time.strftime("%H:%M")
        
        if mode == "start":
            self.task_item.start_time = formatted
            button.text = f"Start: {self.task_item.start_time}"
        else:
            self.task_item.end_time = formatted
            button.text = f"End: {self.task_item.end_time}"

        # Validate time consistency after selection
        self.validate_times()
        instance.dismiss()

    def validate_times(self):
        # Ensure end time is later than start time, else disable save
        if self.task_item.start_time and self.task_item.end_time:
            from datetime import datetime
            fmt = "%H:%M"

            try:
                start_dt = datetime.strptime(self.task_item.start_time, fmt)
                end_dt = datetime.strptime(self.task_item.end_time, fmt)
            except ValueError:
                self.ids.error_label.text = "Invalid time format"
                self.ids.save_btn.disabled = True
                return

            if end_dt <= start_dt:
                self.ids.error_label.text = "End time must be later than start time"
                self.ids.save_btn.disabled = True
                return

        # If times are valid
        self.ids.error_label.text = ""
        self.ids.save_btn.disabled = False

    def save_schedule(self):
        # Persist scheduling info in the database and refresh task list
        app = App.get_running_app()
        app.task_controller.set_time_slot(
            int(self.task_item.task_id),
            self.task_item.selected_date.strip(),
            self.task_item.start_time.strip(),
            self.task_item.end_time.strip()
        )
        self.dismiss()

        # Refresh task list after saving
        task_screen = app.sm.get_screen("tasks")
        Clock.schedule_once(lambda dt: task_screen.refresh_task_list(), 0.0)