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

    """def delete_topic(self, topic_id: int):
        # Deletes an existing topic from the database by its unique ID
        self.db.cursor.execute("DELETE FROM topics WHERE id = ?", (topic_id,))
        self.db.commit()

    def update_topic_name(self, topic_id: int, new_name: str):
        # Updates the name of a topic by its ID
        self.db.cursor.execute("UPDATE topics SET name = ? WHERE id = ?", (new_name, topic_id))
        self.db.commit()"""