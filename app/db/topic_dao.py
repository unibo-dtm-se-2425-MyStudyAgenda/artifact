from app.db.database import Database
from app.model.topic import Topic

class TopicDAO:
    def __init__(self):
        self.db = Database.get_instance()

    def insert_topic(self, topic: Topic):
        self.db.cursor.execute("INSERT OR IGNORE INTO topics (name) VALUES (?)", (topic.name,))
        self.db.commit()

    def get_all_topics(self):
        self.db.cursor.execute("SELECT * FROM topics")
        return self.db.cursor.fetchall()

    def get_topic_by_id(self, topic_id: int):
        self.db.cursor.execute("SELECT * FROM topics WHERE id = ?", (topic_id,))
        return self.db.cursor.fetchone()

    def get_topic_by_name(self, name):
        self.db.cursor.execute("SELECT * FROM topics WHERE name = ?", (name,))
        return self.db.cursor.fetchone()
