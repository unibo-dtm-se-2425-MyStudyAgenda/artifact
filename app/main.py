from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from app.view.task_screen import TaskScreen
from app.view.planner_screen import PlannerScreen
from app.view.notes_screen import NotesScreen
from app.view.pomodoro_screen import PomodoroScreen
from app.controller.topic_controller import TopicController
from app.controller.task_controller import TaskController
from app.controller.note_controller import NoteController

Builder.load_file("view/nav_bar.kv")
Builder.load_file("view/task_screen.kv")
Builder.load_file("view/planner_screen.kv")
Builder.load_file("view/notes_screen.kv")
Builder.load_file("view/pomodoro_screen.kv")

class MyStudyAgenda(App):
    def build(self):
        self.topic_controller = TopicController()
        self.task_controller = TaskController()
        self.note_controller = NoteController()
        self.sm = ScreenManager()
        self.sm.add_widget(TaskScreen(name="tasks"))
        self.sm.add_widget(PlannerScreen(name="planner"))
        self.sm.add_widget(NotesScreen(name="notes"))
        self.sm.add_widget(PomodoroScreen(name="pomodoro"))
        return self.sm

if __name__ == "__main__":
    MyStudyAgenda().run()
