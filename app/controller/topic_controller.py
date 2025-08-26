from db.topic_dao import TopicDAO
from model.topic import Topic

class TopicController:
    def __init__(self):
        self.dao = TopicDAO()

    def create_topic(self, topic_name: Topic):
        topic = Topic(name=topic_name)
        self.dao.insert_topic(topic)

    def get_all_topics(self):
        rows = self.dao.get_all_topics()
        return [self._row_to_topic(row) for row in rows]

    def get_topic_by_id(self, topic_id: int):
        row = self.dao.get_topic_by_id(topic_id)
        return self._row_to_topic(row) if row else None
    
    def get_topic_by_name(self, name):
        row = self.dao.get_topic_by_name(name)
        if row:
            return Topic(id=row[0], name=row[1])
        return None

    def delete_topic(self, topic_id: int):
        self.dao.delete_topic(topic_id)

    def update_topic_name(self, topic_id: int, new_name: str):
        self.dao.update_topic_name(topic_id, new_name)

    def get_topic_id(self, name: str) -> int | None:
        row = self.dao.get_topic_by_name(name)
        return row[0] if row else None
    
    def get_topic_name(self, id: int) -> str | None:
        row = self.dao.get_topic_by_id(id)
        return row[1] if row else None

    def _row_to_topic(self, row):
        return Topic(id=row[0], name=row[1])