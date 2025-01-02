from datetime import datetime
from sqlite3 import Connection
from typing import List, Optional

class Question:
    def __init__(self, question: str, answer: str, 
                 id: Optional[int] = None, 
                 timestamp: Optional[str] = None):
        self.id = id
        self.question = question
        self.answer = answer
        self.timestamp = timestamp or datetime.now().isoformat()

    def to_dict(self):
        return {
            "id": self.id,
            "question": self.question,
            "answer": self.answer,
            "timestamp": self.timestamp
        }

    def save(self, db: Connection):
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO questions (question, answer) VALUES (?, ?)",
            (self.question, self.answer)
        )
        db.commit()
        self.id = cursor.lastrowid

    @staticmethod
    def get_all(db: Connection) -> List["Question"]:
        cursor = db.cursor()
        cursor.execute("SELECT id, question, answer, timestamp FROM questions ORDER BY timestamp DESC")
        return [
            Question(id=row[0], question=row[1], answer=row[2], timestamp=row[3])
            for row in cursor.fetchall()
        ] 

    @staticmethod
    def count_all(db: Connection) -> int:
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM questions")
        return cursor.fetchone()[0]

    @staticmethod
    def get_paginated(db: Connection, page: int = 1, page_size: int = 10) -> List["Question"]:
        offset = (page - 1) * page_size
        cursor = db.cursor()
        cursor.execute(
            """
            SELECT id, question, answer, timestamp 
            FROM questions 
            ORDER BY timestamp DESC
            LIMIT ? OFFSET ?
            """,
            (page_size, offset)
        )
        return [
            Question(id=row[0], question=row[1], answer=row[2], timestamp=row[3])
            for row in cursor.fetchall()
        ] 