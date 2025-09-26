from datetime import date, time
from app.model.topic import Topic

class Task:
    id_counter = 1

    def __init__(self, description: str, topic: Topic, priority: int, is_completed: bool = False,
                 scheduled_date: date = None, start_time: time = None, end_time: time = None):
        
        self.id = Task.id_counter
        Task.id_counter += 1

        self.description = description
        self.topic = topic
        self.priority = priority
        self.is_completed = is_completed
        self.scheduled_date = scheduled_date
        self.start_time = start_time
        self.end_time = end_time

    def mark_completed(self):
        self.is_completed = True
    
    def mark_notcompleted(self):
        self.is_completed = False

    def __repr__(self):
        return (f"Task(id={self.id}, description='{self.description}', topic={self.topic.name}, "
                f"priority={self.priority}, is_completed={self.is_completed}, "
                f"scheduled_date={self.scheduled_date}, start_time={self.start_time}, end_time={self.end_time})")
