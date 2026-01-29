#!/usr/bin/env python3
"""
🏛️ LLM Council Demo Script

Usage:
    python council_demo.py "Your question here"
    python council_demo.py --interactive
    python council_demo.py --health-check
"""

import asyncio
import logging
import sys

# Rich for beautiful console output
try:
    from rich.console import Console
    from rich.markdown import Markdown
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.table import Table
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    print("Note: Install 'rich' for better console output: pip install rich")

from council import LLMCouncil

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

if RICH_AVAILABLE:
    console = Console()


def print_header():
    """Print welcome header."""
    if RICH_AVAILABLE:
        console.print(Panel.fit(
            "[bold cyan]🏛️ LLM COUNCIL[/bold cyan]\n"
            "[dim]Multi-model deliberation system[/dim]",
            border_style="cyan"
        ))
    else:
        print("\n" + "="*50)
        print("🏛️ LLM COUNCIL")
        print("Multi-model deliberation system")
        print("="*50 + "\n")


def print_stage(stage_num: int, title: str):
    """Print stage header."""
    if RICH_AVAILABLE:
        console.print(f"\n[bold yellow]━━━ STAGE {stage_num}: {title} ━━━[/bold yellow]\n")
    else:
        print(f"\n{'='*10} STAGE {stage_num}: {title} {'='*10}\n")


async def run_health_check():
    """Run health check on all providers."""
    print_header()

    if RICH_AVAILABLE:
        console.print("[bold]Running health check...[/bold]\n")
    else:
        print("Running health check...\n")

    try:
        council = LLMCouncil.from_env()
        results = await council.health_check()

        if RICH_AVAILABLE:
            table = Table(title="Provider Health Status")
            table.add_column("Provider", style="cyan")
            table.add_column("Status", style="green")

            for provider, healthy in results.items():
                status = "✅ OK" if healthy else "❌ Failed"
                table.add_row(provider, status)

            console.print(table)
        else:
            for provider, healthy in results.items():
                status = "✅ OK" if healthy else "❌ Failed"
                print(f"  {provider}: {status}")

        await council.close()

    except ValueError as e:
        print(f"❌ Error: {e}")
        print("Make sure to copy .env.example to .env and add your API keys.")


async def run_query(query: str):
    """Run a single query through the council."""
    print_header()

    if RICH_AVAILABLE:
        console.print(f"[bold]Query:[/bold] {query}\n")
    else:
        print(f"Query: {query}\n")

    try:
        council = LLMCouncil.from_env()

        # Run deliberation
        if RICH_AVAILABLE:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress:
                task = progress.add_task("[cyan]Council deliberating...", total=None)
                session = await council.deliberate(query, verbose=False)
                progress.update(task, description="[green]✓ Complete!")
        else:
            print("Council deliberating...")
            session = await council.deliberate(query, verbose=True)

        # Print Stage 1 results
        print_stage(1, "INDIVIDUAL RESPONSES")

        if RICH_AVAILABLE:
            for resp in session.stage1_responses:
                status = "[green]✓[/green]" if resp.success else "[red]✗[/red]"
                console.print(Panel(
                    resp.content[:500] + ("..." if len(resp.content) > 500 else ""),
                    title=f"{status} {resp.provider_name} ({resp.model})",
                    subtitle=f"⏱️ {resp.latency_ms:.0f}ms | 🔤 {resp.tokens_used} tokens",
                    border_style="blue" if resp.success else "red"
                ))
        else:
            for resp in session.stage1_responses:
                status = "✓" if resp.success else "✗"
                print(f"\n[{status}] {resp.provider_name} ({resp.model})")
                print(f"    Time: {resp.latency_ms:.0f}ms | Tokens: {resp.tokens_used}")
                print(f"    {resp.content[:200]}...")

        # Print Stage 2 results
        if session.stage2_reviews:
            print_stage(2, "PEER REVIEW")

            if RICH_AVAILABLE:
                table = Table(title="Peer Review Scores")
                table.add_column("Reviewer", style="cyan")
                table.add_column("Reviewed", style="magenta")
                table.add_column("Score", style="yellow")

                for review in session.stage2_reviews:
                    score_color = "green" if review.score >= 7 else "yellow" if review.score >= 5 else "red"
                    table.add_row(
                        review.reviewer,
                        review.reviewee,
                        f"[{score_color}]{review.score}/10[/{score_color}]"
                    )

                console.print(table)
            else:
                for review in session.stage2_reviews:
                    print(f"  {review.reviewer} → {review.reviewee}: {review.score}/10")

        # Print Stage 3 result
        print_stage(3, "CHAIRMAN CONSENSUS")

        if RICH_AVAILABLE:
            console.print(Panel(
                Markdown(session.stage3_consensus),
                title=f"👑 Final Answer (by {session.chairman_provider})",
                border_style="green",
                padding=(1, 2)
            ))
        else:
            print(f"\n👑 Final Answer (by {session.chairman_provider}):\n")
            print(session.stage3_consensus)

        await council.close()

    except ValueError as e:
        print(f"❌ Error: {e}")
        print("\nMake sure to:")
        print("1. Copy .env.example to .env")
        print("2. Add your API keys")


async def run_interactive():
    """Run interactive mode."""
    print_header()

    if RICH_AVAILABLE:
        console.print("[bold]Interactive mode. Type 'quit' to exit.[/bold]\n")
    else:
        print("Interactive mode. Type 'quit' to exit.\n")

    try:
        council = LLMCouncil.from_env()

        while True:
            try:
                query = input("\n🏛️ You: ").strip()

                if query.lower() in ('quit', 'exit', 'q'):
                    print("\nGoodbye! 👋")
                    break

                if not query:
                    continue

                session = await council.deliberate(query, verbose=False)

                if RICH_AVAILABLE:
                    console.print(Panel(
                        Markdown(session.stage3_consensus),
                        title="👑 Council",
                        border_style="green"
                    ))
                else:
                    print(f"\n👑 Council: {session.stage3_consensus}")

            except KeyboardInterrupt:
                print("\n\nGoodbye! 👋")
                break

        await council.close()

    except ValueError as e:
        print(f"❌ Error: {e}")


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage:")
        print('  python council_demo.py "Your question here"')
        print('  python council_demo.py --interactive')
        print('  python council_demo.py --health-check')
        sys.exit(1)

    arg = sys.argv[1]

    if arg == "--health-check":
        asyncio.run(run_health_check())
    elif arg == "--interactive":
        asyncio.run(run_interactive())
    else:
        # Treat all remaining args as the query
        query = " ".join(sys.argv[1:])
        asyncio.run(run_query(query))


if __name__ == "__main__":
    main()
