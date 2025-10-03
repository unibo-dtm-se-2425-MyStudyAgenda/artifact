import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
import unittest
from datetime import date, time, datetime
from app.model.topic import Topic
from app.model.task import Task
from app.model.note import Note


# ---------------- Topic model tests ----------------
class TestTopic(unittest.TestCase):
    def setUp(self):
        Topic._id_counter = 1  # reset counter for consistent IDs

    def test_topic_creation_with_auto_id(self):
        # Should auto-increment id if not provided
        topic = Topic(name="Math")
        self.assertEqual(topic.id, 1)
        self.assertEqual(topic.name, "Math")

    def test_topic_creation_with_custom_id(self):
        # Should accept custom id
        topic = Topic(id=99, name="Science")
        self.assertEqual(topic.id, 99)
        self.assertEqual(topic.name, "Science")

    def test_topic_repr(self):
        # __repr__ should contain id and name
        topic = Topic(id=2, name="History")
        self.assertEqual(repr(topic), "Topic(id=2, name='History')")


# ---------------- Task model tests ----------------
class TestTask(unittest.TestCase):
    def setUp(self):
        Task._id_counter = 1  # reset counter
    
    def test_task_creation_with_auto_id(self):
        # Should auto-increment id if not provided
        task = Task()
        self.assertEqual(task.id, 1)
        self.assertEqual(task.description, "")
        self.assertFalse(task.is_completed)

    def test_task_with_topic_and_priority(self):
        # Task should store topic and priority correctly
        topic = Topic(id=1, name="Math")
        task = Task(id=10, description="Study algebra", topic=topic, priority=2)
        self.assertEqual(task.id, 10)
        self.assertEqual(task.description, "Study algebra")
        self.assertEqual(task.topic.name, "Math")
        self.assertEqual(task.priority, 2)

    def test_mark_completed_and_notcompleted(self):
        # Toggle completion status
        task = Task(description="Do homework")
        task.mark_completed()
        self.assertTrue(task.is_completed)
        task.mark_notcompleted()
        self.assertFalse(task.is_completed)

    def test_repr_contains_all_fields(self):
        # __repr__ should include description, topic and scheduling info
        topic = Topic(id=2, name="Science")
        task = Task(id=1, description="Lab report", topic=topic,
                    priority=3, is_completed=True,
                    scheduled_date=date(2025, 9, 19),
                    start_time=time(10, 0), end_time=time(11, 0))
        result = repr(task)
        self.assertIn("Lab report", result)
        self.assertIn("Science", result)
        self.assertIn("2025-09-19", result)


# ---------------- Note model tests ----------------
class TestNote(unittest.TestCase):
    def setUp(self):
        Note._id_counter = 1  # reset counter

    def test_note_creation_with_auto_id(self):
        # Should auto-increment id if not provided
        note = Note(title="My first note")
        self.assertEqual(note.id, 1)
        self.assertEqual(note.title, "My first note")
        self.assertEqual(note.content, "")

    def test_note_creation_with_topic(self):
        # Should link note to a topic
        topic = Topic(id=5, name="Math")
        note = Note(title="Lesson 1", topic=topic, content="2+2=4")
        self.assertEqual(note.topic.name, "Math")
        self.assertEqual(note.content, "2+2=4")

    def test_note_creation_with_custom_id_and_datetime(self):
        # Should accept custom id and created_at
        custom_date = datetime(2025, 1, 1, 12, 0)
        note = Note(id=42, title="Custom", created_at=custom_date)
        self.assertEqual(note.id, 42)
        self.assertEqual(note.created_at, custom_date)

    def test_note_repr(self):
        # __repr__ should include id and title
        note = Note(title="Testing")
        result = repr(note)
        self.assertIn("Testing", result)
        self.assertIn("Note(id=", result)


if __name__ == "__main__":
    unittest.main()
