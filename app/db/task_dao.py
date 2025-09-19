from db.database import Database
from model.task import Task

class TaskDAO:
    def __init__(self):
        # Get a singleton instance of the database connection
        self.db = Database.get_instance()

    def insert_task(self, task: Task):
        # Inserts a new task into the database
        self.db.cursor.execute(
            """INSERT INTO tasks (description, topic_id, priority, is_completed, scheduled_date, start_time, end_time)
            VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                task.description,
                task.topic.id,
                task.priority,
                task.is_completed,
                # Converts datetime fields (scheduled_date, start_time, end_time) to string format
                task.scheduled_date.format() if task.scheduled_date else None,
                task.start_time.format() if task.start_time else None,
                task.end_time.format() if task.end_time else None
            )
        )
        self.db.commit()
        # Returns the ID of the inserted task
        return self.db.cursor.lastrowid

    def get_all_tasks(self):
        # Retrieve all tasks with their associated topic names
        self.db.cursor.execute(
            """SELECT t.id, t.description, t.topic_id, tp.name, t.priority, t.is_completed, t.scheduled_date, t.start_time, t.end_time
            FROM tasks t
            LEFT JOIN topics tp ON t.topic_id = tp.id""")
            # Uses a LEFT JOIN so tasks without a topic are still returned
        return self.db.cursor.fetchall()

    def get_tasks_by_topic(self, topic_id: int):
        # Retrieves all the existing tasks associated with the same topic identified by its ID
        self.db.cursor.execute("SELECT * FROM tasks WHERE topic_id = ?", (topic_id,))
        return self.db.cursor.fetchall()

    def set_time_slot(self, task_id: int, scheduled_date: str, start_time: str, end_time: str):
        # Update the scheduling information (date, start, end times) of an existing task identified by its ID
        self.db.cursor.execute(
            """ UPDATE tasks
                SET scheduled_date = ?, start_time = ?, end_time = ?
                WHERE id = ? """, 
        (scheduled_date, start_time, end_time, task_id))
        self.db.commit()

    def delete_task(self, task_id: int):
        # Deletes a specific task identified by its ID
        self.db.cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        self.db.commit()

    def mark_completed(self, task_id: int):
        # Updates an existing task's boolean is_completed to true (1)
        self.db.cursor.execute("UPDATE tasks SET is_completed = 1 WHERE id = ?", (task_id,))
        self.db.commit()
    
    def mark_notcompleted(self, task_id: int):
        # Updates an existing task's boolean is_completed to false (0)
        self.db.cursor.execute("UPDATE tasks SET is_completed = 0 WHERE id = ?", (task_id,))
        self.db.commit()