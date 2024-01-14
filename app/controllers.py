import sqlite3
from datetime import datetime
from app.models import Note, NoteCategory, Relationship
from app.user import User
from app.vision import VisionAnalysisManager

DB_PATH = "your_database.db"

class NoteController:
    def __init__(self):
        self.vision_manager = VisionAnalysisManager() # Заглушка

        self.create_tables()

    def create_tables(self):
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at DATETIME NOT NULL,
                    updated_at DATETIME NOT NULL,
                    category_id INTEGER,
                    FOREIGN KEY (category_id) REFERENCES categories(id)
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS relationships (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    type TEXT NOT NULL,
                    note_id INTEGER,
                    related_note_id INTEGER,
                    FOREIGN KEY (note_id) REFERENCES notes(id),
                    FOREIGN KEY (related_note_id) REFERENCES notes(id)
                )
            """)
    
    def add_note(self, title, content, category=None):
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            
            new_note = Note(title, content, category)
            new_note.created_at = datetime.now().isoformat()
            new_note.updated_at = datetime.now().isoformat()

            cursor.execute("""
                INSERT INTO notes (title, content, created_at, updated_at, category_id)
                VALUES (?, ?, ?, ?, ?)
            """, (new_note.title, new_note.content, new_note.created_at, new_note.updated_at, category.id if category else None))
            
            note_id = cursor.lastrowid
            new_note.id = note_id

            # юзаем заглушки хддд
            categories = self.vision_manager.analyze_note(new_note)
            self.vision_manager.create_relationships(new_note, categories)

            return new_note

    def get_all_notes(self):
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM notes")
            rows = cursor.fetchall()

            notes = []
            for row in rows:
                note = Note(
                    title=row[1],
                    content=row[2],
                    category=None,
                )
                note.id = row[0]
                note.created_at = datetime.fromisoformat(row[3])
                note.created_at = datetime.fromisoformat(row[4])

                notes.append(note)

            return notes