from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from database.db import connect_db


class LeaderboardScreen(Screen):

    def on_enter(self):
        # 1. Clear the previous list so it doesn't duplicate every time you open the screen
        self.ids.leaderboard_list.clear_widgets()

        conn = connect_db()
        cursor = conn.cursor()

        # 2. Optimized SQL: Gets the best score for each user
        cursor.execute("""
            SELECT username, MAX(score) as best_score
            FROM results
            GROUP BY username
            ORDER BY best_score DESC
            LIMIT 10
        """)

        data = cursor.fetchall()
        conn.close()

        # 3. Build the rows dynamically
        for rank, row in enumerate(data, 1):
            username = row[0]
            score = row[1]

            # Define colors for the Podium (Gold, Silver, Bronze)
            if rank == 1:
                rank_color = (1, 0.84, 0, 1)  # Gold
            elif rank == 2:
                rank_color = (0.75, 0.75, 0.75, 1)  # Silver
            elif rank == 3:
                rank_color = (0.8, 0.5, 0.2, 1)  # Bronze
            else:
                rank_color = (1, 1, 1, 1)  # White for others

            # Create a horizontal row for each user
            row_layout = BoxLayout(size_hint_y=None, height=45, padding=[10, 0], spacing=10)

            # Rank Label
            row_layout.add_widget(Label(
                text=str(rank),
                color=rank_color,
                bold=(rank <= 3),
                size_hint_x=0.2
            ))

            # Username Label
            row_layout.add_widget(Label(
                text=username,
                size_hint_x=0.5,
                halign='left',
                text_size=(200, None)  # Ensures text alignment
            ))

            # Score Label
            row_layout.add_widget(Label(
                text=str(score),
                size_hint_x=0.3,
                bold=True
            ))

            # Add this row to the ScrollView container in your .kv file
            self.ids.leaderboard_list.add_widget(row_layout)