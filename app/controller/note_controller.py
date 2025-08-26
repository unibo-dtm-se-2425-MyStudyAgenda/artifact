from db.note_dao import NoteDAO
from model.note import Note
from model.topic import Topic

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

    def update_note(self, note_id: int, new_content: str):
        self.dao.update_note(note_id, new_content)

    def _row_to_note(self, row):
        topic_id = row[2] if row[2] is not None else None
        topic = Topic(id=topic_id) if topic_id else None

        return Note(
            id=row[0],
            title=row[1],
            topic=topic,
            content=row[3]
        )

