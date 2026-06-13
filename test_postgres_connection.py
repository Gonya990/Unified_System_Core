import asyncio
import os
import sys
import asyncpg

# Try to use .env if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

async def test_connection():
    # If running locally on Mac, connect to igor-gaming, else use db hostname
    host = os.environ.get("DB_HOST", "igor-gaming")
    user = os.environ.get("POSTGRES_USER", "postgres")
    password = os.environ.get("DATABASE_PASSWORD", "unified_password")
    db_name = os.environ.get("POSTGRES_DB", "knowledge_graph")
    
    dsn = f"postgresql://{user}:{password}@{host}:5432/{db_name}"
    print(f"Testing connection to: {dsn.replace(password, '***')}")
    
    try:
        conn = await asyncpg.connect(dsn)
        version = await conn.fetchval('SELECT version()')
        print(f"✅ Connection successful!")
        print(f"PostgreSQL Version: {version}")
        
        # Test pgvector extension
        try:
            await conn.execute("CREATE EXTENSION IF NOT EXISTS vector")
            print("✅ pgvector extension is available and created/verified.")
        except Exception as e:
            print(f"⚠️ Could not create pgvector extension. Make sure the pgvector image is used: {e}")

        await conn.close()
        return True
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_connection())
    if not success:
        sys.exit(1)
