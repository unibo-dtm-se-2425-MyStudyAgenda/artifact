from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from view.task_screen import TaskScreen
from view.planner_screen import PlannerScreen
from view.notes_screen import NotesScreen
from view.components.task_item import TaskItem
from controller.task_controller import TaskController
from controller.topic_controller import TopicController

Builder.load_file("view/nav_bar.kv")
Builder.load_file("view/task_screen.kv")
Builder.load_file("view/planner_screen.kv")
Builder.load_file("view/notes_screen.kv")

class MyStudyAgenda(App):
    def build(self):
        self.task_controller = TaskController()
        self.topic_controller = TopicController()
        self.sm = ScreenManager()
        self.sm.add_widget(TaskScreen(name="tasks"))
        self.sm.add_widget(PlannerScreen(name="planner"))
        self.sm.add_widget(NotesScreen(name="notes"))
        return self.sm
    
    def add_task_from_popup(self, desc, topic, prio, date, start, end, popup):
        if not desc or not topic or prio == "":
            print("Missing required fields")
            return

        try:
            prio = int(prio)
        except ValueError:
            print("Priority must be an integer")
            return

        task_id = self.task_controller.create_task(
            description=desc,
            topic_name=topic,
            priority=prio,
            date=date if date else None,
            start_time=start if start else None,
            end_time=end if end else None
        )
        print(f"Task created with ID: {task_id}")
        popup.dismiss()

if __name__ == "__main__":
    MyStudyAgenda().run()