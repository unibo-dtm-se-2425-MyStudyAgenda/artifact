from app.db.task_dao import TaskDAO
from app.model.task import Task
from app.model.topic import Topic
from datetime import date, time

class TaskController:
    def __init__(self):
        self.dao = TaskDAO()

    def create_task(self, task: Task):
        return self.dao.insert_task(task)

    def get_all_tasks(self):
        tasks_data = self.dao.get_all_tasks()
        return [self._row_to_task(row) for row in tasks_data]

    def set_time_slot(self, task_id, scheduled_date, start_time, end_time):
        self.dao.set_time_slot(task_id, scheduled_date, start_time, end_time)

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
            topic=Topic(id=row[2], name=row[3]),
            priority=row[4],
            is_completed=bool(row[5]),
            scheduled_date=date.fromisoformat(row[6]) if row[6] else None,
            start_time=time.fromisoformat(row[7]) if row[7] else None,
            end_time=time.fromisoformat(row[8]) if row[8] else None
        )
