from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty

class InstructionScreen(Screen):
    # You can use this to dynamically change instructions based on the category
    instructions_text = StringProperty(
        "1. You will have 30 seconds per question.\n"
        "2. Each correct answer gives you 1 point.\n"
        "3. You cannot go back once a question is answered.\n"
        "4. Click 'Start Test' when you are ready."
    )

    def start_test(self):
        self.manager.current = "test"

    def go_back(self):
        self.manager.current = "dashboard" # Or "category" if you've added it