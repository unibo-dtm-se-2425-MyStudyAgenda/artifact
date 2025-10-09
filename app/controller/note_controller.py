from app.db.note_dao import NoteDAO
from app.model.note import Note
from app.model.topic import Topic
from datetime import datetime

class NoteController:
    def __init__(self):
        # Initialize DAO for database interaction
        self.dao = NoteDAO()

    def create_note(self, note: Note):
         # Insert a new note into the database
        return self.dao.insert_note(note)

    def get_all_notes(self):
        # Retrieve all notes and convert them to Note objects
        rows = self.dao.get_all_notes()
        return [self._row_to_note(row) for row in rows]

    def get_note_by_id(self, note_id: int):
        # Retrieve a note by its ID
        row = self.dao.get_note_by_id(note_id)
        return self._row_to_note(row) if row else None

    def delete_note(self, note_id: int):
        # Permanently remove a note by ID
        self.dao.delete_note(note_id)

    def update_note(self, note_id: int, new_content: str):
        # Update the content of a note
        self.dao.update_note(note_id, new_content)

    def _row_to_note(self, row):
        # Convert a database row into a Note object
        # Handles parsing of created_at field safely
        
        topic_id = row[2] if row[2] is not None else None
        topic = Topic(id=topic_id) if topic_id else None

        created_at = None
        if row[4]:
            try:
                created_at = datetime.fromisoformat(row[4])
            except Exception:
                # fallback in case the result is different
                created_at = datetime.strptime(row[4], "%Y-%m-%d %H:%M:%S")

        return Note(
            id=row[0],
            title=row[1],
            topic=topic,
            content=row[3],
            created_at=created_at
        )
