from kivy.uix.popup import Popup
from kivy.app import App
from app.model.note import Note
from app.model.topic import Topic
from app.view.add_topic_popup import AddTopicPopup

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
        topic_id = None # Topic is optional

        # Check if title is empty: if so, an error is displayed
        if not title:
            self.ids.error_label.text = "Title cannot be empty"
            return
        else:
            self.ids.error_label.text = ""  # clear error if valid
        
        if topic_name != "Select topic":
            topic_id = app.topic_controller.get_topic_id(topic_name)

        note = Note(
            id=None,
            title=title,
            topic=app.topic_controller.get_topic_by_id(topic_id) if topic_id else None,
            content=""
        )
        note_id = app.note_controller.create_note(note)
        print(str(note))

        self.dismiss()

        notebook = app.root.get_screen("notebook")
        notebook.open_note(note_id)
        app.root.current = "notebook"
