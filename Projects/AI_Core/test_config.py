import os
import sys

from pathlib import Path
SRC_DIR = Path('/Users/igorgoncharenko/Documents/Unified_System_Core/Projects/AI_Core/src')
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from config_manager import ConfigManager

conf = ConfigManager()
print("Gemini:", conf.get("GEMINI_API_KEY")[:8] + "..." if conf.get("GEMINI_API_KEY") else "None")
print("OpenRouter:", conf.get("OPENROUTER_API_KEY")[:8] + "..." if conf.get("OPENROUTER_API_KEY") else "None")
print("GitHub Models:", conf.get("GITHUB_MODELS_API_KEY")[:8] + "..." if conf.get("GITHUB_MODELS_API_KEY") else "None")
print("Project ID:", os.environ.get("PROJECT_ID"))
