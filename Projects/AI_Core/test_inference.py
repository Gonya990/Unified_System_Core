import asyncio
import sys
from pathlib import Path
SRC_DIR = Path('/Users/igorgoncharenko/Documents/Unified_System_Core/Projects/AI_Core/src')
sys.path.insert(0, str(SRC_DIR))
from config_manager import ConfigManager
from inference_client import InferenceClient

async def main():
    cm = ConfigManager()
    client = InferenceClient(cm)
    print("Testing OpenRouter...")
    response = await client.chat([{"role": "user", "content": "Say 'hello world'"}])
    print(f"Response: {response}")

if __name__ == "__main__":
    asyncio.run(main())
