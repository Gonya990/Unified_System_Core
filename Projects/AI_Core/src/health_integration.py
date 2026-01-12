"""
Health Integration Module
Receives health data (steps, weight, sleep) via Webhook.
Intended to be used with iOS Shortcuts or Android Automation.
"""
import logging
import sqlite3
from datetime import datetime
from typing import Dict

logger = logging.getLogger(__name__)

class HealthIntegration:
    """Manages health data storage and retrieval."""

    def __init__(self, db_path: str = "health.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialize SQLite database for health metrics."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        # Metrics table
        c.execute('''
            CREATE TABLE IF NOT EXISTS metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                metric_type TEXT,  -- steps, weight, sleep_hours, calories
                value REAL,
                unit TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                source TEXT        -- ios, android, manual
            )
        ''')

        # User goals table
        c.execute('''
            CREATE TABLE IF NOT EXISTS goals (
                user_id INTEGER PRIMARY KEY,
                steps_goal INTEGER DEFAULT 10000,
                weight_goal REAL,
                sleep_goal REAL DEFAULT 8.0
            )
        ''')

        conn.commit()
        conn.close()

    def add_metric(self, user_id: int, metric_type: str, value: float, unit: str, source: str = "manual"):
        """Record a new metric."""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute(
                "INSERT INTO metrics (user_id, metric_type, value, unit, source) VALUES (?, ?, ?, ?, ?)",
                (user_id, metric_type, value, unit, source)
            )
            conn.commit()
            conn.close()
            logger.info(f"Recorded {metric_type}: {value} for user {user_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to record metric: {e}")
            return False

    def get_today_stats(self, user_id: int) -> Dict[str, float]:
        """Get aggregate stats for today."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        stats = {}
        today_start = datetime.now().strftime("%Y-%m-%d 00:00:00")

        # Steps (Sum)
        c.execute("SELECT SUM(value) FROM metrics WHERE user_id=? AND metric_type='steps' AND timestamp >= ?", (user_id, today_start))
        res = c.fetchone()
        stats['steps'] = res[0] if res[0] else 0

        # Sleep (Last entry or Sum? Usually Sum if multiple naps, but let's assume Sum)
        c.execute("SELECT SUM(value) FROM metrics WHERE user_id=? AND metric_type='sleep_hours' AND timestamp >= ?", (user_id, today_start))
        res = c.fetchone()
        stats['sleep'] = res[0] if res[0] else 0

        # Weight (Last entry)
        c.execute("SELECT value FROM metrics WHERE user_id=? AND metric_type='weight' ORDER BY timestamp DESC LIMIT 1", (user_id,))
        res = c.fetchone()
        stats['weight'] = res[0] if res else 0

        conn.close()
        return stats

    def get_weekly_stats(self, user_id: int) -> Dict[str, float]:
        """Get average stats for the last 7 days."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        stats = {}
        week_start = datetime.now().strftime("%Y-%m-%d 00:00:00") # Simplified, actually needs -7 days logic, handled below

        # Avg Steps
        c.execute("SELECT AVG(daily_steps) FROM (SELECT SUM(value) as daily_steps FROM metrics WHERE user_id=? AND metric_type='steps' AND timestamp >= date('now', '-7 days') GROUP BY date(timestamp))", (user_id,))
        res = c.fetchone()
        stats['avg_steps'] = res[0] if res[0] else 0

        conn.close()
        return stats

    def set_goal(self, user_id: int, metric: str, value: float):
        """Set a goal."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        # Check if exists
        c.execute("SELECT user_id FROM goals WHERE user_id=?", (user_id,))
        if not c.fetchone():
            c.execute("INSERT INTO goals (user_id) VALUES (?)", (user_id,))

        if metric == 'steps':
            c.execute("UPDATE goals SET steps_goal=? WHERE user_id=?", (value, user_id))
        elif metric == 'weight':
            c.execute("UPDATE goals SET weight_goal=? WHERE user_id=?", (value, user_id))
        elif metric == 'sleep':
            c.execute("UPDATE goals SET sleep_goal=? WHERE user_id=?", (value, user_id))

        conn.commit()
        conn.close()
