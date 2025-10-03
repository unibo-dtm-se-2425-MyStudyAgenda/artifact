import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
import unittest
from datetime import date, time
from app.db.database import Database
from app.db.note_dao import NoteDAO
from app.db.task_dao import TaskDAO
from app.db.topic_dao import TopicDAO
from app.model.note import Note
from app.model.task import Task
from app.model.topic import Topic

# ------------------------
# Base class for DAO tests
# ------------------------
class BaseDAOTest(unittest.TestCase):
    def setUp(self):
        # Use in-memory DB to keep tests isolated
        Database._instance = Database(":memory:")
        self.db = Database.get_instance()

        # Reinitialize DAOs for each test
        self.note_dao = NoteDAO()
        self.task_dao = TaskDAO()
        self.topic_dao = TopicDAO()

    def tearDown(self):
        # Safely close DB connection
        self.db.close()
        Database._instance = None


# ------------------------
# TopicDAO tests
# ------------------------
class TestTopicDAO(BaseDAOTest):
    def test_insert_and_get_topic(self):
        # Insert a topic and verify it is retrieved
        topic = Topic(name="Math")
        self.topic_dao.insert_topic(topic)

        result = self.topic_dao.get_all_topics()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], "Math")

    def test_get_topic_by_id_and_name(self):
        # Retrieve topic both by name and by id
        topic = Topic(name="Science")
        self.topic_dao.insert_topic(topic)

        t_by_name = self.topic_dao.get_topic_by_name("Science")
        self.assertIsNotNone(t_by_name)
        self.assertEqual(t_by_name[1], "Science")

        t_by_id = self.topic_dao.get_topic_by_id(t_by_name[0])
        self.assertEqual(t_by_id[1], "Science")


# ------------------------
# NoteDAO tests
# ------------------------
class TestNoteDAO(BaseDAOTest):
    def test_insert_and_get_note(self):
        # Insert a note and fetch it by id
        topic = Topic(name="Subject")
        note = Note(title="My Note", topic=topic, content="Hello world")
        note_id = self.note_dao.insert_note(note)

        fetched = self.note_dao.get_note_by_id(note_id)
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched[1], "My Note")
        self.assertEqual(fetched[2], topic.id)
        self.assertEqual(fetched[3], "Hello world")

    def test_update_and_delete_note(self):
        # Update note content and then delete it
        note = Note(title="Temp Note", content="old")
        note_id = self.note_dao.insert_note(note)

        self.note_dao.update_note(note_id, "new content")
        updated = self.note_dao.get_note_by_id(note_id)
        self.assertEqual(updated[3], "new content")

        self.note_dao.delete_note(note_id)
        deleted = self.note_dao.get_note_by_id(note_id)
        self.assertIsNone(deleted)


# ------------------------
# TaskDAO tests
# ------------------------
class TestTaskDAO(BaseDAOTest):
    def test_insert_and_get_task(self):
        # Insert a task with schedule and check values
        task = Task(
            description="Study math",
            topic=None,
            priority=2,
            is_completed=False,
            scheduled_date=date(2025, 1, 1),
            start_time=time(10, 0),
            end_time=time(11, 0),
        )
        self.task_dao.insert_task(task)

        tasks = self.task_dao.get_all_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0][1], "Study math")
        self.assertEqual(tasks[0][4], 2)

    def test_mark_completed_and_notcompleted(self):
        # Mark a task as completed and then not completed
        task = Task(description="Do homework", priority=1)
        task_id = self.task_dao.insert_task(task)

        self.task_dao.mark_completed(task_id)
        updated = self.task_dao.get_all_tasks()[0]
        self.assertEqual(updated[5], 1)

        self.task_dao.mark_notcompleted(task_id)
        updated = self.task_dao.get_all_tasks()[0]
        self.assertEqual(updated[5], 0)

    def test_set_time_slot_and_delete(self):
        # Assign time slot to a task and then delete it
        task = Task(description="Temp", priority=1)
        task_id = self.task_dao.insert_task(task)

        self.task_dao.set_time_slot(task_id, "2025-01-02", "12:00", "13:00")
        updated = self.task_dao.get_all_tasks()[0]
        self.assertEqual(updated[6], "2025-01-02")
        self.assertEqual(updated[7], "12:00")

        self.task_dao.delete_task(task_id)
        all_tasks = self.task_dao.get_all_tasks()
        self.assertEqual(len(all_tasks), 0)


if __name__ == "__main__":
    unittest.main()
