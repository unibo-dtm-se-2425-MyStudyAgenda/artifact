from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from view.task_screen import TaskScreen
from view.planner_screen import PlannerScreen
from view.notes_screen import NotesScreen
from controller.task_controller import TaskController

Builder.load_file("view/nav_bar.kv")
Builder.load_file("view/task_screen.kv")
Builder.load_file("view/planner_screen.kv")
Builder.load_file("view/notes_screen.kv")

class MyStudyAgenda(App):
    def build(self):
        self.task_controller = TaskController()
        self.sm = ScreenManager()
        self.sm.add_widget(TaskScreen(name="tasks"))
        self.sm.add_widget(PlannerScreen(name="planner"))
        self.sm.add_widget(NotesScreen(name="notes"))
        return self.sm

if __name__ == "__main__":
    MyStudyAgenda().run()