import asyncio
import base64
import logging
import os
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

# Setup basic logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("DeepIndexer")

# Paths
CORE_PATH = Path("/home/gonya/Unified_System_Core")
AI_CORE_PATH = CORE_PATH / "Projects" / "AI_Core"
DB_PATH = AI_CORE_PATH / "knowledge_base.db"

# Add AI_Core/src to path for imports
sys.path.append(str(AI_CORE_PATH / "src"))

try:
    from config_manager import ConfigManager
    from inference_client import InferenceClient
except ImportError as e:
    logger.error(f"Failed to import core modules: {e}")
    sys.exit(1)

# Configuration
SCAN_TARGETS = [
    "/mnt/g/VSCode",
    "/mnt/g/OneDrive",
    "/mnt/h/RECOVERY_FULL_UNPACKED",
    "/home/gonya/meta_archives",
    "/home/gonya/google_archives",
]

# Supported extensions
TEXT_EXTS = {".txt", ".md", ".py", ".js", ".json", ".yaml", ".yml", ".html", ".css", ".sh"}
IGNORE_DIRS = {".git", ".venv", "node_modules", "__pycache__", ".cache"}


class DeepIndexer:
    def __init__(self):
        self.config = ConfigManager()
        # InferenceClient initializes its own swarm
        self.client = InferenceClient(config=self.config)
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS assets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    path TEXT UNIQUE,
                    filename TEXT,
                    extension TEXT,
                    size_mb REAL,
                    mtime TEXT,
                    category TEXT,
                    concept_summary TEXT,
                    metadata_json TEXT,
                    last_indexed TEXT
                )
            """)
            # Full Text Search table
            conn.execute("""
                CREATE VIRTUAL TABLE IF NOT EXISTS assets_fts USING fts5(
                    path, filename, concept_summary, content='assets', content_rowid='id'
                )
            """)
            # Trigger to update FTS
            conn.execute("""
                CREATE TRIGGER IF NOT EXISTS assets_ai AFTER INSERT ON assets BEGIN
                    INSERT INTO assets_fts(rowid, path, filename, concept_summary)
                    VALUES (new.id, new.path, new.filename, new.concept_summary);
                END;
            """)

    async def scan_folders(self):
        logger.info("🚀 Starting deep scan of folders...")
        total_discovered = 0

        for target in SCAN_TARGETS:
            if not os.path.exists(target):
                logger.warning(f"Target not found: {target}")
                continue

            logger.info(f"📂 Scanning {target}...")
            for root, dirs, files in os.walk(target):
                dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

                batch = []
                for f in files:
                    full_path = str(Path(root) / f)
                    ext = os.path.splitext(f)[1].lower()

                    try:
                        stat = os.stat(full_path)
                        mtime = datetime.fromtimestamp(stat.st_mtime).isoformat()
                        size_mb = stat.st_size / (1024 * 1024)

                        category = "other"
                        if ext in TEXT_EXTS:
                            category = "text"
                        elif ext in {".jpg", ".png", ".jpeg", ".gif"}:
                            category = "image"
                        elif ext in {".mp4", ".mov", ".avi"}:
                            category = "video"
                        elif ext in {".pdf", ".docx"}:
                            category = "doc"

                        batch.append((full_path, f, ext, size_mb, mtime, category, datetime.now().isoformat()))
                    except Exception:
                        continue

                if batch:
                    with sqlite3.connect(DB_PATH) as conn:
                        conn.executemany(
                            """
                            INSERT OR IGNORE INTO assets (path, filename, extension, size_mb, mtime, category, last_indexed)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                        """,
                            batch,
                        )
                    total_discovered += len(batch)

        logger.info(f"✅ Discovery complete. Total files in DB: {total_discovered}")

    async def summarize_asset(self, asset_id, path, category, size_mb):
        """Use AI to summarize a single asset."""
        try:
            if category == "text":
                with open(path, encoding="utf-8", errors="ignore") as f:
                    content = f.read(4000)  # First 4k chars

                if not content.strip():
                    return True

                prompt = f"Analyze this file and provide a 1-sentence summary of its content and 3 key tags. Path: {path}\nContent snippet: {content[:2000]}"
                summary, _ = await self.client.chat(
                    [{"role": "user", "content": prompt}],
                    system_prompt="You are a high-speed knowledge indexer for the Unified System. Be concise and technical.",
                )

                if summary:
                    with sqlite3.connect(DB_PATH) as conn:
                        conn.execute("UPDATE assets SET concept_summary = ? WHERE id = ?", (summary, asset_id))
                        # Refresh FTS
                        conn.execute(
                            "INSERT OR REPLACE INTO assets_fts(rowid, path, filename, concept_summary) SELECT id, path, filename, concept_summary FROM assets WHERE id = ?",
                            (asset_id,),
                        )
                    return True
            elif category == "image" and size_mb < 5:
                try:
                    with open(path, "rb") as f:
                        img_data = base64.b64encode(f.read()).decode()
                    prompt = "What is in this image? Provide a 1-sentence description and 3 tags."
                    summary, _ = await self.client.chat(
                        [{"role": "user", "content": prompt, "images": [img_data]}],
                        system_prompt="You are a high-speed vision indexer for the Unified System.",
                    )
                    if summary:
                        with sqlite3.connect(DB_PATH) as conn:
                            conn.execute("UPDATE assets SET concept_summary = ? WHERE id = ?", (summary, asset_id))
                            conn.execute(
                                "INSERT OR REPLACE INTO assets_fts(rowid, path, filename, concept_summary) SELECT id, path, filename, concept_summary FROM assets WHERE id = ?",
                                (asset_id,),
                            )
                        return True
                except Exception:
                    pass
        except Exception as e:
            logger.debug(f"Failed to summarize {path}: {e}")
        return False

    async def process_queue(self):
        """Process files needing AI summary in parallel batches."""
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.execute("""
                SELECT id, path, category, size_mb FROM assets
                WHERE concept_summary IS NULL
                AND category IN ('text', 'doc', 'image')
                ORDER BY category DESC
                LIMIT 50000
            """)
            queue = cursor.fetchall()

        if not queue:
            logger.info("No new assets to process.")
            return

        logger.info(f"🧠 Processing {len(queue)} assets with the GPU Council (Full Gas Edition)...")

        # Parallel processing
        batch_size = 50
        for i in range(0, len(queue), batch_size):
            batch = queue[i : i + batch_size]
            tasks = [self.summarize_asset(aid, path, cat, size) for aid, path, cat, size in batch]
            await asyncio.gather(*tasks)
            if (i // batch_size) % 10 == 0:
                logger.info(f"Progress: {i + len(batch)}/{len(queue)}")
            await asyncio.sleep(0.1)


async def main():
    indexer = DeepIndexer()
    await indexer.scan_folders()
    await indexer.process_queue()


if __name__ == "__main__":
    asyncio.run(main())
