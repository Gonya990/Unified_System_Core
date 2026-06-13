import asyncio
import logging
import os

import asyncpg

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("KnowledgeGraphManager")

class KnowledgeGraphManager:
    def __init__(self):
        self.host = os.environ.get("DB_HOST", "igor-gaming")
        self.user = os.environ.get("POSTGRES_USER", "postgres")
        self.password = os.environ.get("DATABASE_PASSWORD", "unified_password")
        self.db_name = os.environ.get("POSTGRES_DB", "knowledge_graph")
        self.dsn = f"postgresql://{self.user}:{self.password}@{self.host}:5432/{self.db_name}"
        self.pool = None

    async def connect(self):
        if not self.pool:
            logger.info("Connecting to Knowledge Graph DB...")
            self.pool = await asyncpg.create_pool(self.dsn)
            logger.info("Connected.")

    async def close(self):
        if self.pool:
            await self.pool.close()
            self.pool = None

    async def initialize_schema(self):
        """Initializes the database schema including pgvector for embeddings."""
        await self.connect()
        async with self.pool.acquire() as conn:
            # Ensure pgvector is enabled
            await conn.execute("CREATE EXTENSION IF NOT EXISTS vector;")

            # Create core tables
            # Entities (Projects, Agents, Concepts)
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS entities (
                    id SERIAL PRIMARY KEY,
                    uuid UUID DEFAULT gen_random_uuid() UNIQUE,
                    name VARCHAR(255) NOT NULL,
                    type VARCHAR(50) NOT NULL,
                    metadata JSONB DEFAULT '{}',
                    embedding VECTOR(768), -- Vertex AI text-embedding model size
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                );
            """)

            # Relationships
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS relationships (
                    id SERIAL PRIMARY KEY,
                    source_uuid UUID REFERENCES entities(uuid) ON DELETE CASCADE,
                    target_uuid UUID REFERENCES entities(uuid) ON DELETE CASCADE,
                    relationship_type VARCHAR(100) NOT NULL,
                    properties JSONB DEFAULT '{}',
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE (source_uuid, target_uuid, relationship_type)
                );
            """)

            # Context/Memory Logs
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS memories (
                    id SERIAL PRIMARY KEY,
                    entity_uuid UUID REFERENCES entities(uuid) ON DELETE SET NULL,
                    content TEXT NOT NULL,
                    context JSONB DEFAULT '{}',
                    embedding VECTOR(768),
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                );
            """)

            # Create vector indices for similarity search
            await conn.execute("""
                CREATE INDEX IF NOT EXISTS entities_embedding_idx ON entities USING hnsw (embedding vector_l2_ops);
                CREATE INDEX IF NOT EXISTS memories_embedding_idx ON memories USING hnsw (embedding vector_l2_ops);
            """)

            logger.info("Database schema initialized successfully.")

if __name__ == "__main__":
    async def run_init():
        manager = KnowledgeGraphManager()
        await manager.initialize_schema()
        await manager.close()

    asyncio.run(run_init())
