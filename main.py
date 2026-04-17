from database.db import create_tables, create_admin
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from screens.login import LoginScreen
from screens.dashboard import DashboardScreen
from screens.test import TestScreen
from screens.result import ResultScreen
from screens.admin import AdminScreen
from screens.leaderboard import LeaderboardScreen
from screens.my_results import MyResultsScreen
from kivy.properties import StringProperty
from screens.profile import ProfileScreen

class MockTestApp(App):
    current_user = StringProperty("")
    def build(self):
        from kivy.core.window import Window
        Window.clearcolor = (0.1, 0.1, 0.1, 1)  # dark background

        create_tables()
        create_admin()

        Builder.load_file("kv/login.kv")
        Builder.load_file("kv/profile.kv")
        Builder.load_file("kv/dashboard.kv")
        Builder.load_file("kv/test.kv")
        Builder.load_file("kv/result.kv")
        Builder.load_file("kv/admin.kv")
        Builder.load_file("kv/leaderboard.kv")
        Builder.load_file("kv/my_results.kv")

        sm = ScreenManager()
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(ProfileScreen(name="profile"))
        sm.add_widget(DashboardScreen(name="dashboard"))
        sm.add_widget(TestScreen(name="test"))
        sm.add_widget(ResultScreen(name="result"))
        sm.add_widget(AdminScreen(name="admin"))
        sm.add_widget(LeaderboardScreen(name="leaderboard"))
        sm.add_widget(MyResultsScreen(name="my_results"))
        return sm

if __name__ == "__main__":
    MockTestApp().run()