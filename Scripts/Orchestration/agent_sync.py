#!/usr/bin/env python3
"""
Agent Sync - Unified workflow for Agent Mail + Beads synchronization.

Combines:
- Agent Mail: inbox fetch, registration, message handling
- Beads: task sync, ready queue, status updates

Usage:
    python agent_sync.py                    # Full sync
    python agent_sync.py --quick            # Quick sync (inbox + beads only)
    python agent_sync.py inbox              # Inbox only
    python agent_sync.py beads              # Beads only
    python agent_sync.py status             # Show current status
"""

import argparse
import json
import os
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

# Optional .env loading (no hard dependency in committed code)
try:
    import importlib

    dotenv = importlib.import_module("dotenv")
    # Try loading from standard locations first
    if not dotenv.load_dotenv():
        # Try finding it in Projects/AI_Core explicitly
        script_dir = Path(__file__).resolve().parent
        repo_root = script_dir.parent.parent
        env_path = repo_root / "Projects/AI_Core/.env"
        if env_path.exists():
            dotenv.load_dotenv(env_path)
except Exception:
    pass

try:
    # Allow running from repo root.
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import agent_mail_client as _agent_mail_client

    AgentMailClient = _agent_mail_client.AgentMailClient
    AgentMailConfig = _agent_mail_client.AgentMailConfig
except Exception as e:
    raise SystemExit(
        "agent_sync.py requires Scripts/Orchestration/agent_mail_client.py and its dependencies.\n"
        "Run from Scripts/Orchestration or set PYTHONPATH accordingly.\n\n"
        "Example:\n"
        "  cd Scripts/Orchestration\n"
        "  python3 agent_mail_client.py health\n"
    ) from e


@dataclass
class SyncResult:
    """Result of a sync operation"""

    success: bool
    component: str
    data: dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None

    def to_dict(self) -> dict:
        return {"success": self.success, "component": self.component, "data": self.data, "error": self.error}


@dataclass
class SyncReport:
    """Aggregated sync report"""

    timestamp: str
    agent_name: str
    results: list[SyncResult] = field(default_factory=list)

    @property
    def all_success(self) -> bool:
        return all(r.success for r in self.results)

    @property
    def urgent_messages(self) -> list[dict]:
        for r in self.results:
            if r.component == "inbox" and r.success:
                return [m for m in r.data.get("messages", []) if m.get("importance") in ("high", "urgent")]
        return []

    @property
    def ready_tasks(self) -> list[dict]:
        for r in self.results:
            if r.component == "beads" and r.success:
                return r.data.get("ready", [])
        return []

    def to_dict(self) -> dict:
        return {
            "timestamp": self.timestamp,
            "agent_name": self.agent_name,
            "success": self.all_success,
            "results": [r.to_dict() for r in self.results],
            "urgent_count": len(self.urgent_messages),
            "ready_count": len(self.ready_tasks),
        }

    def print_summary(self):
        """Print human-readable summary"""
        print(f"\n{'=' * 50}")
        print(f"SYNC REPORT - {self.agent_name}")
        print(f"{'=' * 50}")
        print(f"Time: {self.timestamp}")
        print(f"Status: {'✅ OK' if self.all_success else '❌ ERRORS'}")
        print()

        for r in self.results:
            icon = "✅" if r.success else "❌"
            print(f"{icon} {r.component.upper()}")
            if r.error:
                print(f"   Error: {r.error}")
            elif r.component == "inbox":
                msgs = r.data.get("messages", [])
                urgent = [m for m in msgs if m.get("importance") in ("high", "urgent")]
                print(f"   Messages: {len(msgs)} ({len(urgent)} urgent)")
                for m in urgent[:3]:
                    print(f"   ⚠️  [{m.get('from')}] {m.get('subject')}")
            elif r.component == "beads":
                ready = r.data.get("ready", [])
                in_prog = r.data.get("in_progress", [])
                print(f"   Ready: {len(ready)} | In Progress: {len(in_prog)}")
                for t in ready[:3]:
                    print(f"   📋 {t.get('id')}: {t.get('title', '')[:40]}")
            elif r.component == "health":
                print(f"   Server: {'online' if r.data.get('healthy') else 'offline'}")

        print(f"{'=' * 50}\n")


class AgentSync:
    """Unified sync orchestrator"""

    def __init__(self, config: Optional[Any] = None):
        self.config = config or AgentMailConfig.from_env()
        self.mail_client = AgentMailClient(self.config)
        self.project_root = self._find_project_root()
        self.bd_available = self._check_bd_availability()

    def _check_bd_availability(self) -> bool:
        """Check if bd CLI is installed and in path"""
        try:
            subprocess.run(["bd", "--version"], capture_output=True, check=False)
            return True
        except FileNotFoundError:
            return False

    def _find_project_root(self) -> Path:
        """Find project root (contains .beads/)"""
        current = Path.cwd()
        for parent in [current] + list(current.parents):
            if (parent / ".beads").exists():
                return parent
        return current

    def _run_bd(self, *args) -> subprocess.CompletedProcess:
        """Run beads CLI command"""
        cmd = ["bd"] + list(args)
        try:
            return subprocess.run(cmd, capture_output=True, text=True, cwd=self.project_root)
        except FileNotFoundError:
            return subprocess.CompletedProcess(
                args=cmd, returncode=127, stdout="", stderr="Beads (bd) command not found. Please install it."
            )

    def check_health(self) -> SyncResult:
        """Check Agent Mail server health"""
        try:
            healthy = self.mail_client.health_check()
            return SyncResult(success=True, component="health", data={"healthy": healthy})
        except Exception as e:
            return SyncResult(success=False, component="health", error=str(e))

    def sync_inbox(self, limit: int = 20) -> SyncResult:
        """Fetch and process inbox"""
        try:
            messages = self.mail_client.fetch_inbox(limit=limit)

            # Auto-acknowledge urgent messages we've seen
            for msg in messages:
                if msg.get("ack_required") and msg.get("importance") in ("high", "urgent"):
                    try:
                        self.mail_client.acknowledge_message(msg["id"])
                    except Exception:
                        pass

            return SyncResult(
                success=True,
                component="inbox",
                data={
                    "messages": messages,
                    "count": len(messages),
                    "unread": len([m for m in messages if not m.get("read")]),
                },
            )
        except Exception as e:
            return SyncResult(success=False, component="inbox", error=str(e))

    def sync_beads(self) -> SyncResult:
        """Sync beads task board"""
        if not self.bd_available:
            return SyncResult(
                success=True,
                component="beads",
                data={"ready": [], "in_progress": [], "synced": False, "note": "Beads CLI (bd) not found"},
            )
        try:
            # Sync with remote
            sync_result = self._run_bd("sync")
            if sync_result.returncode != 0 and "not initialized" in sync_result.stderr:
                self._run_bd("init")
                self._run_bd("sync", "--import-only")

            # Get ready tasks
            ready_result = self._run_bd("ready", "--json")
            ready_tasks = []
            if ready_result.returncode == 0 and ready_result.stdout.strip():
                try:
                    ready_tasks = json.loads(ready_result.stdout)
                except json.JSONDecodeError:
                    # Parse text output
                    for line in ready_result.stdout.strip().split("\n"):
                        if line.startswith("US-") or line.startswith("BD-"):
                            parts = line.split(None, 1)
                            ready_tasks.append({"id": parts[0], "title": parts[1] if len(parts) > 1 else ""})

            # Get in-progress tasks
            prog_result = self._run_bd("list", "--status=in_progress", "--json")
            in_progress = []
            if prog_result.returncode == 0 and prog_result.stdout.strip():
                try:
                    in_progress = json.loads(prog_result.stdout)
                except json.JSONDecodeError:
                    pass

            return SyncResult(
                success=True, component="beads", data={"ready": ready_tasks, "in_progress": in_progress, "synced": True}
            )
        except Exception as e:
            return SyncResult(success=False, component="beads", error=str(e))

    def register_agent(self, task_description: str = "Active session") -> SyncResult:
        """Register/update agent status"""
        try:
            result = self.mail_client.register(program="claude-code", model="opus-4.5")
            return SyncResult(success=True, component="registration", data=result)
        except Exception as e:
            return SyncResult(success=False, component="registration", error=str(e))

    def push_beads(self) -> SyncResult:
        """Commit and push beads changes to prevent sync conflicts"""
        try:
            # First do a full sync
            self._run_bd("sync", "--import-only")
            self._run_bd("sync")

            # Check if there are changes to commit
            status = subprocess.run(
                ["git", "status", "--porcelain", ".beads/"], capture_output=True, text=True, cwd=self.project_root
            )

            if not status.stdout.strip():
                return SyncResult(
                    success=True, component="push", data={"pushed": False, "reason": "No changes to push"}
                )

            # Add, commit, pull --rebase, push
            subprocess.run(["git", "add", ".beads/"], cwd=self.project_root, check=True)
            subprocess.run(
                ["git", "commit", "-m", "chore: sync beads"], cwd=self.project_root, check=True, capture_output=True
            )
            subprocess.run(
                ["git", "pull", "--rebase"],
                cwd=self.project_root,
                check=True,
                capture_output=True,
                env={**os.environ, "GIT_TERMINAL_PROMPT": "0"},
            )
            subprocess.run(
                ["git", "push"],
                cwd=self.project_root,
                check=True,
                capture_output=True,
                env={**os.environ, "GIT_TERMINAL_PROMPT": "0"},
            )

            return SyncResult(success=True, component="push", data={"pushed": True})
        except subprocess.CalledProcessError as e:
            return SyncResult(success=False, component="push", error=f"Git error: {e.stderr if e.stderr else str(e)}")
        except Exception as e:
            return SyncResult(success=False, component="push", error=str(e))

    def full_sync(self, task_description: str = "Active session") -> SyncReport:
        """Perform full sync: health + register + inbox + beads"""
        report = SyncReport(timestamp=datetime.utcnow().isoformat() + "Z", agent_name=self.config.agent_name)

        # Health check
        report.results.append(self.check_health())

        # Only continue if healthy
        if report.results[-1].data.get("healthy"):
            report.results.append(self.register_agent(task_description))
            report.results.append(self.sync_inbox())

        # Beads sync (local, doesn't need mail server)
        report.results.append(self.sync_beads())

        return report

    def quick_sync(self) -> SyncReport:
        """Quick sync: inbox + beads only"""
        report = SyncReport(timestamp=datetime.utcnow().isoformat() + "Z", agent_name=self.config.agent_name)

        report.results.append(self.sync_inbox())
        report.results.append(self.sync_beads())

        return report


def main():
    parser = argparse.ArgumentParser(
        description="Agent Sync - Unified Agent Mail + Beads workflow",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  agent_sync.py                 Full sync (health + register + inbox + beads)
  agent_sync.py --quick         Quick sync (inbox + beads only)
  agent_sync.py inbox           Inbox only
  agent_sync.py beads           Beads only
  agent_sync.py status          Current status
  agent_sync.py --json          Output as JSON
        """,
    )

    parser.add_argument(
        "action",
        nargs="?",
        default="full",
        choices=["full", "quick", "inbox", "beads", "health", "status"],
        help="Sync action (default: full)",
    )
    parser.add_argument("--quick", "-q", action="store_true", help="Quick sync (inbox + beads only)")
    parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")
    parser.add_argument("--task", "-t", default="Active session", help="Task description for registration")
    parser.add_argument("--limit", "-l", type=int, default=20, help="Inbox message limit")
    parser.add_argument("--push", "-p", action="store_true", help="Commit and push beads changes after sync")

    args = parser.parse_args()

    sync = AgentSync()

    # Handle --quick flag
    if args.quick:
        args.action = "quick"

    report: Optional[SyncReport] = None

    # Execute action
    if args.action == "full":
        report = sync.full_sync(args.task)
    elif args.action == "quick":
        report = sync.quick_sync()
    elif args.action == "inbox":
        result = sync.sync_inbox(args.limit)
        report = SyncReport(
            timestamp=datetime.utcnow().isoformat() + "Z", agent_name=sync.config.agent_name, results=[result]
        )
    elif args.action == "beads":
        result = sync.sync_beads()
        report = SyncReport(
            timestamp=datetime.utcnow().isoformat() + "Z", agent_name=sync.config.agent_name, results=[result]
        )
    elif args.action == "health":
        result = sync.check_health()
        report = SyncReport(
            timestamp=datetime.utcnow().isoformat() + "Z", agent_name=sync.config.agent_name, results=[result]
        )
    elif args.action == "status":
        report = sync.quick_sync()

    if report is None:
        raise SystemExit(f"Unknown action: {args.action}")

    # Output
    if args.json:
        print(json.dumps(report.to_dict(), indent=2))
    else:
        report.print_summary()

    # Push beads changes if requested
    if args.push:
        print("\n📤 Pushing beads changes...")
        push_result = sync.push_beads()
        report.results.append(push_result)
        if push_result.success:
            print("✅ Beads changes committed and pushed")
        else:
            print(f"❌ Push failed: {push_result.error}")

    # Exit code based on urgent messages
    if report.urgent_messages:
        print("⚠️  URGENT MESSAGES REQUIRE ATTENTION")
        sys.exit(2)

    sys.exit(0 if report.all_success else 1)


if __name__ == "__main__":
    main()
