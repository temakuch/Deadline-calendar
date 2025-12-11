import sqlite3

class DatabaseManager:
    def __init__(self, db_name="deadline_calendar.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        """Створює таблицю, якщо її не існує"""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS deadlines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                due_date TEXT NOT NULL,
                due_time TEXT,
                status TEXT DEFAULT 'Active'
            )
        """)
        self.conn.commit()

    def add_event(self, title, description, due_date, due_time):
        """Додає нову подію"""
        self.cursor.execute("""
            INSERT INTO deadlines (title, description, due_date, due_time)
            VALUES (?, ?, ?, ?)
        """, (title, description, due_date, due_time))
        self.conn.commit()

    def get_events_by_date(self, date_str):
        """Отримує всі події для конкретної дати (формат YYYY-MM-DD)"""
        self.cursor.execute("SELECT * FROM deadlines WHERE due_date = ?", (date_str,))
        return self.cursor.fetchall()
    
    def delete_event(self, event_id):
        """Видаляє подію за ID"""
        self.cursor.execute("DELETE FROM deadlines WHERE id = ?", (event_id,))
        self.conn.commit()