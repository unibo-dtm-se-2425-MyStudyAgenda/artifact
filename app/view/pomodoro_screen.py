from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.app import App
from kivymd.uix.dialog import MDDialog

class PomodoroScreen(Screen):
    study_duration = 0
    break_duration = 0
    remaining_time = 0
    is_study = True
    timer_event = None

    def start_pomodoro(self):
        try:
            self.study_duration = int(self.ids.study_spinner.text) * 60
            self.break_duration = int(self.ids.break_spinner.text) * 60
        except ValueError:
            print("Invalid input")
            return

        if self.study_duration <= 0 or self.break_duration <= 0:
            print("Durations must be positive")
            return

        self.is_study = True
        self.start_phase(self.study_duration)

        # changes the view 
        self.ids.setup_view.opacity = 0
        self.ids.timer_view.opacity = 1

    def start_phase(self, duration):
        self.remaining_time = duration
        if self.timer_event:
            self.timer_event.cancel()
        self.timer_event = Clock.schedule_interval(self.update_timer, 1)

    def update_timer(self, dt):
        if self.remaining_time > 0:
            self.remaining_time -= 1
            minutes, seconds = divmod(self.remaining_time, 60)
            self.ids.timer_label.text = f"{minutes:02d}:{seconds:02d}"
        else:
            self.timer_event.cancel()
            self.show_alert()

    def show_alert(self):
        phase = "Study" if self.is_study else "Break"
        next_phase = "Break" if self.is_study else "Study"

        dialog = MDDialog(
            title=f"{phase} finished!",
            text=f"{next_phase} starts now!",
            buttons=[],
        )
        dialog.open()

        Clock.schedule_once(lambda dt: dialog.dismiss(), 4)  # the dialog has a duration of 4 seconds

        # the next "phase" is started
        self.is_study = not self.is_study
        duration = self.study_duration if self.is_study else self.break_duration
        self.start_phase(duration)

    def reset_pomodoro(self):
        if self.timer_event:
            self.timer_event.cancel()
        self.ids.setup_view.opacity = 1
        self.ids.timer_view.opacity = 0
        self.ids.study_spinner.text = "25"
        self.ids.break_spinner.text = "5"
        self.ids.timer_label.text = "00:00"

    def stop_session(self):
        if self.timer_event:
            self.timer_event.cancel()
        self.reset_pomodoro()
