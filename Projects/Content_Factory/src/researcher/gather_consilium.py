import asyncio
import os
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

# Setup paths to include AI_Core and Content_Factory
SCRIPT_DIR = Path(__file__).parent.resolve()
ROOT_DIR = SCRIPT_DIR.parent.parent.parent.parent  # researcher -> src -> Content_Factory -> Projects -> ROOT
sys.path.append(str(ROOT_DIR / "Projects/AI_Core/src"))
sys.path.append(str(ROOT_DIR / "Projects/Content_Factory/src/researcher"))

load_dotenv(ROOT_DIR / ".env")

from agent_orchestrator import AgentOrchestrator
from config_manager import ConfigManager
from inference_client import InferenceClient


async def gather_consilium():
    print("🛸 CONCILIUM GATHERING: Initiating Full Gas Content Factory (GitHub VIBRANIUM Engine)...")

    config = ConfigManager()
    config._config["INFERENCE_PROVIDER"] = "github"
    config._config["GITHUB_TOKEN"] = os.getenv("GITHUB_TOKEN")
    config._config["GITHUB_MODEL"] = "gpt-4o"

    inference = InferenceClient(config)
    orchestrator = AgentOrchestrator(inference)

    research_tasks = [
        ("api-discoverer", "Deep research on 2026 WhatsApp Meta API automation features."),
        ("code-explorer", "RTX 4090 multi-agent performance optimization guide."),
        ("code-architect", "Structural plan for Sovereign AI infrastructure (Mac/Win/Linux)."),
        ("senior-ui-ux-designer", "UI/UX specs for Glassmorphism Dashboard for AI Management."),
        ("security-hardening-worker", "Securing USDT/Crypto gateways for Telegram automation."),
        ("performance-optimizer", "Python Async concurrency benchmarks for 17+ agents."),
        ("implementer", "FastAPI + Make.com lead processing module code."),
        ("bug-fixer", "Resolving distributed bot cluster sync issues."),
        ("code-reviewer", "Auditing for Vibranium System Core standards."),
        ("tdd-cycle-driver", "TDD suite for WhatsApp lead sentiment analysis."),
        ("hexagonal-architecture-guardian", "Clean Architecture validation for the Bridge module."),
        ("performance-optimization-worker", "Tailscale networking latency optimization."),
        ("code-quality-coordinator", "Standardizing UI/UX tokens for the Gonya brand."),
        ("devops-workflow-orchestrator", "Cross-platform deployment automation scripts."),
        ("feedback-loop-optimizer", "AI self-correcting mechanisms from WhatsApp user interactions."),
        ("github-workflow", "CI/CD setup with automated verification for Core repo."),
        ("dependency-mapper", "Mapping the Unified System ecosystem graph.")
    ]

    print(f"👥 Gathering {len(research_tasks)} agents. Using BATCHING to respect rate limits...")

    results = {}
    batch_size = 2
    for i in range(0, len(research_tasks), batch_size):
        batch = research_tasks[i:i + batch_size]
        print(f"📦 Processing Batch {i//batch_size + 1}/{len(research_tasks)//batch_size + 1}: {', '.join([a for a, _ in batch])}")

        batch_results = await orchestrator.run_parallel(batch, context="Unified System Core 2026. High Aesthetics, Speed, Sovereignty.")
        results.update(batch_results)

        if i + batch_size < len(research_tasks):
            print("⏳ Cooling down for 10 seconds to avoid GitHub Rate Limits...")
            await asyncio.sleep(10)

    print("📜 Consolidating Consilium Insights...")
    consilium_report = "# 🎓 CONSILIUM REPORT: Full Gas Innovation (Vibranium Engine)\n"
    consilium_report += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    consilium_report += orchestrator.format_results(results, mode="detailed")

    timestamp = datetime.now().strftime('%Y%n%d_%H%M%S')
    report_path = ROOT_DIR / f"Projects/Content_Factory/outputs/consilium_report_{timestamp}.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(consilium_report)

    print(f"✅ Consilium Research Complete! Report saved to: {report_path}")

if __name__ == "__main__":
    asyncio.run(gather_consilium())
