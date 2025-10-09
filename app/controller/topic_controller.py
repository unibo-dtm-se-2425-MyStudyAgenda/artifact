from app.db.topic_dao import TopicDAO
from app.model.topic import Topic

class TopicController:
    def __init__(self):
        # Initialize DAO for database interaction
        self.dao = TopicDAO()

    def create_topic(self, topic_name: Topic):
        # Insert a new topic into the database
        topic = Topic(name=topic_name)
        self.dao.insert_topic(topic)

    def get_all_topics(self):
        # Retrieve all topics and convert them to Topic objects
        rows = self.dao.get_all_topics()
        return [self._row_to_topic(row) for row in rows]

    def get_topic_by_id(self, topic_id: int):
        # Retrieve a topic by its ID
        row = self.dao.get_topic_by_id(topic_id)
        return self._row_to_topic(row) if row else None
    
    def get_topic_by_name(self, name):
        # Retrieve a topic by its name
        row = self.dao.get_topic_by_name(name)
        if row:
            return Topic(id=row[0], name=row[1])
        return None

    def get_topic_id(self, name: str) -> int | None:
        # Return the ID of a topic given its name
        row = self.dao.get_topic_by_name(name)
        return row[0] if row else None
    
    def get_topic_name(self, id: int) -> str | None:
        # Return the name of a topic given its ID
        row = self.dao.get_topic_by_id(id)
        return row[1] if row else None

    def _row_to_topic(self, row):
        # Convert a database row into a Topic object
        return Topic(id=row[0], name=row[1])