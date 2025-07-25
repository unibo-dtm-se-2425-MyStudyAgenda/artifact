from db.topic_dao import TopicDAO
from model.topic import Topic

class TopicController:
    def __init__(self):
        self.dao = TopicDAO()

    def create_topic(self, topic: Topic):
        self.dao.insert_topic(topic)

    def get_all_topics(self):
        rows = self.dao.get_all_topics()
        return [self._row_to_topic(row) for row in rows]

    def get_topic_by_id(self, topic_id: int):
        row = self.dao.get_topic_by_id(topic_id)
        return self._row_to_topic(row) if row else None

    def delete_topic(self, topic_id: int):
        self.dao.delete_topic(topic_id)

    def update_topic_name(self, topic_id: int, new_name: str):
        self.dao.update_topic_name(topic_id, new_name)

    def _row_to_topic(self, row):
        return Topic(id=row[0], name=row[1])