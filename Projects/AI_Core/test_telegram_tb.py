import sys
from pathlib import Path
SRC_DIR = Path('/Users/igorgoncharenko/Documents/Unified_System_Core/Projects/AI_Core/src')
sys.path.insert(0, str(SRC_DIR))
from token_broker import TokenBroker

tb = TokenBroker()
print(f"Telegram Bot Token from TokenBroker TELEGRAM: {tb.get_key('TELEGRAM')}")
