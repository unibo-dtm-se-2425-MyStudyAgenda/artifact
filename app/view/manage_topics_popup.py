from kivy.uix.popup import Popup
from kivy.app import App
from app.view.topic_item import TopicItem

class ManageTopicsPopup(Popup):
    def __init__(self, parent_popup=None, **kwargs):
        super().__init__(**kwargs)
        # Save the reference to the parent popup (either AddTask o AddNote)
        self.parent_popup = parent_popup 
        self.load_topics()

    def load_topics(self):
        # Load all topics from the controller and display them in the UI
        app = App.get_running_app()
        self.ids.topics_list.clear_widgets()
        topics = app.topic_controller.get_all_topics()
        
        for topic in topics:
            topic_item = TopicItem(topic, manage_popup=self)
            self.ids.topics_list.add_widget(topic_item)

        # Refresh the parent popup’s topic spinner instantly
        if self.parent_popup and hasattr(self.parent_popup, "on_open"):
            self.parent_popup.on_open()
        