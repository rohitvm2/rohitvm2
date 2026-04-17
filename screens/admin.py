from kivy.uix.screenmanager import Screen
from database.db import connect_db


class AdminScreen(Screen):

    def add_question(self):
        # Grabbing all fields including the new 'category' ID
        q = self.ids.q.text.strip()
        cat = self.ids.category.text.strip()  # New field for subject
        o1 = self.ids.o1.text.strip()
        o2 = self.ids.o2.text.strip()
        o3 = self.ids.o3.text.strip()
        o4 = self.ids.o4.text.strip()
        ans = self.ids.ans.text.strip()

        # Validation: Ensure nothing is empty
        if not all([q, cat, o1, o2, o3, o4, ans]):
            self.ids.msg.text = "⚠ Fill all fields, including Category"
            return

        conn = connect_db()
        cursor = conn.cursor()

        try:
            # UPDATED SQL: Added 'category' to the insert statement
            cursor.execute("""
            INSERT INTO questions (question, option1, option2, option3, option4, answer, category)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (q, o1, o2, o3, o4, ans, cat))

            conn.commit()
            self.ids.msg.text = f"✅ Added to {cat} category"

            # Clear all input fields
            for field in ['q', 'category', 'o1', 'o2', 'o3', 'o4', 'ans']:
                self.ids[field].text = ""

            # Reset display area
            self.ids.display_area.text = ""

        except Exception as e:
            self.ids.msg.text = f"❌ DB Error: {str(e)}"
        finally:
            conn.close()

    def show_questions(self):
        conn = connect_db()
        cursor = conn.cursor()

        # Fetch everything, including the category
        cursor.execute("SELECT * FROM questions")
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            self.ids.display_area.text = "No questions found in database."
            return

        output = ""
        for i, row in enumerate(rows, 1):
            # Mapping based on: ID(0), Q(1), O1(2), O2(3), O3(4), O4(5), Ans(6), Cat(7)
            output += (
                f"{i}. [{row[7]}] {row[1]}\n"  # Shows Category in brackets
                f"   A) {row[2]}  B) {row[3]}\n"
                f"   C) {row[4]}  D) {row[5]}\n"
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
        self.ids.msg.text = "🗑 All questions wiped from DB"