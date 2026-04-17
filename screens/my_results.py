from kivy.uix.screenmanager import Screen
from kivy.app import App
from database.db import connect_db

class MyResultsScreen(Screen):

    def on_enter(self):
        user = App.get_running_app().current_user

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT score FROM results WHERE username=?",
            (user,)
        )

        data = cursor.fetchall()
        conn.close()

        text = "My Results\n\n"

        for i, row in enumerate(data, 1):
            text += f"Test {i}: {row[0]}\n"

        self.ids.result_list.text = text