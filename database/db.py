"""Database functions and their isolated background worker."""

from datetime import datetime
import queue
import sqlite3
import threading
from typing import Any


class DatabaseManager:
    def __init__(self) -> None:
        self.requests: queue.Queue[tuple[str, tuple[Any, ...]] | None] = queue.Queue()
        self.results: queue.Queue[Any] = queue.Queue()
        self.thread: threading.Thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    def _run(self) -> None:
        db_file = sqlite3.connect("database/one.db")
        cursor = db_file.cursor()

        while True:
            request = self.requests.get()
            if request is None:
                break

            sql, params = request
            try:
                cursor.execute(sql, params)
                if sql.strip().upper().startswith("SELECT"):
                    self.results.put(cursor.fetchall())
                else:
                    db_file.commit()
                    self.results.put(True)
            except Exception:
                self.results.put(False)
            finally:
                self.requests.task_done()

    def execute(self, sql: str, params: tuple[Any, ...] = ()) -> Any:
        self.requests.put((sql, params))
        return self.results.get()


# Single database service. Its queues and worker are no longer module globals.
database = DatabaseManager()


def create_table():
    database.execute(
        """CREATE TABLE IF NOT EXISTS history(
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        intent TEXT, 
        target TEXT)""",
    )
    database.execute(
        """CREATE TABLE IF NOT EXISTS task(
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        name TEXT, 
        time_remaining TEXT, 
        status TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'finished', 'in progress')), 
        description TEXT)""",
    )

def create_task(name: str, time_remaining: datetime | None, status: str | None = "pending", description: str | None = None):
    database.execute(
        "INSERT INTO task(name, time_remaining, status, description) VALUES(?, ?, ?, ?)",
        (name, time_remaining, status, description),
    )


def view_tasks():
    result = database.execute("SELECT * FROM task")
    if isinstance(result, Exception):
        print(f"Error in {result}")
        return

    for row in result:
        print(row)


def history_insert(intent: str, target: str):
    database.execute(
        "INSERT INTO history(action, target) VALUES(?, ?)",
        (intent, target),
    )


def db_query():
    result = database.execute("SELECT * FROM history")
    if isinstance(result, Exception):
        print(f"Error in {result}")
        return

    for row in result:
        print(row)


create_table()
