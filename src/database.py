import sqlite3
from contextlib import contextmanager


class Database:
    def __init__(self, db_file='events.db'):
        self.db_file = db_file
        self._create_table()

    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_file)
        try:
            yield conn
        finally:
            conn.close()

    def _create_table(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS events (
                    uid TEXT PRIMARY KEY,
                    title TEXT,
                    course_number TEXT,
                    due_date TEXT,
                    processed_date TEXT,
                    todoist_task_id TEXT,
                    sync_status TEXT
                )
            ''')
            conn.commit()

    def event_exists(self, uid):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM events WHERE uid = ?", (uid,))
            return cursor.fetchone() is not None

    def add_event(self, event):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO events 
                (uid, title, course_number, due_date, processed_date, sync_status)
                VALUES (?, ?, ?, ?, datetime('now'), 'pending')
            ''', (event['uid'], event['title'], event['course_number'], event['due_date'].isoformat()))
            conn.commit()

    def update_sync_status(self, uid, status, todoist_task_id=None):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if todoist_task_id:
                cursor.execute('''
                    UPDATE events 
                    SET sync_status = ?, todoist_task_id = ? 
                    WHERE uid = ?
                ''', (status, todoist_task_id, uid))
            else:
                cursor.execute('''
                    UPDATE events 
                    SET sync_status = ? 
                    WHERE uid = ?
                ''', (status, uid))
            conn.commit()

    def get_pending_events(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM events WHERE sync_status = 'pending'")
            return cursor.fetchall()
