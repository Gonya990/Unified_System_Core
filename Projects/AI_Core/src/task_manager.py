"""
Simple Task Manager for AI Telegram Bot.
Stores tasks in SQLite database.
"""

import logging
import sqlite3

logger = logging.getLogger(__name__)


class TaskManager:
    def __init__(self, db_path: str = "tasks.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialize SQLite database and tables."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS tasks (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        text TEXT,
                        status TEXT DEFAULT 'pending',
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                conn.commit()
                logger.info(f"Task database initialized at {self.db_path}")
        except Exception as e:
            logger.error(f"Failed to init task DB: {e}")

    def add_task(self, user_id: int, text: str) -> int:
        """Add a new task."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO tasks (user_id, text) VALUES (?, ?)", (user_id, text))
                conn.commit()
                return cursor.lastrowid
        except Exception as e:
            logger.error(f"Failed to add task: {e}")
            return -1

    def list_tasks(self, user_id: int, status: str = "pending") -> list[dict]:
        """List tasks for a user."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT * FROM tasks WHERE user_id = ? AND status = ? ORDER BY id DESC", (user_id, status)
                )
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Failed to list tasks: {e}")
            return []

    def complete_task(self, user_id: int, task_id: int) -> bool:
        """Mark a task as completed."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE tasks SET status = 'completed' WHERE id = ? AND user_id = ?", (task_id, user_id))
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            logger.error(f"Failed to complete task: {e}")
            return False
