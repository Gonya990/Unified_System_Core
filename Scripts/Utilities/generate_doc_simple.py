import asyncio
import sys

from openai import AsyncOpenAI

# Add paths for TokenBroker
sys.path.insert(0, "/Users/igorgoncharenko/Documents/Unified_System_Core/Projects/AI_Core/src")
from token_broker import TokenBroker


async def generate_script():
    broker = TokenBroker()
    key = broker.get_key("openai")
    if not key:
        print("❌ No key")
        return

    client = AsyncOpenAI(api_key=key)

    prompt = """
Write a 3000-word documentary script "Unified System Core (2026)". 
Deep male narrator voice. Professional, technical, visionary.
Must cover: Architecture (GKE/Proxmox), Council (Multi-LLM), Security (Vibranium Shield), Wealth (Bybit $50).
"""

    print("🚀 Calling OpenAI...")
    try:
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=4000
        )
        content = response.choices[0].message.content

        path = "/Users/igorgoncharenko/Documents/Unified_System_Core/Reports/DOCUMENTARY_SCRIPT_2026.md"
        with open(path, "w") as f:
            f.write(content)
        print(f"✅ Saved to {path} ({len(content)} chars)")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(generate_script())
