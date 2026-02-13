
import sqlite3
from pathlib import Path

DB_PATH = Path(
    "/Users/igorgoncharenko/Documents/Unified_System_Core/Context/tracking.db"
)

def init_db():
    """Initialize the tracking database."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Task logging table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS agent_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            task_name TEXT,
            status TEXT,
            details TEXT,
            model TEXT
        )
    ''')

    # State tracking
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS system_state (
            key TEXT PRIMARY KEY,
            value TEXT,
            last_updated DATETIME
        )
    ''')

    conn.commit()
    conn.close()

def log_task(task_name, status, details="", model="Antigravity-v1"):
    """Log a task execution."""
    if not DB_PATH.exists():
        init_db()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO agent_log (task_name, status, details, model) VALUES (?, ?, ?, ?)",
        (task_name, status, details, model)
    )
    conn.commit()
    conn.close()
    print(f"📊 [DATABASE LOG] Task '{task_name}' status: {status}")

if __name__ == "__main__":
    init_db()
    log_task("DB Initialization", "Success", "Unified Tracking DB created in Context/")
