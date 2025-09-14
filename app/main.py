from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from view.task_screen import TaskScreen
from view.planner_screen import PlannerScreen
from view.notes_screen import NotesScreen
from view.notes_screen import NotebookScreen
from controller.task_controller import TaskController
from controller.topic_controller import TopicController
from controller.note_controller import NoteController

Builder.load_file("view/nav_bar.kv")
Builder.load_file("view/task_screen.kv")
Builder.load_file("view/planner_screen.kv")
Builder.load_file("view/notes_screen.kv")
Builder.load_file("view/task_item.kv")
Builder.load_file("view/add_topic_popup.kv")

class MyStudyAgenda(MDApp):
    def build(self):
        self.task_controller = TaskController()
        self.topic_controller = TopicController()
        self.note_controller = NoteController()
        self.sm = ScreenManager()
        self.sm.add_widget(TaskScreen(name="tasks"))
        self.sm.add_widget(PlannerScreen(name="planner"))
        self.sm.add_widget(NotesScreen(name="notes"))
        self.sm.add_widget(NotebookScreen(name="notebook"))
        return self.sm

if __name__ == "__main__":
    MyStudyAgenda().run()