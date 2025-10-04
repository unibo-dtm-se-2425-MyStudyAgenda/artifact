import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
import unittest
from datetime import date, time
from app.controller.task_controller import TaskController
from app.controller.topic_controller import TopicController
from app.controller.note_controller import NoteController
from app.model.task import Task
from app.model.topic import Topic
from app.model.note import Note
from app.db.database import Database

# ------------------------
# Base setup for controller tests
# ------------------------
class BaseControllerTest(unittest.TestCase):
    def setUp(self):
        # Use in-memory DB to avoid touching real planner.db
        Database._instance = Database(":memory:")
        self.db = Database.get_instance()

        # Reinitialize controllers before each test
        self.task_controller = TaskController()
        self.topic_controller = TopicController()
        self.note_controller = NoteController()


# ------------------------
# TopicController tests
# ------------------------
class TestTopicController(BaseControllerTest):
    def test_create_and_get_topic(self):
        # Create a topic and check it is retrievable
        self.topic_controller.create_topic("Math")
        topics = self.topic_controller.get_all_topics()
        self.assertEqual(len(topics), 1)
        self.assertEqual(topics[0].name, "Math")

    def test_get_topic_by_name_and_id(self):
        # Retrieve topic using both name and id
        self.topic_controller.create_topic("Science")
        t_by_name = self.topic_controller.get_topic_by_name("Science")
        self.assertIsNotNone(t_by_name)
        self.assertEqual(t_by_name.name, "Science")

        t_by_id = self.topic_controller.get_topic_by_id(t_by_name.id)
        self.assertEqual(t_by_id.name, "Science")

    def test_get_topic_id_and_name(self):
        # Get topic id from name and vice versa
        self.topic_controller.create_topic("History")
        topic_id = self.topic_controller.get_topic_id("History")
        self.assertIsInstance(topic_id, int)

        topic_name = self.topic_controller.get_topic_name(topic_id)
        self.assertEqual(topic_name, "History")


# ------------------------
# TaskController tests
# ------------------------
class TestTaskController(BaseControllerTest):
    def test_create_and_get_task(self):
        # Create a task and verify retrieval
        topic = Topic(name="Programming")
        self.topic_controller.dao.insert_topic(topic)

        task = Task(
            description="Finish project",
            topic=topic,
            priority=2,
            scheduled_date=date.today(),
            start_time=time(9, 0),
            end_time=time(11, 0)
        )
        task_id = self.task_controller.create_task(task)
        self.assertIsInstance(task_id, int)

        tasks = self.task_controller.get_all_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].description, "Finish project")

    def test_mark_completed_and_notcompleted(self):
        # Mark a task completed, then revert to not completed
        task = Task(description="Test task", priority=1)
        task_id = self.task_controller.create_task(task)

        self.task_controller.mark_completed(task_id)
        tasks = self.task_controller.get_all_tasks()
        self.assertTrue(tasks[0].is_completed)

        self.task_controller.mark_notcompleted(task_id)
        tasks = self.task_controller.get_all_tasks()
        self.assertFalse(tasks[0].is_completed)

    def test_delete_task(self):
        # Delete an existing task
        task = Task(description="Temp task", priority=1)
        task_id = self.task_controller.create_task(task)

        self.task_controller.delete_task(task_id)
        tasks = self.task_controller.get_all_tasks()
        self.assertEqual(len(tasks), 0)


# ------------------------
# NoteController tests
# ------------------------
class TestNoteController(BaseControllerTest):
    def test_create_and_get_note(self):
        # Create a note and verify retrieval
        note = Note(title="My Note", content="Some text")
        note_id = self.note_controller.create_note(note)
        self.assertIsInstance(note_id, int)

        notes = self.note_controller.get_all_notes()
        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0].title, "My Note")

    def test_get_note_by_id(self):
        # Retrieve a note by id
        note = Note(title="Check ID", content="Test")
        note_id = self.note_controller.create_note(note)

        retrieved = self.note_controller.get_note_by_id(note_id)
        self.assertEqual(retrieved.title, "Check ID")

    def test_update_and_delete_note(self):
        # Update note content and then delete it
        note = Note(title="Draft", content="Old")
        note_id = self.note_controller.create_note(note)

        self.note_controller.update_note(note_id, "Updated")
        updated = self.note_controller.get_note_by_id(note_id)
        self.assertEqual(updated.content, "Updated")

        self.note_controller.delete_note(note_id)
        notes = self.note_controller.get_all_notes()
        self.assertEqual(len(notes), 0)


if __name__ == "__main__":
    unittest.main()
