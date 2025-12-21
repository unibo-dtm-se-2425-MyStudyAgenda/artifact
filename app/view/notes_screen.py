from kivy.uix.screenmanager import Screen
from kivy.app import App
from app.view.note_item import NoteItem
from app.view.add_note_popup import AddNotePopup

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

