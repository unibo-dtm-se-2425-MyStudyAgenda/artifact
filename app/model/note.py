from datetime import datetime
from app.model.topic import Topic

"""
Represents a user-created note
Attributes:
    id (int): Unique identifier for the note
    title (str): Short title of the note
    topic (Topic): Associated topic (optional)
    content (str): Main text content of the note
    created_at (datetime): Timestamp of when the note was created
"""

class Note:
    _id_counter = 1

    def __init__(self, title: str, topic: Topic = None, content: str = "", id=None, created_at: datetime = None):
        if id is not None:
            self.id = id
        else:
            self.id = Note._id_counter
            Note._id_counter += 1

        self.title = title
        self.topic = topic
        self.content = content
        self.created_at = created_at if created_at is not None else datetime.now()

    def __repr__(self):
        return f"Note(id={self.id}, title='{self.title}', topic='{self.topic}', created_at='{self.created_at}')"
