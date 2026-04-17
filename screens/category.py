from kivy.uix.screenmanager import Screen

class CategoryScreen(Screen):
    def select_category(self, category_name):
        # You can save the selection to the app class to use in TestScreen
        self.manager.get_screen('test').current_category = category_name
        # Navigate to instructions
        self.manager.current = "instructions"

    def go_back(self):
        self.manager.current = "dashboard"