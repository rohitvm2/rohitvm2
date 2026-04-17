from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.properties import ListProperty


class ReviewScreen(Screen):
    # This will hold the questions and answers from the test
    # Format: [{"q": "...", "correct": "...", "selected": "..."}, ...]
    results_data = ListProperty([])

    def on_enter(self):
        self.ids.review_container.clear_widgets()

        if not self.results_data:
            self.ids.review_container.add_widget(Label(text="No data to review"))
            return

        for i, item in enumerate(self.results_data, 1):
            is_correct = item['selected'] == item['correct']

            # Create a Card for each question
            card = BoxLayout(orientation='vertical', size_hint_y=None, height=140, padding=15, spacing=5)

            # Card Background Styling
            with card.canvas.before:
                from kivy.graphics import Color, RoundedRectangle
                Color(rgba=(0.15, 0.15, 0.15, 1))
                self.rect = RoundedRectangle(pos=card.pos, size=card.size, radius=[10])
            card.bind(pos=self._update_rect, size=self._update_rect)

            # Question Text
            card.add_widget(Label(text=f"{i}. {item['q']}", bold=True, halign='left', text_size=(None, None)))

            # Selected Answer (Red if wrong, Green if right)
            color = (0.2, 0.8, 0.4, 1) if is_correct else (1, 0.3, 0.3, 1)
            card.add_widget(
                Label(text=f"Your Answer: {item['selected']}", color=color, halign='left', text_size=(None, None)))

            # Correct Answer (Always show for learning)
            if not is_correct:
                card.add_widget(Label(text=f"Correct Answer: {item['correct']}", color=(0.2, 0.6, 1, 1), halign='left',
                                      text_size=(None, None)))

            self.ids.review_container.add_widget(card)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size