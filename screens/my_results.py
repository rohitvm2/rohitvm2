from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.app import App
from database.db import connect_db


class MyResultsScreen(Screen):

    def on_enter(self):
        # 1. Clear previous entries to prevent duplication
        self.ids.container.clear_widgets()

        # 2. Get the current logged-in user
        user = App.get_running_app().current_user

        conn = connect_db()
        cursor = conn.cursor()

        # 3. Fetch category, score, and date
        # We sort by date DESC so the newest results appear at the top
        cursor.execute(
            "SELECT category, score, date FROM results WHERE username=? ORDER BY id DESC",
            (user,)
        )

        data = cursor.fetchall()
        conn.close()

        if not data:
            self.ids.container.add_widget(Label(text="No test history found.", color=(0.5, 0.5, 0.5, 1)))
            return

        # 4. Create a structured row for every result
        for row in data:
            category = row[0] if row[0] else "General"
            score = row[1]
            # Format date to show only YYYY-MM-DD
            raw_date = row[2] if row[2] else "N/A"
            date_display = raw_date.split(" ")[0]

            # Create a horizontal layout for the row
            row_box = BoxLayout(size_hint_y=None, height=45, padding=[10, 0])

            # Column 1: Category
            row_box.add_widget(Label(text=str(category), size_hint_x=0.4, halign='left', text_size=(None, None)))

            # Column 2: Score (Color coded: Green for pass, White for fail)
            score_color = (0.2, 0.8, 0.4, 1) if int(score) >= 3 else (1, 1, 1, 1)
            row_box.add_widget(Label(text=str(score), size_hint_x=0.2, bold=True, color=score_color))

            # Column 3: Date
            row_box.add_widget(Label(text=date_display, size_hint_x=0.4, font_size='12sp', color=(0.7, 0.7, 0.7, 1)))

            # Add the row to the ScrollView container
            self.ids.container.add_widget(row_box)