
import json
import os
from datetime import datetime

# Configuration
ARCHIVE_PATHS = [ "/mnt/g/VSCode/recovery_archive", "/mnt/g/OneDrive", "/mnt/h/RECOVERY_FULL_UNPACKED",
    "/home/gonya/meta_archives",
    "/home/gonya/google_archives",
    "/home/gonya/Documents/Unified_System" # Scan existing docs too
]

OUTPUT_FILE = "/home/gonya/Unified_System_Core/Projects/Content_Factory/config/knowledge_base_index.json"

# Supported Types
TEXT_TYPES = ['.txt', '.md', '.json', '.csv']
DOC_TYPES = ['.pdf', '.docx', '.pptx', '.doc']
MEDIA_TYPES = ['.mp4', '.mov', '.mp3', '.wav', '.jpg', '.png']

IGNORED_DIRS = {'.venv', '.git', 'node_modules', '__pycache__', 'venv', 'env', '.idea', '.vscode'}

def scan_archives():
    print("🕵️‍♂️ Starting Archive Scan...")

    knowledge_index = {
        "documents": [],
        "media_assets": [],
        "conversations": [], # From JSON dumps
        "stats": {
            "total_files": 0,
            "total_size_mb": 0
        }
    }

    for base_path in ARCHIVE_PATHS:
        if not os.path.exists(base_path):
            print(f"⚠️ Path not found (skipping): {base_path}")
            continue

        print(f"📂 Scanning: {base_path}")

        for root, dirs, files in os.walk(base_path):
            # Modify dirs in-place to exclude ignored directories
            dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]

            for file in files:
                try:
                    ext = os.path.splitext(file)[1].lower()
                    full_path = os.path.join(root, file)

                    # Skip if it's a broken link
                    if not os.path.exists(full_path):
                        continue

                    size_mb = os.path.getsize(full_path) / (1024 * 1024)

                    knowledge_index["stats"]["total_files"] += 1
                    knowledge_index["stats"]["total_size_mb"] += size_mb

                    # Categorize
                    item = {
                        "path": full_path,
                        "filename": file,
                        "size_mb": round(size_mb, 2),
                        "source_root": base_path,
                        "timestamp": datetime.fromtimestamp(os.path.getmtime(full_path)).isoformat()
                    }

                    if ext in DOC_TYPES or ext in TEXT_TYPES:
                        knowledge_index["documents"].append(item)
                    elif ext in MEDIA_TYPES:
                        knowledge_index["media_assets"].append(item)

                    # Special handling for JSON exports (Messenger/Insta)
                    if ext == '.json' and ('message' in file or 'chat' in file):
                        knowledge_index["conversations"].append(item)
                except Exception as e:
                    print(f"⚠️ Error processing {file}: {e}")

    # Save Index
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(knowledge_index, f, indent=2)

    print("\n✅ Indexing Complete!")
    print(f"📄 Documents: {len(knowledge_index['documents'])}")
    print(f"🎬 Media Assets: {len(knowledge_index['media_assets'])}")
    print(f"💾 Total Size: {int(knowledge_index['stats']['total_size_mb'])} MB")
    print(f"📂 Stats saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    scan_archives()
