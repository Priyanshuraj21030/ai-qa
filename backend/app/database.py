import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).parent.parent / "qa_history.db"

def init_db():
    conn = sqlite3.connect(str(DATABASE_PATH))
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def get_db():
    return sqlite3.connect(str(DATABASE_PATH)) 