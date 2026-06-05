#!/usr/bin/env python3
"""
Bridge monitoring signals into OpenClaw Task Flow queue + local MCP alerts.
Extends mail_processor / unified_monitoring patterns without requiring Documents access.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

STAGING_ROOT = Path(__file__).resolve().parents[2]
ALERTS_DIR = STAGING_ROOT / "data" / "alerts"
TASK_QUEUE = STAGING_ROOT / "data" / "task-queue"
WIKI_DIR = STAGING_ROOT / "data" / "memory-wiki"

# Optional paths when monorepo is reachable
MAIL_PROCESSOR = Path.home() / "Documents/Unified_System_Core/Projects/AI_Core/src/mail_processor.py"
UNIFIED_MONITORING = Path.home() / "Documents/Unified_System_Core/Projects/AI_Core/unified_monitoring.py"


def emit_alert(severity: str, title: str, body: str, source: str = "monitoring-bridge") -> Path:
    ALERTS_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "severity": severity,
        "title": title,
        "body": body,
        "source": source,
        "timestamp": datetime.now(timezone.utc).timestamp(),
        "iso": datetime.now(timezone.utc).isoformat(),
    }
    path = ALERTS_DIR / f"{int(payload['timestamp'])}_{severity}.json"
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def enqueue_task_flow(name: str, payload: dict) -> Path:
    TASK_QUEUE.mkdir(parents=True, exist_ok=True)
    task = {
        "name": name,
        "payload": payload,
        "enqueued_at": datetime.now(timezone.utc).isoformat(),
        "type": "task_flow",
    }
    path = TASK_QUEUE / f"{name}_{int(datetime.now(timezone.utc).timestamp())}.json"
    path.write_text(json.dumps(task, indent=2), encoding="utf-8")
    return path


def redact_summary(text: str, max_len: int = 500) -> str:
    """Store only redacted semantic summary for external-LLM contexts."""
    lowered = text.lower()
    for token in ("password", "secret", "api_key", "token", "bearer"):
        if token in lowered:
            return "[REDACTED: sensitive content detected]"
    return text[:max_len]


def wiki_log_concept(summary: str, provenance: str) -> Path:
    WIKI_DIR.mkdir(parents=True, exist_ok=True)
    entry = {
        "type": "monitoring_concept",
        "summary": redact_summary(summary),
        "provenance": provenance,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    path = WIKI_DIR / f"concept_{int(datetime.now(timezone.utc).timestamp())}.json"
    path.write_text(json.dumps(entry, indent=2), encoding="utf-8")
    return path


def run_external_check() -> None:
    """Invoke monorepo scripts if present."""
    if MAIL_PROCESSOR.exists():
        emit_alert("info", "mail_processor available", str(MAIL_PROCESSOR))
    if UNIFIED_MONITORING.exists():
        emit_alert("info", "unified_monitoring available", str(UNIFIED_MONITORING))


def tailscale_doctor() -> None:
    try:
        proc = subprocess.run(
            [str(Path.home() / "start_here.sh"), "tailscale", "doctor"],
            capture_output=True,
            text=True,
            timeout=60,
        )
        if proc.returncode != 0:
            emit_alert("critical", "Tailscale doctor failed", proc.stdout + proc.stderr)
            enqueue_task_flow("tailscale_remediation", {"output": proc.stdout[-2000:]})
        else:
            emit_alert("info", "Tailscale doctor ok", "All critical nodes reachable")
    except Exception as exc:
        emit_alert("warning", "Tailscale doctor error", str(exc))


def main() -> int:
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument("--doctor", action="store_true", help="Run tailscale doctor check")
    p.add_argument("--emit-test", action="store_true")
    args = p.parse_args()

    run_external_check()
    if args.doctor:
        tailscale_doctor()
    if args.emit_test:
        emit_alert("warning", "Test alert", "Monitoring bridge self-test")
        wiki_log_concept("Self-test concept capture", "monitoring-bridge/test")

    print(f"Alerts dir: {ALERTS_DIR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
