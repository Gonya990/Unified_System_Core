"""
Usage Tracker for AI Telegram Bot.
Tracks token usage per user, provider, and model using SQLite.
"""
import sqlite3
import logging
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)

class UsageTracker:
    def __init__(self, db_path: str = "usage.db"):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Initialize SQLite database and tables."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS token_usage (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        user_id INTEGER,
                        username TEXT,
                        provider TEXT,
                        model TEXT,
                        prompt_tokens INTEGER,
                        completion_tokens INTEGER,
                        total_tokens INTEGER
                    )
                """)
                conn.commit()
                logger.info(f"Usage database initialized at {self.db_path}")
        except Exception as e:
            logger.error(f"Failed to init usage DB: {e}")

    def log_usage(self, user_id: int, username: str, provider: str, model: str, usage_stats: dict):
        """Log token usage for a request."""
        if not usage_stats or usage_stats.get("total_tokens", 0) == 0:
            return

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO token_usage 
                    (user_id, username, provider, model, prompt_tokens, completion_tokens, total_tokens)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    user_id,
                    username,
                    provider,
                    model,
                    usage_stats.get("prompt_tokens", 0),
                    usage_stats.get("completion_tokens", 0),
                    usage_stats.get("total_tokens", 0)
                ))
                conn.commit()
        except Exception as e:
            logger.error(f"Failed to log usage: {e}")

    def get_user_stats(self, user_id: int, days: int = 30) -> dict:
        """Get usage statistics for a user for the last N days."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                # Total tokens
                cursor.execute("""
                    SELECT 
                        SUM(total_tokens) as total,
                        SUM(prompt_tokens) as prompt,
                        SUM(completion_tokens) as completion,
                        COUNT(*) as requests
                    FROM token_usage
                    WHERE user_id = ? AND timestamp >= date('now', ?)
                """, (user_id, f'-{days} days'))
                
                row = cursor.fetchone()
                if not row or row['total'] is None:
                    return None
                
                stats = {
                    "total_tokens": row['total'],
                    "prompt_tokens": row['prompt'],
                    "completion_tokens": row['completion'],
                    "requests": row['requests'],
                    "by_model": {}
                }
                
                # Breakdown by model
                cursor.execute("""
                    SELECT model, SUM(total_tokens) as tokens
                    FROM token_usage
                    WHERE user_id = ? AND timestamp >= date('now', ?)
                    GROUP BY model
                    ORDER BY tokens DESC
                """, (user_id, f'-{days} days'))
                
                for r in cursor.fetchall():
                    stats["by_model"][r['model']] = r['tokens']
                    
                return stats
        except Exception as e:
            logger.error(f"Failed to get stats: {e}")
            return None

    def get_all_users_stats(self, days: int = 30) -> dict:
        """Get aggregated stats for all users."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT 
                        user_id,
                        username,
                        SUM(total_tokens) as total,
                        COUNT(*) as requests
                    FROM token_usage
                    WHERE timestamp >= date('now', ?)
                    GROUP BY user_id
                    ORDER BY total DESC
                """, (f'-{days} days',))
                
                users = []
                for row in cursor.fetchall():
                    users.append({
                        "user_id": row['user_id'],
                        "username": row['username'],
                        "total_tokens": row['total'],
                        "requests": row['requests']
                    })
                
                return {"users": users}
        except Exception as e:
            logger.error(f"Failed to get all users stats: {e}")
            return {"users": []}

    def get_provider_breakdown(self, days: int = 30) -> dict:
        """Get token usage breakdown by provider."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT 
                        provider,
                        SUM(total_tokens) as total,
                        COUNT(*) as requests
                    FROM token_usage
                    WHERE timestamp >= date('now', ?)
                    GROUP BY provider
                    ORDER BY total DESC
                """, (f'-{days} days',))
                
                providers = {}
                for row in cursor.fetchall():
                    providers[row['provider']] = {
                        "tokens": row['total'],
                        "requests": row['requests']
                    }
                
                return providers
        except Exception as e:
            logger.error(f"Failed to get provider breakdown: {e}")
            return {}

