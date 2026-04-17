from kivy.uix.screenmanager import Screen
from database.db import connect_db

class LeaderboardScreen(Screen):

    def on_enter(self):
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT username, MAX(score) as best_score
            FROM results
            GROUP BY username
            ORDER BY best_score DESC
            LIMIT 10
        """)

        data = cursor.fetchall()
        conn.close()

        text = "Leaderboard\n\n"
        rank = 1

        for row in data:
            text += f"{rank}. {row[0]} - {row[1]}\n"
            rank += 1

        self.ids.leaderboard.text = text