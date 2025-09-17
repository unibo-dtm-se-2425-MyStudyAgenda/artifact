import sqlite3

class Database:
    _instance = None

    # Initialize connection to the SQLite database
    def __init__(self, db_name="planner.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_tables()

    # Create tables if they don't exist
    def create_tables(self):
        self.cursor.execute(""" 
            CREATE TABLE IF NOT EXISTS topics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            ); """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                topic_id INTEGER,
                priority INTEGER NOT NULL,
                is_completed BOOLEAN NOT NULL DEFAULT 0,
                scheduled_date TEXT,
                start_time TEXT,
                end_time TEXT,
                FOREIGN KEY(topic_id) REFERENCES topics(id)
            ); """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                topic_id INTEGER,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY(topic_id) REFERENCES topics(id)
            ); """)

        self.connection.commit()

    # Commit pending transactions to the database
    def commit(self):
        self.connection.commit()

    # Close the database connection
    def close(self):
        self.connection.close()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = Database()
        # Return the singleton instance of the Database
        return cls._instance
