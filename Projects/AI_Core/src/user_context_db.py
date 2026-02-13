import logging
import os
import sqlite3
from datetime import datetime
from typing import Any, Optional

logger = logging.getLogger(__name__)


class UserContextDB:
    def __init__(self, db_path="user_context.db"):
        # Allow environment variable override for K8s/Docker persistence
        self.db_path = os.getenv("DB_PATH", db_path)
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
            # Migrate: Add missing columns if they don't exist
            cursor.execute("PRAGMA table_info(users)")
            columns = {row[1] for row in cursor.fetchall()}

            if "branch_id" not in columns:
                logger.info("Migrating: Adding branch_id column to users table")
                cursor.execute("ALTER TABLE users ADD COLUMN branch_id TEXT DEFAULT 'HOME_HQ'")

            if "role" not in columns:
                logger.info("Migrating: Adding role column to users table")
                cursor.execute("ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'MEMBER'")

            conn.commit()
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
            # Mashov homework cache
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS mashov_homework (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    homework_data TEXT,
                    fetched_at TIMESTAMP,
                    FOREIGN KEY(user_id) REFERENCES users(user_id)
                )
            """)
            conn.commit()

    def add_user(
        self,
        user_id: int,
        username: str,
        full_name: str,
        branch_id: str = "HOME_HQ",
        role: str = "MEMBER",
    ):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT OR IGNORE INTO users (
                    user_id,
                    username,
                    full_name,
                    branch_id,
                    role,
                    last_interaction,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    user_id,
                    username,
                    full_name,
                    branch_id,
                    role,
                    datetime.now(),
                    datetime.now(),
                ),
            )
            conn.commit()

    def add_memory(self, user_id: int, fact_short: str, fact_full: str):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO chat_memories (
                    user_id,
                    fact_short,
                    fact_full,
                    source_date,
                    created_at
                )
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
                """
                SELECT *
                FROM chat_memories
                WHERE user_id = ?
                ORDER BY created_at DESC
                LIMIT ?
                """,
                (user_id, limit),
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
            cursor.execute(
                "UPDATE users SET last_interaction = ? WHERE user_id = ?",
                (datetime.now(), user_id),
            )
            conn.commit()

    def get_inactive_users(self, hours: int = 72) -> list[dict[str, Any]]:
        """Find users who haven't interacted for more than N hours."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT *
                FROM users
                WHERE last_interaction < datetime('now', '-' || ? || ' hours')
                  AND is_approved = 1
                """,
                (hours,),
            )
            return [dict(row) for row in cursor.fetchall()]

    def list_users(self) -> list[dict[str, Any]]:
        """Return all users (admin/scheduler use)."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users")
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
                "UPDATE users SET is_google_connected = ? WHERE user_id = ?",
                (1 if connected else 0, user_id),
            )
            conn.commit()

    def set_google_creds(self, user_id: int, credentials: str):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET google_creds = ? WHERE user_id = ?",
                (credentials, user_id),
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
            cursor.execute(
                "UPDATE users SET is_approved = ? WHERE user_id = ?",
                (1 if approve else 0, user_id),
            )
            conn.commit()

    def add_event_context(
        self,
        user_id: int,
        event_title: str,
        context_description: str,
        event_time: datetime,
    ):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO event_contexts (
                    user_id,
                    event_title,
                    context_description,
                    event_time,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (user_id, event_title, context_description, event_time, datetime.now()),
            )
            conn.commit()

    # ========== RBAC Methods ==========
    # Role hierarchy: ADMIN > MEMBER > GUEST
    ROLE_HIERARCHY = {"ADMIN": 3, "MEMBER": 2, "GUEST": 1}

    def get_role(self, user_id: int) -> str:
        """Get user's role. Returns 'GUEST' if user not found."""
        user = self.get_user(user_id)
        if user and user.get("role"):
            return user["role"]
        return "GUEST"

    def set_role(self, user_id: int, role: str) -> bool:
        """Set user's role. Role must be ADMIN, MEMBER, or GUEST."""
        role = role.upper()
        if role not in self.ROLE_HIERARCHY:
            logger.warning(f"Invalid role: {role}")
            return False
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET role = ? WHERE user_id = ?", (role, user_id))
            conn.commit()
            return cursor.rowcount > 0

    def has_permission(self, user_id: int, required_role: str) -> bool:
        """Check if user has at least the required role level."""
        user_role = self.get_role(user_id)
        required_level = self.ROLE_HIERARCHY.get(required_role.upper(), 0)
        user_level = self.ROLE_HIERARCHY.get(user_role, 0)
        return user_level >= required_level

    def is_admin(self, user_id: int) -> bool:
        """Check if user is an admin."""
        return self.get_role(user_id) == "ADMIN"

    def list_admins(self) -> list[dict[str, Any]]:
        """Get all admin users."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE role = 'ADMIN'")
            return [dict(row) for row in cursor.fetchall()]

    def promote_to_admin(self, user_id: int) -> bool:
        """Promote user to admin role."""
        return self.set_role(user_id, "ADMIN")

    def demote_to_member(self, user_id: int) -> bool:
        """Demote user to member role."""
        return self.set_role(user_id, "MEMBER")

    # ========== Mashov Integration Methods ==========

    def cache_homework(self, user_id: int, homework_data: list) -> bool:
        """
        Cache homework data for user.

        Args:
            user_id: User ID
            homework_data: List of homework items to cache

        Returns:
            True if cached successfully
        """
        try:
            import json

            homework_json = json.dumps(homework_data, ensure_ascii=False)

            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                # Delete old cache for this user
                cursor.execute("DELETE FROM mashov_homework WHERE user_id = ?", (user_id,))
                # Insert new cache
                cursor.execute(
                    """
                    INSERT INTO mashov_homework (user_id, homework_data, fetched_at)
                    VALUES (?, ?, ?)
                """,
                    (user_id, homework_json, datetime.now()),
                )
                conn.commit()
                logger.debug(f"[MASHOV] Cached {len(homework_data)} homework items for user {user_id}")
                return True
        except Exception as e:
            logger.error(f"[MASHOV] Failed to cache homework: {e}")
            return False

    def get_cached_homework(self, user_id: int, max_age_hours: int = 24) -> Optional[list]:
        """
        Get cached homework data if it's recent enough.

        Args:
            user_id: User ID
            max_age_hours: Maximum age of cache in hours (default: 24)

        Returns:
            List of homework items or None if cache is too old/not found
        """
        try:
            import json

            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT homework_data, fetched_at FROM mashov_homework
                    WHERE user_id = ?
                    AND fetched_at > datetime('now', '-' || ? || ' hours')
                    ORDER BY fetched_at DESC LIMIT 1
                """,
                    (user_id, max_age_hours),
                )
                row = cursor.fetchone()
                if row:
                    homework_json, fetched_at = row
                    homework_data = json.loads(homework_json)
                    logger.debug(f"[MASHOV] Retrieved cached homework for user {user_id} (fetched: {fetched_at})")
                    return homework_data
                else:
                    logger.debug(f"[MASHOV] No valid cache for user {user_id}")
                    return None
        except Exception as e:
            logger.error(f"[MASHOV] Failed to retrieve cached homework: {e}")
            return None
