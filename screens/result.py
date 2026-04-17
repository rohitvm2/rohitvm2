from kivy.uix.screenmanager import Screen
from kivy.app import App
from database.db import connect_db


class ResultScreen(Screen):
    def show_result(self, score):
        app = App.get_running_app()
        user = app.current_user

        # We need to know WHICH category was just completed
        test_screen = self.manager.get_screen("test")
        category = test_screen.current_category

        # Update UI text
        self.ids.result.text = f"Category: {category}\nScore: {score}"

        if score >= 4:
            self.ids.message.text = "🏆 Excellent!"
        elif score >= 2:
            self.ids.message.text = "👍 Good Job!"
        else:
            self.ids.message.text = "📚 Keep Practicing!"

        try:
            conn = connect_db()
            cursor = conn.cursor()

            # UPDATED SQL: Now saving the category name as well
            cursor.execute(
                "INSERT INTO results (username, category, score) VALUES (?, ?, ?)",
                (user, category, score)
            )

            conn.commit()
            conn.close()

        except Exception as e:
            print("DB Error during result save:", e)

    def on_enter(self):
        # We can show the user's personal best for the current category
        test_screen = self.manager.get_screen("test")
        current_cat = test_screen.current_category

        conn = connect_db()
        cursor = conn.cursor()

        # SQL: Fetch top scores specifically for the category the user just took
        cursor.execute("""
            SELECT username, score 
            FROM results 
            WHERE category = ? 
            ORDER BY score DESC 
            LIMIT 5
        """, (current_cat,))

        rows = cursor.fetchall()
        conn.close()

        text = f"🏆 Top in {current_cat}:\n"
        for r in rows:
            text += f"{r[0]} - {r[1]}\n"

        self.ids.history.text = text