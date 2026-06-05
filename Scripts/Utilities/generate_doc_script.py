import asyncio
import logging
import os
import sys

# Add paths for Council
root_dir = "/Users/igorgoncharenko/Documents/Unified_System_Core"
sys.path.insert(0, os.path.join(root_dir, "LLM_Council"))
sys.path.insert(0, os.path.join(root_dir, "Projects/AI_Core/src"))

from council.council import LLMCouncil
from council.providers.openai_provider import OpenAIProvider
from token_broker import TokenBroker

logging.basicConfig(level=logging.INFO)

async def generate_15min_script():
    broker = TokenBroker()

    # Setup providers manually to ensure they have keys
    openai_key = broker.get_key("openai")
    broker.get_key("gemini")

    council = LLMCouncil(providers=[])

    if openai_key:
        council.providers.append(OpenAIProvider(api_key=openai_key, model="gpt-4o"))
    else:
        print("❌ No OpenAI key found!")
        return

    prompt = """
Write a 3000-word (15-minute) documentary script entitled "Unified System Core: The Architecture of Autonomous Sovereignty (2026)".
The script is for a deep, professional male voice (timbre of an experienced narrator).
Structure:
1. INTRO: The shift from AI as a tool to AI as an autonomous core.
2. HARDWARE SOVEREIGNTY: GKE, Proxmox, and the Windows Gaming node (The GPU Power).
3. THE BRAIN: The LLM Council and the deliberation process for critical decisions.
4. VIBRANIUM SHIELD: Personality protection, Human-in-the-Loop, and security in the age of Agentic AI.
5. WEALTH ENGINE: Autonomous trading with Bybit and the $50 real-world challenge.
6. CONCLUSION: The roadmap for 2026 and beyond.

Ensure the text is deep, research-based, and uses specific technical details mentioned in the provided context (Unified System Core, GKE, TokenBroker, Vibranium Shield).
"""

    print("🚀 Generating script...")
    session = await council.deliberate(prompt)

    if not session or not session.final_report:
        print("❌ Error: No report generated!")
        return

    report_path = os.path.join(root_dir, "Reports", "DOCUMENTARY_SCRIPT_2026.md")
    print(f"DEBUG: Target path is {report_path}")
    try:
        with open(report_path, "w") as f:
            f.write(session.final_report)
        print(f"✅ Script saved to {report_path}")
        print(f"DEBUG: File size: {os.path.getsize(report_path)} bytes")
    except Exception as e:
        print(f"❌ Failed to save file: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(generate_15min_script())
    except Exception as e:
        print(f"💥 Fatal error: {e}")
