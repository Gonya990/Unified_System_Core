import asyncio
import sys
from pathlib import Path

# Setup paths
PROJECT_ROOT = Path(__file__).parent.parent.parent.resolve()
sys.path.append(str(PROJECT_ROOT / "Scripts/Utilities"))
sys.path.append(str(PROJECT_ROOT / "LLM_Council"))

from council.council import LLMCouncil
from token_broker import TokenBroker


async def council_brev_audit():
    print("🧠 COUNCIL: Starting Deep Research on NVIDIA Brev Zero-Cost Infrastructure...")

    try:
        broker = TokenBroker()
        council = LLMCouncil.from_token_broker(broker)
    except Exception as e:
        print(f"❌ Failed to initialize Council with TokenBroker: {e}")
        return

    query = """
    Perform an in-depth research on NVIDIA Brev (brev.dev).

    FOCUS:
    1. Identify exact 'Zero-Cost' (Free Tier) services available right now.
    2. Are there complementary GPU credits for new developers?
    3. How can we use Brev to host NVIDIA NIM for free or at minimum cost?
    4. Compare Brev with regular NVIDIA NIM API usage.

    Deliver a structured report in Markdown.
    """

    try:
        session = await council.deliberate(query)
        report = session.stage3_consensus

        report_path = PROJECT_ROOT / "Projects/Business_Intelligence/brev_audit.md"
        report_path.parent.mkdir(parents=True, exist_ok=True)

        with open(report_path, "w", encoding="utf-8") as f:
            f.write("# COUNCIL REPORT: NVIDIA Brev Infrastructure Audit\n\n")
            f.write(report)

        print(f"✅ Audit complete. Report saved to: {report_path}")

    except Exception as e:
        print(f"❌ Council audit failed: {e}")
    finally:
        await council.close()


if __name__ == "__main__":
    asyncio.run(council_brev_audit())
