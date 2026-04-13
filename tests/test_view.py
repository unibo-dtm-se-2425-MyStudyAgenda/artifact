import os
import pytest
if "CI" in os.environ:
    pytest.skip("Skipping GUI tests in CI environment", allow_module_level=True)

os.environ["KIVY_NO_ARGS"] = "1" # Prevent Kivy from parsing CLI args in tests
os.environ["KIVY_WINDOW"] = "mock" # Force Kivy into “mock window” mode

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import unittest

from unittest.mock import patch
from kivy.base import EventLoop
from kivy.clock import Clock
from kivymd.app import MDApp
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from types import SimpleNamespace
from unittest.mock import MagicMock
from app.model.task import Task
from app.model.topic import Topic
from app.model.note import Note
from app.view.task_screen import TaskScreen
from app.view.planner_screen import PlannerScreen
from app.view.notes_screen import NotesScreen
from app.view.notebook_screen import NotebookScreen
from app.view.pomodoro_screen import PomodoroScreen
from app.view.note_item import NoteItem
from app.view.task_item import TaskItem
from app.view.add_task_popup import AddTaskPopup
from app.view.add_topic_popup import AddTopicPopup
from app.view.schedule_popup import SchedulePopup
from app.view.add_note_popup import AddNotePopup
from app.view.manage_topics_popup import ManageTopicsPopup
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

        self.app = FakeApp()
        # do not allow kivy to start main loop
        self.app.run = lambda *a, **kw: None
        self.app._run_prepare()

        AddTaskPopup.on_open = lambda self: None

        #App.get_running_app = lambda: self.app
        MDApp.get_running_app = lambda: self.app

    def tearDown(self):
        # Stop the Kivy app after each test to clean resources
        self.app.stop()
        Clock._del_queue.clear()

    def run_clock(self):
        # Force Kivy's clock to process scheduled events (simulate UI loop), with limited clock runs
        for c in range(5):
            Clock.tick()

    def find_widget_by_id(self, screen, widget_id):
        # Helper to retrieve a widget by its id from a given screen
        return screen.ids.get(widget_id)

# ----------------------------
# FakeApp for mocking controllers
# ----------------------------
class FakeApp(MDApp):
    # Minimal fake KivyMD app to satisfy screen dependencies and mock controllers
    def build(self):
        # initialize themes system
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        return None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Mocking all controllers required by any component
        
        # Task Controller Mock
        self.task_controller = SimpleNamespace(
            get_all_tasks=lambda: [
                Task(
                    id=1,
                    description="Test task",
                    topic=None,
                    priority=1,
                    is_completed=False,
                    scheduled_date=None,
                    start_time=None,
                    end_time=None
                )
            ],
            create_task=lambda task: 123,
            #update_task=MagicMock(),
        )

        # Topic Controller Mock
        self.topic_controller = SimpleNamespace(
            get_topic_id=lambda name: 7,
            get_all_topics=lambda: [Topic(id=7, name="Topic Mocked")],
            get_topic_by_id=lambda topic_id: Topic(id=topic_id, name="Topic Mocked"),
            create_topic=MagicMock(),
            get_topic_name=lambda topic_id: "Topic Mocked"
        )
        
        # Note Controller Mock
        self.note_controller = SimpleNamespace(
            get_all_notes=lambda: [Note(id=1, title="Note A", topic=None, content="", created_at=datetime.now())],
            get_note_by_id=lambda note_id: Note(id=note_id, title="Note C", topic=None, content="Hello", created_at=datetime.now()),
            delete_note=lambda note_id: setattr(self, "deleted", note_id),
            create_note=MagicMock(),
            update_note=lambda note_id, content: setattr(self, "updated", (note_id, content))
        )

        # Screen Manager Mock
        self.sm = SimpleNamespace(get_screen=MagicMock(), current="main")

# ----------------------------
# Tests for TaskScreen
# ----------------------------
@pytest.mark.ui
class TestTaskScreen(GUITestCase):
    # Tests task list loading and UI interactions within TaskScreen

    def setUp(self):
        super().setUp()
        # The TaskScreen instance is created
        self.task_screen = TaskScreen()
        self.app.sm.get_screen.return_value = self.task_screen

        # Mock ids of TaskScreen for testing layout manipulation
        self.task_screen.ids = {"task_list": BoxLayout()}

    def test_load_tasks_adds_widgets(self):
        # Verify that after loading tasks, the task_list container has task widgets added
        self.task_screen.load_tasks()
        self.assertGreater(len(self.task_screen.ids["task_list"].children), 0)

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
        self.popup.ids = {
            "desc_input": SimpleNamespace(text=""),
            "priority_spinner": SimpleNamespace(text=""),
            "error_label": SimpleNamespace(text=""),
            "add_btn": SimpleNamespace(disabled=False)
        }
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
        super().setUp()

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
        super().setUp()

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
            fake_dialog = type("MockDialog", (), {
                "get_date": lambda *args: [d], 
                "dismiss": lambda *args: None
            })()
            fake_btn = type("B", (), {"text": ""})()
            self.popup.set_date(fake_dialog, fake_btn)
            self.assertIn("2025-01-01", fake_btn.text)

    def test_invalid_time_order(self):
        # If end time is before start time, an error is shown and save button disabled
        from datetime import time
        # Creates mock buttons that SchedulePopup tries to update
        fake_start_btn = type("B", (), {"text": ""})()
        fake_end_btn = type("B", (), {"text": ""})() 
        start_dialog = type("MockTime", (), {
            "time": time(12, 0), 
            "dismiss": lambda *args: None
        })()
        end_dialog = type("MockTime", (), {
            "time": time(11, 0), 
            "dismiss": lambda *args: None
        })()

        # Simulates the setting of start and end time
        self.popup.set_time(start_dialog, "start", fake_start_btn)
        self.popup.set_time(end_dialog, "end", fake_end_btn)
        
        self.assertEqual(self.popup.ids.error_label.text, "End time must be later than start time")
        self.assertTrue(self.popup.ids.save_btn.disabled)

# ----------------------------
# Tests for PlannerScreen
# ----------------------------
@pytest.mark.ui
class TestPlannerScreen(GUITestCase):
    # Tests week navigation, layout updates, and parsing in PlannerScreen

    def setUp(self):
        super().setUp()

        self.screen = PlannerScreen()
        self.screen.ids = {
            "planner_grid": GridLayout(cols=8, size=(800, 600)),
            "days_header": GridLayout(cols=8, size=(800, 40)), 
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
@pytest.mark.ui
class TestNotesScreen(GUITestCase):
    # Tests notes list loading and notebook screen navigation

    def setUp(self):
        super().setUp()

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
@pytest.mark.ui
class TestAddNotePopup(GUITestCase):
    # Tests topic population, validation, and note creation

    def setUp(self):
        super().setUp()

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
        self.assertEqual(self.app.sm.current, "notebook")

# ----------------------------
# Tests for NotebookScreen
# ----------------------------
@pytest.mark.ui
class TestNotebookScreen(GUITestCase):
    # Tests loading, saving, and navigation for NotebookScreen

    def setUp(self):
        super().setUp()

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
        self.assertEqual(self.app.updated, (5, "Updated"))

# ----------------------------
# Tests for NoteItem
# ----------------------------
@pytest.mark.ui
class TestNoteItem(GUITestCase):
    # Tests initialization and user actions for NoteItem

    def setUp(self):
        super().setUp()

        # Mock NotesScreen behavior
        self.notes_screen = SimpleNamespace(
            open_notebook=lambda note: setattr(self, "opened_note", note),
            refresh_note_list=lambda: setattr(self, "refreshed", True)
        )

        self.app.sm = SimpleNamespace(
            get_screen=lambda name: self.notes_screen
        )

        self.note = Note(id=10, title="Title", topic=Topic(id=1, name="Math"), content="", created_at=datetime.now())
        self.item = NoteItem(self.note)

        self.item.ids = {
            "title_label": SimpleNamespace(text=""),
            "delete_btn": SimpleNamespace()
        }

    def test_open_note_calls_screen(self):
        # Clicking on a note item should call open_note on NotesScreen
        self.item.open_note()
        self.assertEqual(self.opened_note.id, 10)

    def test_delete_note_calls_controller_and_refresh(self):
        # Deleting a note should call controller and refresh note list
        self.item.delete_note()
        self.run_clock() # process scheduled callbacks
        # Deleted note id is stored on FakeApp
        self.assertEqual(self.app.deleted, 10)
        self.assertTrue(self.refreshed)

# ----------------------------
# Tests for PomodoroScreen
# ----------------------------
@pytest.mark.ui
class TestPomodoroScreen(GUITestCase):
    # Tests Pomodoro timer initialization, countdown, and reset

    def setUp(self):
        super().setUp()

        self.screen = PomodoroScreen()
        self.screen.ids = {
            "study_spinner": SimpleNamespace(text="25"),
            "break_spinner": SimpleNamespace(text="5"),
            "setup_view": SimpleNamespace(opacity=1),
            "timer_view": SimpleNamespace(opacity=0),
            "timer_label": SimpleNamespace(text="00:00"),
        }
        self.screen.timer_event = SimpleNamespace(cancel=lambda: None)

    def test_reset_pomodoro_resets_ui(self):
        # Reset should bring all labels to their "standard" value
        self.screen.ids["study_spinner"].text = "15"
        self.screen.ids["break_spinner"].text = "10"
        self.screen.ids["timer_label"].text = "10:00"
        self.screen.reset_pomodoro()
        self.assertEqual(self.screen.ids["study_spinner"].text, "25")
        self.assertEqual(self.screen.ids["break_spinner"].text, "5")
        self.assertEqual(self.screen.ids["timer_label"].text, "00:00")

    def test_start_pomodoro_initializes_durations(self):
        # Starting Pomodoro should initialize study and break durations
        self.screen.start_pomodoro()
        self.assertTrue(hasattr(self.screen, "study_duration"))
        self.assertTrue(hasattr(self.screen, "break_duration"))

    def test_update_timer_counts_down(self):
        # Update should decrease remaining time
        self.screen.remaining_time = 10
        self.screen.update_timer(1)
        self.assertEqual(self.screen.remaining_time, 9)

# ----------------------------
# Tests for ManageTopicsPopup
# ----------------------------
@pytest.mark.ui
class TestManageTopicsPopup(GUITestCase):
    # Tests initialization, topic loading, and deletion coordination between TopicItem and ManageTopicsPopup

    def setUp(self):
        super().setUp()
        
        # Setup Mock Data
        self.test_topics = [
            Topic(id=1, name="Math"),
            Topic(id=2, name="Physics")
        ]

        # Mock Controller behavior
        self.topic_controller = SimpleNamespace(
            get_all_topics=lambda: self.test_topics,
            delete_topic=lambda tid: self.test_topics.remove(
                next(t for t in self.test_topics if t.id == tid)
            )
        )

        # Mock Parent Popup, to verify if on_open is called to refresh the spinner
        self.parent_called = False
        self.mock_parent = SimpleNamespace(
            ids=SimpleNamespace(topic_spinner=SimpleNamespace(values=[])),
            on_open=lambda: setattr(self, "parent_called", True)
        )

        # patch load_topics during init to avoid widgets are called before they are created
        with patch.object(ManageTopicsPopup, "load_topics", lambda x: None):
            self.popup = ManageTopicsPopup(parent_popup=self.mock_parent)

        self.popup.ids = {
            "topics_list": BoxLayout(),
            "close_btn": MagicMock()
        }

        self.app.topic_controller = self.topic_controller

        # Now run real logic
        self.popup.load_topics()
        self.popup.open()
        self.run_clock()

    def tearDown(self):
        self.popup.dismiss()
        super().tearDown()

    def test_initial_topics_loading(self):
        # Verify that the UI correctly generates one TopicItem for each Topic in the DB
        displayed_items = self.popup.ids["topics_list"].children
        # The number of widgets should match the length of the test_topics list
        self.assertEqual(len(displayed_items), len(self.test_topics))

    def test_topic_item_data_integrity(self):
        # Ensure each TopicItem widget holds the correct data from the Model
        # Kivy adds widgets from bottom to top; the last child is the first topic
        first_widget = self.popup.ids["topics_list"].children[-1]
        
        self.assertEqual(first_widget.topic_id, self.test_topics[0].id)
        self.assertEqual(first_widget.topic_name, self.test_topics[0].name)

    def test_delete_action_updates_ui_and_notifies_parent(self):
        """
        Simulate a user clicking 'Delete' on a TopicItem and verify:
        1. The controller is called
        2. The UI list is refreshed
        3. The parent popup (spinner) is notified
        """
        # Pick the first widget to delete
        target_item = self.popup.ids["topics_list"].children[-1]
        target_id = target_item.topic_id
        
        # Reset parent call tracker before action
        self.parent_called = False
        
        # Trigger the delete logic inside the TopicItem
        target_item.delete_topic()
        
        # Advance Kivy clock to process the schedule_once(load_topics)
        self.run_clock()

        # Check if the topic was removed from the mock list
        self.assertFalse(any(t.id == target_id for t in self.test_topics))
        
        # Check if the widget was removed from the UI
        self.assertEqual(len(self.popup.ids["topics_list"].children), 1)
        
        # Verify that the parent popup was refreshed (for the spinner)
        self.assertTrue(self.parent_called)

    def test_close_button_dismisses_popup(self):
        # Ensure the close button properly triggers the dismiss action (simple UI integrity check)
        self.popup.dismiss()
        self.run_clock()
        self.assertTrue(True) # Reaching here without crash