from kivy.uix.screenmanager import Screen

class ProfileScreen(Screen):
    user = ""
    email = ""

    def on_pre_enter(self):
        self.ids.username.text = self.user
        self.ids.email.text = self.email