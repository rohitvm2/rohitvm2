from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from database.db import connect_db
from kivy.properties import StringProperty, NumericProperty, ListProperty  # Added ListProperty


class TestScreen(Screen):
    current_category = StringProperty("General")
    time_left = NumericProperty(30)
    # This will store our session data for the ReviewScreen
    review_data = ListProperty([])

    def on_enter(self):
        # 1. Reset Everything
        self.ids.score_label.text = "Score: 0"
        self.ids.feedback.text = ""
        self.score = 0
        self.q_index = 0
        self.time_left = 30
        self.review_data = []  # Clear previous test data

        self.loaded = False
        Clock.unschedule(self.update_timer)

        # 4. Fetch questions (keeping your existing SQL logic)
        conn = connect_db()
        cursor = conn.cursor()
        query = "SELECT * FROM questions WHERE category = ?"
        cursor.execute(query, (self.current_category,))
        rows = cursor.fetchall()
        conn.close()

        all_questions = []
        for row in rows:
            all_questions.append({
                "question": row[1],
                "option1": row[2],
                "option2": row[3],
                "option3": row[4],
                "option4": row[5],
                "answer": row[6]
            })

        if not all_questions:
            self.ids.question.text = f"No questions found for {self.current_category}"
            Clock.schedule_once(lambda dt: setattr(self.manager, 'current', 'category'), 2)
            return

        import random
        num_to_select = min(5, len(all_questions))
        self.questions = random.sample(all_questions, num_to_select)

        self.ids.question.text = "Loading questions..."
        Clock.schedule_once(lambda dt: self.load_question(), 0.2)
        Clock.schedule_interval(self.update_timer, 1)

    def load_question(self):
        self.answered = False
        self.ids.feedback.text = ""
        self.time_left = 30
        self.ids.timer.text = f"Time: {self.time_left}"

        Clock.unschedule(self.update_timer)
        Clock.schedule_interval(self.update_timer, 1)

        q = self.questions[self.q_index]
        self.ids.question.text = q["question"]
        self.ids.opt1.text = q["option1"]
        self.ids.opt2.text = q["option2"]
        self.ids.opt3.text = q["option3"]
        self.ids.opt4.text = q["option4"]

        total = len(self.questions)
        self.ids.qno.text = f"Question {self.q_index + 1}/{total}"
        self.ids.progress.max = total
        self.ids.progress.value = self.q_index + 1

        for btn in [self.ids.opt1, self.ids.opt2, self.ids.opt3, self.ids.opt4]:
            btn.background_color = (0.2, 0.6, 1, 1)
            btn.disabled = False

    def check_answer(self, selected):
        Clock.unschedule(self.update_timer)
        if hasattr(self, "answered") and self.answered:
            return
        self.answered = True

        current_q = self.questions[self.q_index]
        correct = current_q["answer"]

        # TRACK DATA FOR REVIEW SCREEN
        self.review_data.append({
            "q": current_q["question"],
            "correct": correct,
            "selected": selected
        })

        self.ids.opt1.disabled = True
        self.ids.opt2.disabled = True
        self.ids.opt3.disabled = True
        self.ids.opt4.disabled = True

        if selected == correct:
            self.score += 1
            self.ids.feedback.text = "✅ Correct!"
        else:
            self.ids.feedback.text = f"❌ Wrong! Correct: {correct}"

        Clock.schedule_once(self.next_question, 1.2)

        for btn in [self.ids.opt1, self.ids.opt2, self.ids.opt3, self.ids.opt4]:
            if btn.text == correct:
                btn.background_color = (0, 1, 0, 1)
            elif btn.text == selected:
                btn.background_color = (1, 0, 0, 1)

        self.ids.score_label.text = f"Score: {self.score}"

    def update_timer(self, dt):
        if self.q_index >= len(self.questions):
            Clock.unschedule(self.update_timer)
            return

        self.time_left -= 1
        self.ids.timer.text = f"Time: {self.time_left}"

        if self.time_left <= 0:
            if hasattr(self, "answered") and self.answered:
                return

            # Treat timeout as a wrong answer for review
            current_q = self.questions[self.q_index]
            self.review_data.append({
                "q": current_q["question"],
                "correct": current_q["answer"],
                "selected": "Timed Out"
            })

            self.answered = True
            Clock.unschedule(self.update_timer)
            self.ids.feedback.text = "⏰ Time Up!"
            Clock.schedule_once(self.next_question, 1)

    def next_question(self, dt):
        self.q_index += 1

        if self.q_index < len(self.questions):
            self.load_question()
        else:
            self.ids.feedback.text = "🎉 Test Completed!"

            def go_to_review(dt):
                # Pass data to ReviewScreen before navigating
                review_screen = self.manager.get_screen("review")
                review_screen.results_data = self.review_data
                self.manager.current = "review"

                # Also trigger the ResultScreen save in the background
                result_screen = self.manager.get_screen("result")
                result_screen.show_result(self.score)

            Clock.schedule_once(go_to_review, 0.5)

    def skip_question(self):
        current_q = self.questions[self.q_index]
        self.review_data.append({
            "q": current_q["question"],
            "correct": current_q["answer"],
            "selected": "Skipped"
        })

        self.ids.feedback.text = "⏭ Skipped"
        Clock.schedule_once(self.next_question, 0.5)