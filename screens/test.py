from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from database.db import connect_db

class TestScreen(Screen):

    def on_enter(self):
        self.ids.score_label.text = "Score: 0"

        # FIX: stop any previous timer before starting new one
        Clock.unschedule(self.update_timer)

        if hasattr(self, "loaded") and self.loaded:
            return
        self.loaded = True

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM questions")
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

        self.ids.question.text = "Loading questions..."
        print("Loaded questions:", all_questions)

        if len(all_questions) == 0:
            self.ids.question.text = "No questions available"
            return

        import random
        self.questions = random.sample(all_questions, min(5, len(all_questions)))

        self.q_index = 0
        self.score = 0

        # Load first question
        Clock.schedule_once(lambda dt: self.load_question(), 0.1)

        self.time_left = 30
        Clock.schedule_interval(self.update_timer, 1)

    def load_question(self):
        self.answered = False
        self.ids.feedback.text = ""

        # FIX: reset timer every question
        self.time_left = 30
        self.ids.timer.text = f"Time: {self.time_left}"

        # FIX: restart timer cleanly
        Clock.unschedule(self.update_timer)
        Clock.schedule_interval(self.update_timer, 1)

        q = self.questions[self.q_index]

        self.ids.question.opacity = 0
        Clock.schedule_once(lambda dt: setattr(self.ids.question, 'opacity', 1), 0.2)

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

    def update_timer(self, dt):
        if self.q_index >= len(self.questions):
            Clock.unschedule(self.update_timer)
            return

        self.time_left -= 1
        self.ids.timer.text = f"Time: {self.time_left}"

        if self.time_left <= 0:
            if hasattr(self, "answered") and self.answered:
                return
            self.answered = True

            Clock.unschedule(self.update_timer)
            self.ids.feedback.text = "⏰ Time Up!"
            Clock.schedule_once(self.next_question, 1)

    def check_answer(self, selected):
        Clock.unschedule(self.update_timer)
        if hasattr(self, "answered") and self.answered:
            return
        self.answered = True
        correct = self.questions[self.q_index]["answer"]

        # Disable buttons temporarily
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

    def on_leave(self):
        Clock.unschedule(self.update_timer)
        self.loaded = False

    def next_question(self, dt):
        self.q_index += 1

        if self.q_index < len(self.questions):
            self.ids.opt1.disabled = False
            self.ids.opt2.disabled = False
            self.ids.opt3.disabled = False
            self.ids.opt4.disabled = False

            self.load_question()
        else:
            print("Final Score:", self.score)
            self.ids.feedback.text = "🎉 Test Completed!"

            def go_to_result(dt):
                self.manager.current = "result"

                def update_result(dt2):
                    result_screen = self.manager.get_screen("result")
                    result_screen.show_result(self.score)

                Clock.schedule_once(update_result, 0.1)

            Clock.schedule_once(go_to_result, 0.5)

    def skip_question(self):
        # FIX: reset timer on skip
        self.time_left = 30
        self.ids.timer.text = f"Time: {self.time_left}"

        self.ids.feedback.text = "⏭ Skipped"
        Clock.schedule_once(self.next_question, 0.5)