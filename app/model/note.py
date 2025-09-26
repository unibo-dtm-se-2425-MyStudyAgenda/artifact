from datetime import datetime
from app.model.topic import Topic

class Note:
    id_counter = 1

    def __init__(self, title: str, topic: Topic, content: str):
        self.id = Note.id_counter
        Note.id_counter += 1

        self.title = title
        self.topic = topic
        self.content = content
        self.created_at = datetime.now()

    def __repr__(self):
        return f"Note(id={self.id}, title='{self.title}', created_at='{self.created_at}')"
