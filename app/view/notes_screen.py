from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.app import App
from model.note import Note
from model.topic import Topic
from view.add_topic_popup import AddTopicPopup
from view.note_item import NoteItem

class NotesScreen(Screen):
    def on_enter(self):
        # Reload notes every time the screen is entered
        self.load_notes()

    def load_notes(self):
        # Load all notes and render them as NoteItem widgets
        app = App.get_running_app()
        self.ids.notes_list.clear_widgets()
        notes = app.note_controller.get_all_notes()
        for note in notes:
            note_item = NoteItem(note)
            self.ids.notes_list.add_widget(note_item)

    def open_new_note_popup(self):
        # Open popup for creating a new note
        popup = AddNotePopup()
        popup.open()
        
    def open_notebook(self, note):
        # Open the notebook screen of the selected note
        screen = self.manager.get_screen("notebook")
        screen.open_note(note.id)
        self.manager.current = "notebook"
    
    def refresh_note_list(self):
        # Reload the notes list (used after add/delete operations)
        app = App.get_running_app()
        notes_screen = app.sm.get_screen("notes")
        notes_screen.load_notes()

class AddNotePopup(Popup):
    def on_open(self):
        # Populate topic spinner with all available topics
        app = App.get_running_app()
        topics = app.topic_controller.get_all_topics()
        self.ids.topic_spinner.values = [t.name for t in topics]

    def add_new_topic(self):
        # Open popup for adding a new topic
        popup = AddTopicPopup(parent_popup=self)
        popup.open()

    def create_note(self):
        # Create a new note and open it in the notebook screen
        app = App.get_running_app()
        title = self.ids.title_input.text.strip()
        topic_name = self.ids.topic_spinner.text
        topic_id = None

        # Check if title is empty: if so, an error is displayed
        if not title:
            self.ids.error_label.text = "Title cannot be empty"
            return
        else:
            self.ids.error_label.text = ""  # clear error if valid

        # Topic is optional
        topic_id = None
        if topic_id and topic_name != "Select topic":
            topic_id = app.topic_controller.get_topic_id(topic_name)

        note = Note(
            id=None,
            title=title,
            topic=Topic(id=topic_id) if topic_id else None,
            content=""
        )
        note_id = app.note_controller.create_note(note)

        self.dismiss()

        notebook = app.root.get_screen("notebook")
        notebook.open_note(note_id)
        app.root.current = "notebook"


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
        # Return to the notes list screen
        self.manager.current = "notes"