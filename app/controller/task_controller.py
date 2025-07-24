from db.task_dao import TaskDAO
from model.task import Task
from model.topic import Topic
from datetime import date, time

class TaskController:
    def __init__(self):
        self.dao = TaskDAO()

    def create_task(self, task: Task):
        self.dao.insert_task(task)

    def get_all_tasks(self):
        tasks_data = self.dao.get_all_tasks()
        return [self._row_to_task(row) for row in tasks_data]

    def get_tasks_by_topic(self, topic_id: int):
        tasks_data = self.dao.get_tasks_by_topic(topic_id)
        return [self._row_to_task(row) for row in tasks_data]

    def set_time_slot(self, task_id: int, scheduled_date: date, start_time: time, end_time: time):
        self.dao.set_time_slot(task_id, scheduled_date.isoformat(), start_time.isoformat(), end_time.isoformat())

    def delete_task(self, task_id: int):
        self.dao.delete_task(task_id)

    def mark_completed(self, task_id: int):
        self.dao.mark_completed(task_id)
    
    def mark_notcompleted(self, task_id: int):
        self.dao.mark_notcompleted(task_id)

    def _row_to_task(self, row):
        return Task(
            id=row[0],
            description=row[1],
            topic=Topic(id=row[2]),
            priority=row[3],
            is_completed=bool(row[4]),
            scheduled_date=date.fromisoformat(row[5]) if row[5] else None,
            start_time=time.fromisoformat(row[6]) if row[6] else None,
            end_time=time.fromisoformat(row[7]) if row[7] else None
        )
