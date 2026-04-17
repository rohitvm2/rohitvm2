from kivy.uix.screenmanager import Screen
from database.db import connect_db
from kivy.app import App

class LoginScreen(Screen):
    def login(self):
        username = self.ids.username.text.strip()
        password = self.ids.password.text.strip()

        if username == "" or password == "":
            self.ids.message.text = "Enter username and password"
            return

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )

        user = cursor.fetchone()
        conn.close()

        if user:
            # ✅ ADD THIS LINE
            App.get_running_app().current_user = username

            role = user[3]

            if role == "admin":
                self.manager.current = "admin"
            else:
                self.manager.current = "dashboard"
        else:
            self.ids.message.text = "Invalid credentials"
        self.manager.get_screen("dashboard").user = username
        self.manager.current = "dashboard"

    def register(self):
        username = self.ids.username.text.strip()
        password = self.ids.password.text.strip()

        if username == "" or password == "":
            self.ids.message.text = "Enter username and password"
            return

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cursor.fetchone()

        if user:
            self.ids.message.text = "User already exists, please login"
        else:
            cursor.execute(
                "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                (username, password, "user")
            )
            conn.commit()
            self.ids.message.text = "Registered successfully. Now login"

            # Clear fields after register
            self.ids.username.text = ""
            self.ids.password.text = ""

        conn.close()

    def on_enter(self):
        self.ids.username.text = ""
        self.ids.password.text = ""
        self.ids.message.text = ""