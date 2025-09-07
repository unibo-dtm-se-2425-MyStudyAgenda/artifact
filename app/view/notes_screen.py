from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.app import App
from model.note import Note
from model.topic import Topic

class NotesScreen(Screen):
    def on_enter(self):
        self.load_notes()

    def load_notes(self):
        notes_list = self.ids.notes_list
        notes_list.clear_widgets()

        app = App.get_running_app()
        notes = app.note_controller.get_all_notes()

        for note in notes:
            card = BoxLayout(orientation="vertical", size_hint_y=None, height=80, padding=5)
            card.add_widget(Label(text=f"Title: {note.title}", halign="left"))
            topic_name = app.topic_controller.get_topic_name(note.topic.id) if note.topic else "No topic"
            card.add_widget(Label(text=f"Topic: {topic_name}", halign="left"))
            created_str = note.created_at.strftime("%Y-%m-%d")
            card.add_widget(Label(text=f"Created: {created_str}", halign="left"))

            card.bind(on_touch_down=lambda instance, touch, n=note: 
                      self.open_notebook(n) if instance.collide_point(*touch.pos) else None)

            notes_list.add_widget(card)

    def open_new_note_popup(self):
        popup = AddNotePopup()
        popup.open()
        
    def open_notebook(self, note):
        screen = self.manager.get_screen("notebook")
        screen.open_note(note.id)
        self.manager.current = "notebook"

class AddNotePopup(Popup):
    def on_open(self):
        # topic uploading in the spinner
        app = App.get_running_app()
        topics = app.topic_controller.get_all_topics()
        self.ids.topic_spinner.values = [t.name for t in topics]

    def add_new_topic(self):
        from kivy.uix.textinput import TextInput
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.button import Button

        content = BoxLayout(orientation="vertical", spacing=10, padding=10)
        input_field = TextInput(hint_text="New topic name", multiline=False)
        btn_layout = BoxLayout(size_hint_y=None, height="44dp", spacing=10)
        btn_cancel = Button(text="Cancel")
        btn_add = Button(text="Add")

        btn_layout.add_widget(btn_cancel)
        btn_layout.add_widget(btn_add)

        content.add_widget(input_field)
        content.add_widget(btn_layout)

        popup = Popup(title="Add Topic", content=content, size_hint=(0.8, 0.4), auto_dismiss=False)

        btn_cancel.bind(on_release=popup.dismiss)

        def save_topic(_):
            new_topic = input_field.text.strip()
            if new_topic:
                app = App.get_running_app()
                app.topic_controller.create_topic(new_topic)
                self.on_open()
                popup.dismiss()

        btn_add.bind(on_release=save_topic)
        popup.open()

    def create_note(self):
        app = App.get_running_app()
        title = self.ids.title_input.text.strip()
        topic_name = self.ids.topic_spinner.text
        topic_id = None
        if topic_name != "Select topic":
            topic_id = app.topic_controller.get_topic_id(topic_name)

        if title:
            note = Note(
                id=None,
                title=title,
                topic=Topic(id=topic_id) if topic_id else None,
                content=""
            )
            app.note_controller.create_note(note)

            self.dismiss()

            # takes the last note created and opens it
            last_note = app.note_controller.get_all_notes()[-1]
            notebook = app.root.get_screen("notebook")
            notebook.open_note(last_note.id)
            app.root.current = "notebook"

class NotebookScreen(Screen):
    current_note_id = None

    def open_note(self, note_id):
        self.current_note_id = note_id
        app = App.get_running_app()
        note = app.note_controller.get_note_by_id(note_id)
        self.ids.content_input.text = note.content

    def save_note(self):
        app = App.get_running_app()
        content = self.ids.content_input.text
        if self.current_note_id:
            app.note_controller.update_note(self.current_note_id, content)

    def go_back(self):
        self.manager.current = "notes"
