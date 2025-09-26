from app.db.database import Database
from app.model.note import Note

class NoteDAO:
    def __init__(self):
        self.db = Database.get_instance()

    def insert_note(self, note: Note):
        self.db.cursor.execute(
            """ INSERT INTO notes (title, content, created_at)
                VALUES (?, ?, ?) """,
        (note.title, note.content, note.created_at.isoformat()))
        self.db.commit()

    def get_all_notes(self):
        self.db.cursor.execute("SELECT * FROM notes ORDER BY created_at DESC")
        return self.db.cursor.fetchall()

    def get_note_by_id(self, note_id: int):
        self.db.cursor.execute("SELECT * FROM notes WHERE id = ?", (note_id,))
        return self.db.cursor.fetchone()

    def delete_note(self, note_id: int):
        self.db.cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        self.db.commit()

    def update_note(self, note_id: int, new_title: str, new_content: str):
        self.db.cursor.execute(
            """ UPDATE notes
                SET title = ?, content = ?
                WHERE id = ? """, 
        (new_title, new_content, note_id))
        self.db.commit()
