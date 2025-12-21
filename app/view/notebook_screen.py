from kivy.uix.screenmanager import Screen
from kivy.app import App

class NotebookScreen(Screen):
    current_note_id = None

    def open_note(self, note_id):
        # Load a note by ID and show its content
        self.current_note_id = note_id
        app = App.get_running_app()
        note = app.note_controller.get_note_by_id(note_id)
        self.ids.content_input.text = note.content

    def save_note(self):
        # Save modifications to the current note
        app = App.get_running_app()
        content = self.ids.content_input.text
        if self.current_note_id:
            app.note_controller.update_note(self.current_note_id, content)

    def go_back(self):
        # Return to the notes list screen without saving any modifications (if the 'save' button wasn't pressed beforehand)
        self.manager.current = "notes"