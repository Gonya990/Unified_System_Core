import sys
from pathlib import Path
SRC_DIR = Path('/Users/igorgoncharenko/Documents/Unified_System_Core/Projects/AI_Core/src')
sys.path.insert(0, str(SRC_DIR))
from config_manager import ConfigManager

cm = ConfigManager()
print(f"OpenRouter: {cm.get('OPENROUTER_API_KEY')[:15]}...")
print(f"Gemini: {cm.get('GEMINI_API_KEY')[:15]}...")
