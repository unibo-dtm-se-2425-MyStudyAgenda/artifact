from db.database import Database
from model.task import Task
from datetime import datetime

class TaskDAO:
    def __init__(self):
        self.db = Database.get_instance()

    def insert_task(self, task: Task):
        self.db.cursor.execute(
            """INSERT INTO tasks (description, topic_id, priority, is_completed, scheduled_date, start_time, end_time)
            VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                task.description,
                task.topic.id,
                task.priority,
                task.is_completed,
                task.scheduled_date.isoformat() if task.scheduled_date else None,
                task.start_time.isoformat() if task.start_time else None,
                task.end_time.isoformat() if task.end_time else None
            )
        )
        self.db.commit()
        return self.db.cursor.lastrowid


    def get_all_tasks(self):
        self.db.cursor.execute(
            """SELECT t.id, t.description, t.topic_id, tp.name, t.priority, t.is_completed, t.scheduled_date, t.start_time, t.end_time
            FROM tasks t
            LEFT JOIN topics tp ON t.topic_id = tp.id""")
        return self.db.cursor.fetchall()


    def get_tasks_by_topic(self, topic_id: int):
        self.db.cursor.execute("SELECT * FROM tasks WHERE topic_id = ?", (topic_id,))
        return self.db.cursor.fetchall()

    def set_time_slot(self, task_id: int, scheduled_date: str, start_time: str, end_time: str):
        self.db.cursor.execute(
            """ UPDATE tasks
                SET scheduled_date = ?, start_time = ?, end_time = ?
                WHERE id = ? """, 
        (scheduled_date, start_time, end_time, task_id))
        self.db.commit()

    def delete_task(self, task_id: int):
        self.db.cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        self.db.commit()

    def mark_completed(self, task_id: int):
        self.db.cursor.execute("UPDATE tasks SET is_completed = 1 WHERE id = ?", (task_id,))
        self.db.commit()
    
    def mark_notcompleted(self, task_id: int):
        self.db.cursor.execute("UPDATE tasks SET is_completed = 0 WHERE id = ?", (task_id,))
        self.db.commit()
