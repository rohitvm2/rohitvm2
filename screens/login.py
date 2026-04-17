from kivy.uix.screenmanager import Screen
from database.db import connect_db
from kivy.app import App


class LoginScreen(Screen):

    def login(self):
        # This input field now represents either Username OR Email
        login_input = self.ids.username.text.strip()
        password = self.ids.password.text.strip()

        if login_input == "" or password == "":
            self.ids.message.text = "Enter credentials"
            return

        conn = connect_db()
        cursor = conn.cursor()

        # UPDATED SQL: Check if input matches username OR email
        cursor.execute(
            "SELECT * FROM users WHERE (username=? OR email=?) AND password=?",
            (login_input, login_input, password)
        )

        user = cursor.fetchone()
        conn.close()

        if user:
            # Mapping: (0:id, 1:username, 2:password, 3:email, 4:role)
            db_username = user[1]
            db_email = user[3] if len(user) > 3 else "No Email"
            db_role = user[4] if len(user) > 4 else "user"

            # Set global app data
            app = App.get_running_app()
            app.current_user = db_username

            # Sync Dashboard
            dashboard = self.manager.get_screen("dashboard")
            dashboard.user = db_username

            # Sync Profile
            profile = self.manager.get_screen("profile")
            profile.user = db_username
            profile.email = db_email

            # Navigation
            if db_role == "admin":
                self.manager.current = "admin"
            else:
                self.manager.current = "dashboard"

        else:
            self.ids.message.text = "Invalid username/email or password"

    def register(self):
        # During registration, we still want to collect all three separately
        username = self.ids.username.text.strip()
        password = self.ids.password.text.strip()
        email = self.ids.email.text.strip()

        if username == "" or password == "" or email == "":
            self.ids.message.text = "Fill all fields for registration"
            return

        conn = connect_db()
        cursor = conn.cursor()

        # Check for existing user or email
        cursor.execute("SELECT * FROM users WHERE username=? OR email=?", (username, email))
        if cursor.fetchone():
            self.ids.message.text = "Username or Email already exists"
        else:
            try:
                cursor.execute(
                    "INSERT INTO users (username, password, email, role) VALUES (?, ?, ?, ?)",
                    (username, password, email, "user")
                )
                conn.commit()
                self.ids.message.text = "Registered successfully! You can now Login."

                # Clear inputs after registration
                self.ids.username.text = ""
                self.ids.password.text = ""
                self.ids.email.text = ""
            except Exception as e:
                self.ids.message.text = f"Error: {str(e)}"

        conn.close()

    def on_enter(self):
        # Clean slate when the user lands on the login page
        self.ids.username.text = ""
        self.ids.password.text = ""
        self.ids.email.text = ""
        self.ids.message.text = ""