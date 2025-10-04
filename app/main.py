from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

class MyStudyAgenda(App):
    def build(self):
        self.sm = ScreenManager()
        return self.sm

if __name__ == "__main__":
    MyStudyAgenda().run()
