import os
import sys
import asyncio
from openai import AsyncOpenAI

# Add paths for TokenBroker
sys.path.insert(0, "/Users/igorgoncharenko/Documents/Unified_System_Core/Projects/AI_Core/src")
from token_broker import TokenBroker

async def translate_script():
    broker = TokenBroker()
    key = broker.get_key("openai")
    client = AsyncOpenAI(api_key=key)
    
    script_path = "/Users/igorgoncharenko/Documents/Unified_System_Core/Reports/DOCUMENTARY_SCRIPT_2026.md"
    with open(script_path, "r") as f:
        en_script = f.read()
    
    prompt = f"""
Translate the following documentary script into Russian. 
Maintain the EXACT SAME structure, scene markers [Scene: ...], and narrator markers [NARRATOR SPEAKS].
The tone must be deep, professional, and suitable for a narrator (deep male voice). 
Avoid bureaucratic or overly formal language; keep it visionary and technical.

Script:
{en_script}
"""

    print("🚀 Translating script to Russian...")
    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=4000
    )
    ru_script = response.choices[0].message.content
    
    ru_path = "/Users/igorgoncharenko/Documents/Unified_System_Core/Reports/DOCUMENTARY_SCRIPT_2026_RU.md"
    with open(ru_path, "w") as f:
        f.write(ru_script)
    print(f"✅ Russian script saved to {ru_path}")

if __name__ == "__main__":
    asyncio.run(translate_script())
