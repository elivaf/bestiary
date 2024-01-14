from datetime import datetime
import sqlite3

DB_PATH = "your_database.db"

class Note:
    def __init__(self, title="", content="", category=None):
        self.id = None
        self.title = title
        self.content = content
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.category = category
        self.relationships = []

    def add_relationship(self, relationship):
        self.relationships.append(relationship)

    def remove_relationship(self, relationship_id):
        self.relationships = [rel for rel in self.relationships if rel.id != relationship_id]

    def get_related_notes(self):
        return [rel.related_note for rel in self.relationships]
    
    @classmethod
    def get_prompt(cls, edit_mode=False):
        prompts = {
            "title": "Введите заголовок заметки:",
            "content": "Введите содержание заметки:",
        }

        if edit_mode:
            prompts["user_fields"] = "Введите пользовательские поля (если есть):"

        return prompts

class NoteCategory:
    def __init__(self, name):
        self.id = None
        self.name = name

    def get_category_notes(self):
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM notes WHERE category_id = ?", (self.id,))
            rows = cursor.fetchall()

            notes = []
            for row in rows:
                note = Note(
                    title=row[1],
                    content=row[2],
                    category=self,
                )
                note.id = row[0]
                note.created_at = datetime.fromisoformat(row[3])
                note.updated_at = datetime.fromisoformat(row[4])

                notes.append(note)

            return notes

class Relationship:
    def __init__(self, related_note, relationship_type):
        self.id = None
        self.related_note = related_note
        self.type = relationship_type

    def update_type(self, new_type):
        self.type = new_type
