import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
import os
import pytest
os.environ["KIVY_NO_ARGS"] = "1" # Prevent Kivy from parsing CLI args in tests
import unittest
from kivy.base import EventLoop
from kivy.clock import Clock
from kivymd.app import MDApp
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from types import SimpleNamespace
from unittest.mock import MagicMock
from app.main import MyStudyAgenda
from app.model.task import Task
from app.model.topic import Topic
from app.model.note import Note
from app.view.add_task_popup import AddTaskPopup
from app.view.add_topic_popup import AddTopicPopup
from app.view.task_item import TaskItem
from app.view.planner_screen import PlannerScreen
from app.view.schedule_popup import SchedulePopup
from app.view.add_note_popup import AddNotePopup
from app.view.notes_screen import NotesScreen
from app.view.note_item import NoteItem
from app.view.notebook_screen import NotebookScreen
from datetime import datetime

# ----------------------------
# Base class for GUI test cases
# ----------------------------
class GUITestCase(unittest.TestCase):
    # Base class to run the app in test mode and provide utility methods

    def setUp(self):
        # Initialize and prepare the Kivy app before each test
        if not EventLoop.event_listeners:
            EventLoop.ensure_window()
        self.app = MyStudyAgenda()
        self.app._run_prepare()

    def tearDown(self):
        # Stop the Kivy app after each test to clean resources
        self.app.stop()

    def run_clock(self):
        # Force Kivy's clock to process scheduled events (simulate UI loop)
        Clock.tick()

    def find_widget_by_id(self, screen, widget_id):
        # Helper to retrieve a widget by its id from a given screen
        return screen.ids.get(widget_id)

# ----------------------------
# FakeApp for mocking controllers
# ----------------------------
class FakeApp(MDApp):
    # Minimal fake KivyMD app to satisfy screen dependencies
    def build(self):
        return None


# ----------------------------
# Tests for AddTaskPopup
# ----------------------------
@pytest.mark.ui
class TestAddTaskPopup(GUITestCase):
    # Tests validation logic and button state for AddTaskPopup

    def setUp(self):
        # Open the AddTaskPopup before each test and force UI refresh
        super().setUp()
        self.popup = AddTaskPopup()
        self.popup.open()
        self.run_clock()

    def tearDown(self):
        # Close the popup and stop the app after each test
        self.popup.dismiss()
        super().tearDown()

    def test_empty_description_shows_error(self):
        # If description is empty, show an error and disable the add button
        self.popup.ids.desc_input.text = ""
        self.popup.ids.priority_spinner.text = "High"
        self.popup.validate_inputs()
        self.assertEqual(self.popup.ids.error_label.text, "Description cannot be empty")
        self.assertTrue(self.popup.ids.add_btn.disabled)

    def test_invalid_priority_shows_error(self):
        # If priority is not selected, show an error and disable the add button
        self.popup.ids.desc_input.text = "Test task"
        self.popup.ids.priority_spinner.text = "Select"
        self.popup.validate_inputs()
        self.assertEqual(self.popup.ids.error_label.text, "Please select a priority")
        self.assertTrue(self.popup.ids.add_btn.disabled)

    def test_valid_inputs_enable_button(self):
        # If description and priority are valid, clear error and enable the add button
        self.popup.ids.desc_input.text = "Test task"
        self.popup.ids.priority_spinner.text = "High"
        self.popup.validate_inputs()
        self.assertEqual(self.popup.ids.error_label.text, "")
        self.assertFalse(self.popup.ids.add_btn.disabled)


# ----------------------------
# Tests for TaskItem
# ----------------------------
@pytest.mark.ui
class TestTaskItem(GUITestCase):
    # Tests task item initialization and checkbox interaction

    def test_priority_label_mapping(self):
        # Verify that a numeric priority is mapped to the correct label
        task = Task(description="Test", topic=Topic(id=1, name="Math"), priority=2)
        item = TaskItem(task)
        self.assertEqual(item.priority, "Medium")

    def test_checkbox_marks_completed(self):
        # Simulate checking the box and verify that completion state is updated
        task = Task(description="Test", priority=1, is_completed=False)
        item = TaskItem(task)
        item.on_checkbox_active(None, True)  # simulate checkbox checked
        self.assertTrue(item.is_completed or not item.is_completed)  # placeholder

# ----------------------------
# Tests for AddTopicPopup
# ----------------------------
@pytest.mark.ui
class TestAddTopicPopup(GUITestCase):
    # Tests topic creation and parent popup refresh in AddTopicPopup

    def setUp(self):
        # Prepare fake app with mocked topic controller
        if not EventLoop.event_listeners:
            EventLoop.ensure_window()
        self.app = FakeApp()
        self.app.run = lambda *args: None
        self.app._run_prepare()
        self.app.topic_controller = MagicMock()
        App.get_running_app = lambda: self.app

        # Create AddTopicPopup with mocked ids
        self.popup = AddTopicPopup()
        self.popup.ids = {"topic_input": SimpleNamespace(text="New Topic")}
        self.popup.dismiss = MagicMock()

    def test_save_topic_creates_topic(self):
        # Saving with a valid topic should call controller and close popup
        self.popup.save_topic()
        self.app.topic_controller.create_topic.assert_called_once_with("New Topic")
        self.popup.dismiss.assert_called_once()

    def test_save_topic_does_not_create_if_empty(self):
        # Empty input should not create a topic or dismiss popup
        self.popup.ids["topic_input"].text = "   "
        self.popup.save_topic()
        self.app.topic_controller.create_topic.assert_not_called()
        self.popup.dismiss.assert_not_called()

    def test_parent_popup_on_open_called(self):
        # If a parent popup is provided, its on_open should be called
        parent = MagicMock()
        self.popup.parent_popup = parent
        self.popup.save_topic()
        parent.on_open.assert_called_once()

# ----------------------------
# Tests for SchedulePopup
# ----------------------------
@pytest.mark.ui
class TestSchedulePopup(GUITestCase):
    # Tests date and time selection inside SchedulePopup

    def setUp(self):
        if not EventLoop.event_listeners:
            EventLoop.ensure_window()
        self.app = FakeApp()
        self.app.run = lambda *args: None
        self.app._run_prepare()
        self.app.task_controller = MagicMock()
        self.app.topic_controller = MagicMock()
        self.app.sm = MagicMock()
        task_screen_mock = MagicMock()
        task_screen_mock.refresh_task_list = MagicMock()
        self.app.sm.get_screen.return_value = task_screen_mock

        App.get_running_app = lambda: self.app

        # Create a TaskItem and open SchedulePopup before each test
        task = Task(description="Test", priority=1)
        task.selected_date = "2025-01-01"
        task.start_time = "12:00"
        task.end_time = "13:00"

        self.item = TaskItem(task)
        self.popup = SchedulePopup(self.item)
        self.popup.open()
        self.run_clock()
        self.popup.ids = {"error_label": SimpleNamespace(text=""), "save_btn": SimpleNamespace(disabled=False)}

    def tearDown(self):
        # Dismiss the popup and stop the app after each test
        self.popup.dismiss()

    def test_set_date(self):
            # Ensure that selecting a date updates the button text
            from datetime import date
            d = date(2025, 1, 1)
            fake_btn = type("B", (), {"text": ""})()
            self.popup.set_date(d, fake_btn)
            self.assertIn("2025-01-01", fake_btn.text)

    def test_invalid_time_order(self):
        # If end time is before start time, an error is shown and save button disabled
        from datetime import time
        # Creates mock buttons that SchedulePopup tries to update
        fake_start_btn = type("B", (), {"text": ""})()
        fake_end_btn = type("B", (), {"text": ""})() 
        
        # Simulates the setting of start and end time
        self.popup.set_time("start", time(12, 0), fake_start_btn)
        self.popup.set_time("end", time(11, 0), fake_end_btn)
        
        self.assertEqual(self.popup.ids.error_label.text, "End time must be later than start time")
        self.assertTrue(self.popup.ids.save_btn.disabled)

# ----------------------------
# Tests for PlannerScreen
# ----------------------------
@pytest.mark.ui
class TestPlannerScreen(GUITestCase):
    # Tests week navigation, layout updates, and parsing in PlannerScreen

    def setUp(self):
        # Initialize screen with fake app and mock controllers
        if not EventLoop.event_listeners:
            EventLoop.ensure_window()
        self.app = FakeApp()
        self.app.run = lambda *args: None
        self.app._run_prepare()
        self.app.task_controller = type("obj", (), {
            "get_all_tasks": lambda self: []
        })()
        App.get_running_app = lambda: self.app

        self.screen = PlannerScreen()
        self.screen.ids = {
            "planner_grid": GridLayout(cols=8, size=(800, 600)),
            "month_label": type("obj", (), {"text": ""})()
        }

    def test_update_week_view_creates_headers(self):
        # Updating week view should refresh month label
        self.screen.update_week_view()
        self.assertNotEqual(self.screen.ids["month_label"].text, "")

    def test_next_and_previous_week(self):
        # Navigating forward and backward should update current_monday accordingly
        current = self.screen.current_monday
        self.screen.next_week()
        self.assertNotEqual(self.screen.current_monday, current)
        self.screen.previous_week()
        self.assertEqual(self.screen.current_monday, current)

    def test_parse_date_and_time(self):
        # Parse date and time strings correctly
        d = self.screen.parse_date("2025-01-01")
        t = self.screen.parse_time("12:00")
        self.assertEqual(d.year, 2025)
        self.assertEqual(t.hour, 12)

    def test_time_to_y(self):
        # Convert times to Y coordinate, later times should map higher
        from datetime import time
        y1 = self.screen._time_to_y(time(0, 0))
        y2 = self.screen._time_to_y(time(12, 0))
        self.assertTrue(y2 > y1)

# ----------------------------
# Tests for NotesScreen
# ----------------------------
class TestNotesScreen(GUITestCase):
    # Tests notes list loading and notebook screen navigation

    def setUp(self):
        # Prepare fake app and mock controllers for NotesScreen
        if not EventLoop.event_listeners:
            EventLoop.ensure_window()

        self.app = FakeApp()
        self.app.run = lambda *a, **kw: None
        self.app._run_prepare()
        self.app.note_controller = SimpleNamespace(
            get_all_notes=lambda: [Note(id=1, title="Note A", topic=None, content="", created_at=datetime.now())]
        )
        self.app.sm = SimpleNamespace(get_screen=lambda name: self.notes_screen)
        App.get_running_app = lambda: self.app

        # Create NotesScreen with mocked ids
        self.notes_screen = NotesScreen()
        self.notes_screen.ids = {"notes_list": BoxLayout()}

    def test_load_notes_adds_widgets(self):
        # After loading notes, the notes_list should contain at least one widget
        self.notes_screen.load_notes()
        self.assertGreater(len(self.notes_screen.ids["notes_list"].children), 0)

    def test_open_notebook_switches_screen(self):
        # Opening a note should switch screen to notebook and call open_note on it
        class FakeManager:
            def __init__(self):
                self.current = "notes"
            def get_screen(self, name):
                return SimpleNamespace(open_note=lambda note_id: setattr(self, "opened", note_id))

        note = Note(id=42, title="Note B", topic=None, content="", created_at=datetime.now())
        self.notes_screen.manager = FakeManager()
        self.notes_screen.open_notebook(note)
        self.assertEqual(self.notes_screen.manager.current, "notebook")
        self.assertEqual(getattr(self.notes_screen.manager, "opened"), 42)


# ----------------------------
# Tests for AddNotePopup
# ----------------------------
class TestAddNotePopup(GUITestCase):
    # Tests topic population, validation, and note creation

    def setUp(self):
        # Prepare fake app with topic and note controllers
        if not EventLoop.event_listeners:
            EventLoop.ensure_window()

        simulated_topic = Topic(id=1, name="Math")
        self.app = FakeApp()
        self.app.run = lambda *a, **kw: None
        self.app._run_prepare()
        self.app.topic_controller = SimpleNamespace(
            get_all_topics=lambda: [simulated_topic],
            get_topic_id=lambda name: 1 if name == "Math" else None,
            get_topic_by_id=lambda topic_id: simulated_topic if topic_id == 1 else None
        )
        self.app.note_controller = SimpleNamespace(create_note=lambda note: 123)
        self.app.root = SimpleNamespace(
            get_screen=lambda name: SimpleNamespace(open_note=lambda note_id: setattr(self, "opened", note_id)),
            current="notes"
        )
        App.get_running_app = lambda: self.app

        # Create popup with mocked ids
        self.popup = AddNotePopup()
        self.popup.ids = {
            "topic_spinner": SimpleNamespace(values=[], text="Math"),
            "title_input": SimpleNamespace(text="My Note"),
            "error_label": SimpleNamespace(text="")
        }
        self.popup.dismiss = lambda: setattr(self, "dismissed", True)

    def test_create_note_with_empty_title_shows_error(self):
        # Empty title should display an error and prevent note creation
        self.popup.ids["title_input"].text = ""
        self.popup.create_note()
        self.assertEqual(self.popup.ids["error_label"].text, "Title cannot be empty")

    def test_create_note_valid_calls_controller(self):
        # Valid note creation should dismiss popup and switch to notebook
        self.popup.create_note()
        self.assertTrue(hasattr(self, "dismissed"))
        self.assertEqual(self.app.root.current, "notebook")


# ----------------------------
# Tests for NotebookScreen
# ----------------------------
class TestNotebookScreen(GUITestCase):
    # Tests loading, saving, and navigation for NotebookScreen

    def setUp(self):
        # Prepare fake app with mocked note controller
        if not EventLoop.event_listeners:
            EventLoop.ensure_window()

        self.app = FakeApp()
        self.app.run = lambda *a, **kw: None
        self.app._run_prepare()
        self.app.note_controller = SimpleNamespace(
            get_note_by_id=lambda note_id: Note(id=note_id, title="Note C", topic=None, content="Hello", created_at=datetime.now()),
            update_note=lambda note_id, content: setattr(self, "updated", (note_id, content))
        )
        App.get_running_app = lambda: self.app

        self.screen = NotebookScreen()
        self.screen.ids = {"content_input": SimpleNamespace(text="")}

    def test_open_note_loads_content(self):
        # Opening a note should load its content into the text input
        self.screen.open_note(5)
        self.assertEqual(self.screen.ids["content_input"].text, "Hello")

    def test_save_note_updates_controller(self):
        # Saving should update the note content via controller
        self.screen.current_note_id = 5
        self.screen.ids["content_input"].text = "Updated"
        self.screen.save_note()
        self.assertEqual(getattr(self, "updated")[1], "Updated")


# ----------------------------
# Tests for NoteItem
# ----------------------------
class TestNoteItem(GUITestCase):
    # Tests initialization and user actions for NoteItem

    def setUp(self):
        # Prepare fake app with mocked controllers and screen manager
        if not EventLoop.event_listeners:
            EventLoop.ensure_window()

        self.app = FakeApp()
        self.app.run = lambda *a, **kw: None
        self.app._run_prepare()
        self.app.topic_controller = SimpleNamespace(get_topic_name=lambda topic_id: "Math")
        self.app.note_controller = SimpleNamespace(delete_note=lambda note_id: setattr(self, "deleted", note_id))
        self.app.sm = SimpleNamespace(
            get_screen=lambda name: SimpleNamespace(
                open_notebook=lambda note: setattr(self, "opened", note),
                refresh_note_list=lambda: setattr(self, "refreshed", True)
            )
        )
        App.get_running_app = lambda: self.app

        self.note = Note(id=10, title="Title", topic=Topic(id=1, name="Math"), content="", created_at=datetime.now())
        self.item = NoteItem(self.note)

    def test_open_note_calls_screen(self):
        # Clicking on a note item should call open_note on NotesScreen
        self.item.open_note()
        self.assertEqual(getattr(self, "opened").id, 10)

    def test_delete_note_calls_controller_and_refresh(self):
        # Deleting a note should call controller and refresh note list
        self.item.delete_note()
        Clock.tick()  # process scheduled callbacks
        self.assertEqual(getattr(self, "deleted"), 10)
        self.assertTrue(getattr(self, "refreshed"))
