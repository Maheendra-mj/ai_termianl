import sqlite3
import os

# --- LOGIC UPDATED HERE ---
# This new logic ensures the database is ALWAYS created inside the project directory,
# no matter where you run the 'ai-terminal' command from.

# Get the absolute path of the directory where this file (database.py) is located.
# e.g., /home/mahi/ai_terminal_project/ai_terminal/
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Go up one level to get the main project directory.
# e.g., /home/mahi/ai_terminal_project/
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)

# Define the database name to be inside the main project directory.
DB_NAME = os.path.join(PROJECT_DIR, "terminal_history.db")


def initialize_db():
    """Initializes the SQLite database and creates the history table if it doesn't exist."""
    print(f"[DEBUG] Database will be created at: {DB_NAME}") # Added for clarity
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                command TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                was_ai_generated BOOLEAN NOT NULL
            )
        ''')
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Database error: {e}")

def add_command_to_history(command: str, was_ai_generated: bool):
    """Adds a successfully executed command to the history database."""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO history (command, was_ai_generated) VALUES (?, ?)",
            (command, was_ai_generated)
        )
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Failed to write to database: {e}")

