from kivy.uix.screenmanager import Screen

class ProfileScreen(Screen):
    user = ""

    def on_pre_enter(self):
        self.ids.username.text = self.user