import sqlite3


def connect_db():
    # TIP: Using "database/app.db" is good, ensures it stays in your project folder
    conn = sqlite3.connect("database/app.db")
    return conn


def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        email TEXT,
        role TEXT
    )
    """)

    # Questions table - ADDED: category column
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS questions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT,
        option1 TEXT,
        option2 TEXT,
        option3 TEXT,
        option4 TEXT,
        answer TEXT,
        category TEXT
    )
    """)

    # Results table - ADDED: category and timestamp for better Data Science tracking
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS results(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        category TEXT,
        score INTEGER,
        date DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


def create_admin():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username='admin'")
    if not cursor.fetchone():
        cursor.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            ("admin", "admin123", "admin")
        )
    conn.commit()
    conn.close()


# HELPER FUNCTION: Call this once to fill your app with sample questions
def seed_questions():
    conn = connect_db()
    cursor = conn.cursor()

    # Sample questions for different categories
    sample_data = [
        ("What is the symbol of water?", "H2O", "O3", "NaCl", "CO3", "H2O", "Science"),
        ("Which keyword is used to define a function in Python?", "func", "define", "def", "function", "def", "Python"),
        ("What does LSTM stand for?", "Long Short-Term Memory", "Low State Time Model", "Linear System Task Manager",
         "None", "Long Short-Term Memory", "Data Science"),
        ("What is 5 + 7?", "10", "12", "13", "11", "12", "Maths")
    ]

    # Check if we already have questions to avoid duplicates
    cursor.execute("SELECT COUNT(*) FROM questions")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("""
            INSERT INTO questions (question, option1, option2, option3, option4, answer, category)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, sample_data)
        print("Database seeded with sample questions!")

    conn.commit()
    conn.close()