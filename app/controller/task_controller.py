from db.task_dao import TaskDAO
from model.task import Task
from model.topic import Topic
#from controller.topic_controller import TopicController
from datetime import date, time

class TaskController:
    def __init__(self):
        # Initialize DAO and TopicController for database interaction
        self.dao = TaskDAO()
        #self.topic_controller = TopicController()
    
    def create_task(self, task: Task):
         # Insert a new task into the database
        return self.dao.insert_task(task)

    """def create_task(self, description, topic_name, priority, date=None, start_time=None, end_time=None):
        # Create a new Task object and insert it into the database
        # Handles topic lookup and conversion of date/time strings

        topic_obj = self.topic_controller.get_topic_by_name(topic_name)
        if not topic_obj:
            raise ValueError(f"Topic '{topic_name}' non trovato")

        if isinstance(date, str) and date.strip():
            date = datetime.strptime(date, "%Y-%m-%d").date()
        else:
            date = None

        if isinstance(start_time, str) and start_time.strip():
            start_time = datetime.strptime(start_time, "%H:%M").time()
        else:
            start_time = None

        if isinstance(end_time, str) and end_time.strip():
            end_time = datetime.strptime(end_time, "%H:%M").time()
        else:
            end_time = None

        task = Task(
            description=description,
            topic=topic_obj,
            priority=priority,
            scheduled_date=date,
            start_time=start_time,
            end_time=end_time
        )

        task_id = self.dao.insert_task(task)
        task.task_id = task_id
        return task_id"""

    def get_all_tasks(self):
        # Retrieve all tasks from the database and map them to Task objects
        tasks_data = self.dao.get_all_tasks()
        return [self._row_to_task(row) for row in tasks_data]

    def get_tasks_by_topic(self, topic_id: int):
        # Retrieve all tasks that belong to a specific topic
        tasks_data = self.dao.get_tasks_by_topic(topic_id)
        return [self._row_to_task(row) for row in tasks_data]

    def set_time_slot(self, task_id, scheduled_date, start_time, end_time):
        # Update scheduled date and time range for a task
        self.dao.set_time_slot(task_id, scheduled_date, start_time, end_time)

    def delete_task(self, task_id: int):
        # Permanently remove a task by ID
        self.dao.delete_task(task_id)

    def mark_completed(self, task_id: int):
        # Mark task as completed
        self.dao.mark_completed(task_id)
    
    def mark_notcompleted(self, task_id: int):
        # Mark task as not completed
        self.dao.mark_notcompleted(task_id)

    def _row_to_task(self, row):
        # Convert a database row into a Task object
        return Task(
            task_id=row[0],
            description=row[1],
            topic=Topic(id=row[2], name=row[3]),
            priority=row[4],
            is_completed=bool(row[5]),
            scheduled_date=date.fromisoformat(row[6]) if row[6] else None,
            start_time=time.fromisoformat(row[7]) if row[7] else None,
            end_time=time.fromisoformat(row[8]) if row[8] else None
        )