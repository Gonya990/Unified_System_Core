#!/usr/bin/env python3
import sys
from pathlib import Path

# Add current dir and src to path
# Factory path structure: projects/content_factory
current_dir = Path(__file__).resolve().parent
src_dir = current_dir / "src"

sys.path.append(str(current_dir))
sys.path.append(str(src_dir))

# Import the factory scheduler content or just execute it
try:
    from pipeline.factory_scheduler import run_factory_production, start_scheduler
except ImportError as e:
    print(f"Error importing factory_scheduler: {e}")
    print(f"Sys Path: {sys.path}")
    sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--daily":
         run_factory_production(mode="daily")
    else:
         start_scheduler()
