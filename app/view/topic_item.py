from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.app import App
from kivy.clock import Clock

class TopicItem(BoxLayout):
    topic_id = None
    topic_name = StringProperty("")
    
    def __init__(self, topic, manage_popup, **kwargs):
        self._initializing = True
        super().__init__(**kwargs)
        self.topic_id = topic.id
        self.topic_name = topic.name
        self.manage_popup = manage_popup

    def delete_topic(self):
        app = App.get_running_app()
        try:
            app.topic_controller.delete_topic(int(self.topic_id))
            Clock.schedule_once(lambda dt: self.manage_popup.load_topics(), 0.0)
        except Exception as e:
            print(f"Error during deletion: {e}")