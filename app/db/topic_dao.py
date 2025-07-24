from db.database import Database
from model.topic import Topic

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

    def delete_topic(self, topic_id: int):
        self.db.cursor.execute("DELETE FROM topics WHERE id = ?", (topic_id,))
        self.db.commit()

    def update_topic_name(self, topic_id: int, new_name: str):
        self.db.cursor.execute("UPDATE topics SET name = ? WHERE id = ?", (new_name, topic_id))
        self.db.commit()
