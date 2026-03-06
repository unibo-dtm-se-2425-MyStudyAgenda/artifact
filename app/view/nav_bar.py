from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.clock import Clock

class NavigationBar(BoxLayout):
    screen_manager = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # updates buttons color every 0.1 seconds
        Clock.schedule_interval(self.update_buttons_color, 0.1)

    def update_buttons_color(self, dt):
        if not self.screen_manager:
            return
        for child in self.children:
            if hasattr(child, 'screen_name'):
                if child.screen_manager.current == child.screen_name:
                    child.background_color = (1,0.8,0.2,1)
                else:
                    child.background_color = (1,1,0.3,0.5)