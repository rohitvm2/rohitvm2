from kivy.uix.screenmanager import Screen
from kivy.app import App
from database.db import connect_db

class ResultScreen(Screen):
    def show_result(self, score):
        user = App.get_running_app().current_user

        # SHOW RESULT FIRST (important)
        self.ids.result.text = f"Score: {score}"
        if score >= 4:
            self.ids.message.text = "Excellent!"
        elif score >= 2:
            self.ids.message.text = "Good Job!"
        else:
            self.ids.message.text = "Keep Practicing!"

        try:
            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO results (username, score) VALUES (?, ?)",
                (user, score)
            )

            conn.commit()
            conn.close()

        except Exception as e:
            print("DB Error:", e)

    def on_enter(self):
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("SELECT username, score FROM results ORDER BY score DESC LIMIT 5")
        rows = cursor.fetchall()
        conn.close()

        text = "🏆 Top Scores:\n"
        for r in rows:
            text += f"{r[0]} - {r[1]}\n"

        self.ids.history.text = text