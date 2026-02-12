import os
import logging
import psycopg2
from psycopg2.extras import Json

logger = logging.getLogger(__name__)

class KnowledgeBase:
    """
    Centralized Knowledge Base for AI Agents.
    Stores agent memories, project states, and architectural context.
    """
    def __init__(self, db_url=None):
        default_url = (
            "postgresql://trading_user:trading_pass"
            "@timescaledb.trading:5432/trading"
        )
        self.db_url = db_url or os.getenv("DATABASE_URL", default_url)
        self.conn = None

    def connect(self):
        """Establish connection to PostgreSQL/TimescaleDB."""
        if not self.conn or self.conn.closed:
            try:
                self.conn = psycopg2.connect(self.db_url)
                self.conn.autocommit = True
                logger.info("Connected to Knowledge Base (PostgreSQL)")
            except Exception as e:
                logger.error(f"Failed to connect to Knowledge Base: {e}")
                raise

    def init_schema(self):
        """Initialize database tables."""
        self.connect()
        with self.conn.cursor() as cur:
            # Table for agent experiences and learnings
            cur.execute("""
                CREATE TABLE IF NOT EXISTS agent_memories (
                    id SERIAL PRIMARY KEY,
                    agent_name TEXT NOT NULL,
                    memory_type TEXT DEFAULT 'general',
                    content JSONB NOT NULL,
                    importance INTEGER DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            # Table for tracking project-wide state and progress
            cur.execute("""
                CREATE TABLE IF NOT EXISTS project_status (
                    project_id TEXT PRIMARY KEY,
                    current_milestone TEXT,
                    health_status TEXT DEFAULT 'OK',
                    metadata JSONB DEFAULT '{}',
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            # Create indexes for performance
            cur.execute(
                "CREATE INDEX IF NOT EXISTS idx_memories_agent "
                "ON agent_memories(agent_name);"
            )
            cur.execute(
                "CREATE INDEX IF NOT EXISTS idx_memories_type "
                "ON agent_memories(memory_type);"
            )
            logger.info("Knowledge Base schema initialized.")

    def add_memory(self, agent_name, content, memory_type='general', importance=1):
        """Store a new piece of information."""
        self.connect()
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO agent_memories "
                    "(agent_name, memory_type, content, importance) "
                    "VALUES (%s, %s, %s, %s)",
                    (agent_name, memory_type, Json(content), importance)
                )
        except Exception as e:
            logger.error(f"Failed to add memory: {e}")

    def get_memories(self, agent_name=None, memory_type=None, limit=20):
        """Retrieve memories based on filters."""
        self.connect()
        try:
            with self.conn.cursor() as cur:
                query = (
                    "SELECT agent_name, memory_type, content, importance, "
                    "created_at FROM agent_memories"
                )
                params = []
                where_clauses = []
                
                if agent_name:
                    where_clauses.append("agent_name = %s")
                    params.append(agent_name)
                if memory_type:
                    where_clauses.append("memory_type = %s")
                    params.append(memory_type)
                
                if where_clauses:
                    query += " WHERE " + " AND ".join(where_clauses)
                
                query += " ORDER BY created_at DESC LIMIT %s"
                params.append(limit)
                
                cur.execute(query, params)
                return cur.fetchall()
        except Exception as e:
            logger.error(f"Failed to retrieve memories: {e}")
            return []

    def update_project_status(
        self, 
        project_id, 
        milestone, 
        health='OK', 
        meta=None
    ):
        """Update the status of a specific project."""
        self.connect()
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO project_status 
                    (project_id, current_milestone, health_status, metadata)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (project_id) DO UPDATE SET 
                        current_milestone = EXCLUDED.current_milestone,
                        health_status = EXCLUDED.health_status,
                        metadata = EXCLUDED.metadata,
                        updated_at = CURRENT_TIMESTAMP
                """, (project_id, milestone, health, Json(meta or {})))
        except Exception as e:
            logger.error(f"Failed to update project status: {e}")

if __name__ == "__main__":
    # Test/Initialize
    logging.basicConfig(level=logging.INFO)
    kb = KnowledgeBase()
    try:
        kb.init_schema()
        kb.update_project_status(
            "Unified_System_Core", 
            "Knowledge Base Implementation", 
            "OK", 
            {"version": "3.0"}
        )
        print("Knowledge Base initialized and tested.")
    except Exception as e:
        print(f"Initialization failed: {e}")
