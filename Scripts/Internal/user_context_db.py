import logging
import sqlite3
from datetime import datetime
from typing import Any, Optional

logger = logging.getLogger(__name__)


class UserContextDB:
    def __init__(self, db_path="user_context.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    full_name TEXT,
                    is_approved BOOLEAN DEFAULT 0,
                    is_google_connected BOOLEAN DEFAULT 0,
                    google_creds TEXT,
                    branch_id TEXT DEFAULT 'HOME_HQ',
                    role TEXT DEFAULT 'MEMBER',
                    last_interaction TIMESTAMP,
                    created_at TIMESTAMP
                )
            """)
            # Events context table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS event_contexts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    event_title TEXT,
                    context_description TEXT,
                    event_time TIMESTAMP,
                    created_at TIMESTAMP,
                    FOREIGN KEY(user_id) REFERENCES users(user_id)
                )
            """)
            # Key Value Store for random persistence
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS kv_store (
                    key TEXT PRIMARY KEY,
                    value TEXT
                )
            """)
            # Chat memory/facts extracted by AI
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS chat_memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    fact_short TEXT,
                    fact_full TEXT,
                    source_date TIMESTAMP,
                    created_at TIMESTAMP,
                    FOREIGN KEY(user_id) REFERENCES users(user_id)
                )
            """)
            # Pending Approvals Queue
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS pending_approvals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    requester_agent TEXT,
                    task_type TEXT,
                    task_payload TEXT,
                    status TEXT DEFAULT 'pending',
                    created_at TIMESTAMP
                )
            """)
            conn.commit()

    def add_user(self, user_id: int, username: str, full_name: str, branch_id: str = "HOME_HQ", role: str = "MEMBER"):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT OR IGNORE INTO users (user_id, username, full_name, branch_id, role, last_interaction, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
                (user_id, username, full_name, branch_id, role, datetime.now(), datetime.now()),
            )
            conn.commit()

    def add_memory(self, user_id: int, fact_short: str, fact_full: str):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO chat_memories (user_id, fact_short, fact_full, source_date, created_at)
                VALUES (?, ?, ?, ?, ?)
            """,
                (user_id, fact_short, fact_full, datetime.now(), datetime.now()),
            )
            conn.commit()

    def get_memories(self, user_id: int, limit: int = 10) -> list[dict[str, Any]]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM chat_memories WHERE user_id = ? ORDER BY created_at DESC LIMIT ?", (user_id, limit)
            )
            return [dict(row) for row in cursor.fetchall()]

    def clear_memories(self, user_id: int):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM chat_memories WHERE user_id = ?", (user_id,))
            conn.commit()

    def update_last_interaction(self, user_id: int):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET last_interaction = ? WHERE user_id = ?", (datetime.now(), user_id))
            conn.commit()

    def get_inactive_users(self, hours: int = 72) -> list[dict[str, Any]]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM users WHERE last_interaction < datetime('now', '-' || ? || ' hours') AND is_approved = 1",
                (hours,),
            )
            return [dict(row) for row in cursor.fetchall()]

    def get_user(self, user_id: int) -> Optional[dict[str, Any]]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def set_google_connected(self, user_id: int, connected: bool = True):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET is_google_connected = ? WHERE user_id = ?", (1 if connected else 0, user_id)
            )
            conn.commit()

    def is_approved(self, user_id: int) -> bool:
        user = self.get_user(user_id)
        if user:
            return bool(user["is_approved"])
        return False

    def approve_user(self, user_id: int, approve: bool = True):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET is_approved = ? WHERE user_id = ?", (1 if approve else 0, user_id))
            conn.commit()

    def add_event_context(self, user_id: int, event_title: str, context_description: str, event_time: datetime):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO event_contexts (user_id, event_title, context_description, event_time, created_at)
                VALUES (?, ?, ?, ?, ?)
            """,
                (user_id, event_title, context_description, event_time, datetime.now()),
            )
            conn.commit()
