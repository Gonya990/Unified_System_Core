import asyncio
import sys
from pathlib import Path

# Setup paths
ROOT_DIR = Path(__file__).parent.parent.parent.resolve()
sys.path.append(str(ROOT_DIR / "LLM_Council"))
sys.path.append(str(ROOT_DIR / "Scripts/Utilities"))

from council.council import LLMCouncil
from token_broker import TokenBroker


def conduct_market_research(topic: str):
    print(f"🕵️ Starting Market Research on: {topic}")

    broker = TokenBroker()
    # Forces NVIDIA NIM or local models to avoid OpenAI quota issues mentioned by user
    council = LLMCouncil.from_token_broker(broker)

    research_query = f"""
    Conduct a deep market analysis for a project involving: {topic}
    Specifically for Kickstarter and early-stage VC investors.

    Focus on:
    1. Market Size (AI Video Production 2024-2026)
    2. Competitor analysis (Synthesia, HeyGen, Sora-based startups)
    3. Potential for Kickstarter (Success stories of AI content tools)
    4. Monetization strategy for a "Long-Form AI Documentary Factory"

    Format the output as a professional Business Report in Russian.
    """

    session = asyncio.run(council.deliberate(research_query, verbose=True))
    report = session.stage3_consensus

    output_path = Path(__file__).parent / "Market_Research/AI_Documentary_Market_Report.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"✅ Market Research Report generated: {output_path}")
    return report


if __name__ == "__main__":
    conduct_market_research("Autonomous AI Documentary Production & Content Factory")
