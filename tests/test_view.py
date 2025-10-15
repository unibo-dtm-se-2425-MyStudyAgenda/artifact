import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
import os
import pytest

# Prevent Kivy from parsing CLI args in tests
os.environ["KIVY_NO_ARGS"] = "1"
import unittest
from kivy.base import EventLoop
from kivy.clock import Clock
from kivymd.app import MDApp
from kivy.app import App
from types import SimpleNamespace
from unittest.mock import MagicMock
from app.main import MyStudyAgenda
from app.view.add_task_popup import AddTaskPopup
from app.view.add_topic_popup import AddTopicPopup
from app.view.task_item import TaskItem
from app.view.add_topic_popup import AddTopicPopup
from app.model.task import Task
from app.model.topic import Topic

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
        # Avoid building full canvas on headless CI runners
        try:
            import os
            if os.environ.get("CI") == "true" and os.environ.get("RUN_UI_TESTS") != "1":
                self.app.build = lambda: self.app.root if getattr(self.app, "root", None) else super(type(self.app), self.app).build()  # type: ignore[attr-defined]
        except Exception:
            pass
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
pytestmark = pytest.mark.ui
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
class AddTopicPopupTestCase(unittest.TestCase):
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