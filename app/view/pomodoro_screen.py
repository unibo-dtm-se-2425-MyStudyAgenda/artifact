from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivymd.uix.dialog import MDDialog

class PomodoroScreen(Screen):
    # Default attributes for Pomodoro session
    study_duration = 0
    break_duration = 0
    remaining_time = 0
    is_study = True
    timer_event = None

    def start_pomodoro(self):
        # Initialize the Pomodoro session using user-selected durations
        try:
            self.study_duration = int(self.ids.study_spinner.text) * 60
            self.break_duration = int(self.ids.break_spinner.text) * 60
        except ValueError:
            print("Invalid input")
            return

        self.is_study = True
        self.start_phase(self.study_duration)

        # Switch view: hide setup, show timer
        self.ids.setup_view.opacity = 0
        self.ids.timer_view.opacity = 1

    def start_phase(self, duration):
        # Start a new phase (study or break) with the given duration
        self.remaining_time = duration
        if self.timer_event:
            self.timer_event.cancel()
        self.timer_event = Clock.schedule_interval(self.update_timer, 1)

    def update_timer(self, dt):
        # Update the countdown every second and refresh the timer label
        if self.remaining_time > 0:
            self.remaining_time -= 1
            minutes, seconds = divmod(self.remaining_time, 60)
            self.ids.timer_label.text = f"{minutes:02d}:{seconds:02d}"
        else:
            # Phase finished: stop current timer and notify user with a dialog
            self.timer_event.cancel()
            self.show_alert()

    def show_alert(self):
        # Show a temporary alert dialog when a phase ends and automatically start the next one
        phase = "Study" if self.is_study else "Break"
        next_phase = "Break" if self.is_study else "Study"

        dialog = MDDialog(
            title=f"{phase} finished!",
            text=f"{next_phase} starts now!",
            buttons=[],
        )
        dialog.open()

        # Auto-dismiss after 4 seconds
        Clock.schedule_once(lambda dt: dialog.dismiss(), 4)

        # Switch to next phase
        self.is_study = not self.is_study
        duration = self.study_duration if self.is_study else self.break_duration
        self.start_phase(duration)

    def reset_pomodoro(self):
        # Reset the Pomodoro session to its default setup state
        if self.timer_event:
            self.timer_event.cancel()
        self.ids.setup_view.opacity = 1
        self.ids.timer_view.opacity = 0
        self.ids.study_spinner.text = "25"
        self.ids.break_spinner.text = "5"
        self.ids.timer_label.text = "00:00"

    def stop_session(self):
        # Stop the current Pomodoro session and reset everything
        if self.timer_event:
            self.timer_event.cancel()
        self.reset_pomodoro()
