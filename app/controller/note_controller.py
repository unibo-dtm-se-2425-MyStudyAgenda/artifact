from db.note_dao import NoteDAO
from model.note import Note
from model.topic import Topic
from datetime import datetime

class NoteController:
    def __init__(self):
        self.dao = NoteDAO()

    def create_note(self, note: Note):
        self.dao.insert_note(note)

    def get_all_notes(self):
        rows = self.dao.get_all_notes()
        return [self._row_to_note(row) for row in rows]

    def get_note_by_id(self, note_id: int):
        row = self.dao.get_note_by_id(note_id)
        return self._row_to_note(row) if row else None

    def delete_note(self, note_id: int):
        self.dao.delete_note(note_id)

    def update_note(self, note_id: int, new_title: str, new_content: str):
        self.dao.update_note(note_id, new_title, new_content)

    def _row_to_note(self, row):
        return Note(
            id=row[0],
            title=row[1],
            topic=Topic(id=row[2]),
            content=row[3],
            created_at=datetime.fromisoformat(row[4])
        )
