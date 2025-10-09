"""
Represents a topic/category to which tasks or notes can be assigned
Attributes:
    id (int): Unique identifier of the topic
    name (str): Name of the topic
"""

class Topic:
    _id_counter = 1

    def __init__(self, id=None, name=None):
        if id is not None:
            self.id = id
        else:
            self.id = Topic._id_counter
            Topic._id_counter += 1
        self.name = name

    def __repr__(self):
        return f"Topic(id={self.id}, name='{self.name}')"
