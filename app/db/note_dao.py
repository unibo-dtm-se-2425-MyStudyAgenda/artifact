from app.db.database import Database
from app.model.note import Note

class NoteDAO:
    def __init__(self):
        self.db = Database.get_instance()

    def insert_note(self, note: Note):
        self.db.cursor.execute(
            """ INSERT INTO notes (title, topic_id, content, created_at)
                VALUES (?, ?, ?, ?) """,
        (note.title, note.topic.id if note.topic else None, note.content, note.created_at.isoformat()))
        self.db.commit()
        # Returns the ID of the inserted note
        return self.db.cursor.lastrowid

    def get_all_notes(self):
        self.db.cursor.execute("SELECT * FROM notes ORDER BY created_at DESC")
        return self.db.cursor.fetchall()

    def get_note_by_id(self, note_id: int):
        self.db.cursor.execute("SELECT * FROM notes WHERE id = ?", (note_id,))
        return self.db.cursor.fetchone()

    def delete_note(self, note_id: int):
        self.db.cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        self.db.commit()

    def update_note(self, note_id, new_content):
        self.db.cursor.execute(
            "UPDATE notes SET content = ? WHERE id = ?",
            (new_content, note_id)
        )
        self.db.connection.commit()
