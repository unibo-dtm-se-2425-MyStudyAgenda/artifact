from db.database import Database
from model.topic import Topic

class TopicDAO:
    def __init__(self):
        # Get a singleton instance of the database connection
        self.db = Database.get_instance()

    def insert_topic(self, topic: Topic):
        # Inserts a new topic into the database; uses INSERT OR IGNORE to avoid duplicates by name
        self.db.cursor.execute("INSERT OR IGNORE INTO topics (name) VALUES (?)", (topic.name,))
        self.db.commit()

    def get_all_topics(self):
        # Retrieves all topics from the database; returns a list of rows (id, name)
        self.db.cursor.execute("SELECT * FROM topics")
        return self.db.cursor.fetchall()

    def get_topic_by_id(self, topic_id: int):
        # Retrieves a single topic by its unique ID
        self.db.cursor.execute("SELECT * FROM topics WHERE id = ?", (topic_id,))
        return self.db.cursor.fetchone()
    
    def get_topic_by_name(self, name):
        # Retrieves a topic by its name
        self.db.cursor.execute("SELECT * FROM topics WHERE name = ?", (name,))
        return self.db.cursor.fetchone()