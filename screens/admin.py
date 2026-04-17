from kivy.uix.screenmanager import Screen
from database.db import connect_db

class AdminScreen(Screen):

    def add_question(self):
        q = self.ids.q.text
        o1 = self.ids.o1.text
        o2 = self.ids.o2.text
        o3 = self.ids.o3.text
        o4 = self.ids.o4.text
        ans = self.ids.ans.text

        # Validation
        if not q or not o1 or not o2 or not o3 or not o4 or not ans:
            self.ids.msg.text = "⚠ Fill all fields"
            return

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO questions (question, option1, option2, option3, option4, answer)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (q, o1, o2, o3, o4, ans))

        conn.commit()
        conn.close()

        self.ids.msg.text = "✅ Question added"

        # Clear fields
        self.ids.q.text = ""
        self.ids.o1.text = ""
        self.ids.o2.text = ""
        self.ids.o3.text = ""
        self.ids.o4.text = ""
        self.ids.ans.text = ""

        # Clear previous display
        self.ids.display_area.text = ""

    def show_questions(self):
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM questions")
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            self.ids.display_area.text = "No questions found"
            return

        output = ""
        for i, row in enumerate(rows, 1):
            output += (
                f"{i}. {row[1]}\n"
                f"   A) {row[2]}\n"
                f"   B) {row[3]}\n"
                f"   C) {row[4]}\n"
                f"   D) {row[5]}\n"
                f"   ✔ Answer: {row[6]}\n\n"
            )

        self.ids.display_area.text = output

    def delete_all(self):
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM questions")
        conn.commit()
        conn.close()

        self.ids.display_area.text = ""
        self.ids.msg.text = "🗑 All questions deleted"