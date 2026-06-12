import os
import sys

from pathlib import Path
SRC_DIR = Path('/Users/igorgoncharenko/Documents/Unified_System_Core/Projects/AI_Core/src')
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from token_broker import TokenBroker
from dotenv import load_dotenv

broker = TokenBroker()
print("Vault Keys:")
for provider, keys in broker.key_store.items():
    if isinstance(keys, list):
        for k in keys:
            val = k.get("key", "")
            print(f"{provider}: {val[:8]}...{val[-4:]}")

load_dotenv('/Users/igorgoncharenko/Documents/Unified_System_Core/Projects/AI_Core/.env')
print("\nENV Keys:")
print("GEMINI:", os.getenv("GEMINI_API_KEY", "")[:8] + "..." + os.getenv("GEMINI_API_KEY", "")[-4:])
print("OPENAI:", os.getenv("OPENAI_API_KEY", "")[:8] + "..." + os.getenv("OPENAI_API_KEY", "")[-4:])
print("OPENROUTER:", os.getenv("OPENROUTER_API_KEY", "")[:8] + "..." + os.getenv("OPENROUTER_API_KEY", "")[-4:])

