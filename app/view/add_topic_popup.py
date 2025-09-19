from kivy.uix.popup import Popup
from kivy.app import App

class AddTopicPopup(Popup):
    def __init__(self, parent_popup=None, **kwargs):
        # Optional reference to the popup that opened this one
        super().__init__(**kwargs)
        self.parent_popup = parent_popup

    def save_topic(self):
        # Create a new topic from the user input
        app = App.get_running_app()
        new_topic = self.ids.topic_input.text.strip()
        if new_topic:
            app.topic_controller.create_topic(new_topic)

            # Refresh the parent popup’s topic spinner instantly
            if self.parent_popup and hasattr(self.parent_popup, "on_open"):
                self.parent_popup.on_open()

            # Close the popup after saving
            self.dismiss()