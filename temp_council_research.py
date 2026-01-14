import asyncio
import os
import sys

# Add project root to path
sys.path.append(os.getcwd())

from LLM_Council.council.council import LLMCouncil
from Scripts.Utilities.token_broker import TokenBroker


async def main():
    print("🧠 Council Convening: Researching XTTS Voice Cloning Best Practices...")

    # Initialize Broker and Council
    broker = TokenBroker()
    council = LLMCouncil.from_token_broker(broker)

    topic = "Provide a concise, step-by-step technical guide for creating high-quality reference audio for Coqui XTTS v2 voice cloning. Focus on: 1. Audio format (wav/mp3, sample rate). 2. Ideal length (seconds). 3. Recording environment and noise floor. 4. Speaking style for best cloning. Format as a markdown list."

    # Run Deliberation
    result = await council.deliberate(topic)
    print("\n--- COUNCIL FINDINGS ---\n")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
