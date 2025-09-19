from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.properties import StringProperty
from kivy.clock import Clock

class NoteItem(BoxLayout):
    # UI properties bound to note data
    title = StringProperty("")
    topic = StringProperty("")
    created_at = StringProperty("")

    def __init__(self, note, **kwargs):
        # Initialize NoteItem with note data
        app = App.get_running_app()
        super().__init__(**kwargs)
        self.note = note
        self.note_id = str(getattr(note, "id", getattr(note, "note_id", 0)) or 0)
        self.title = note.title or ""
        self.topic = app.topic_controller.get_topic_name(note.topic.id) if note.topic else ""
        self.created_at = note.created_at.strftime("%Y-%m-%d")

    def open_note(self):
        # Open the notebook screen for this note
        app = App.get_running_app()
        notes_screen = app.sm.get_screen("notes")
        notes_screen.open_notebook(self.note)

    def delete_note(self):
        # Delete this note and refresh the list
        app = App.get_running_app()
        note_screen = app.sm.get_screen("notes")
        try:
            app.note_controller.delete_note(int(self.note_id))
        finally:
            Clock.schedule_once(lambda dt: note_screen.refresh_note_list(), 0.0)