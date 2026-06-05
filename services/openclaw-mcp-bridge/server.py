#!/usr/bin/env python3
"""MCP stdio server: Cursor client ↔ OpenClaw (or local fallback wiki/alerts)."""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import httpx
import yaml

STAGING_ROOT = Path(__file__).resolve().parents[2]
DATA_WIKI = STAGING_ROOT / "data" / "memory-wiki"
DATA_ALERTS = STAGING_ROOT / "data" / "alerts"
OPENCLAW_BASE = os.environ.get("OPENCLAW_BASE_URL", "")
APPROVAL_URL = os.environ.get("APPROVAL_GATEWAY_URL", "http://127.0.0.1:8790")


def _wiki_entries() -> list[dict]:
    DATA_WIKI.mkdir(parents=True, exist_ok=True)
    entries = []
    for p in sorted(DATA_WIKI.glob("*.json")):
        try:
            entries.append(json.loads(p.read_text(encoding="utf-8")))
        except json.JSONDecodeError:
            continue
    return entries


def _alerts() -> list[dict]:
    DATA_ALERTS.mkdir(parents=True, exist_ok=True)
    out = []
    for p in sorted(DATA_ALERTS.glob("*.json"), reverse=True):
        try:
            out.append(json.loads(p.read_text(encoding="utf-8")))
        except json.JSONDecodeError:
            continue
    return out[:50]


def memory_search(query: str, limit: int = 10) -> list[dict]:
    q = query.lower()
    hits = []
    for e in _wiki_entries():
        text = json.dumps(e, ensure_ascii=False).lower()
        if q in text:
            hits.append(e)
        if len(hits) >= limit:
            break
    return hits


def get_recent_alerts(hours: int = 4) -> list[dict]:
    cutoff = datetime.now(timezone.utc).timestamp() - hours * 3600
    alerts = []
    for a in _alerts():
        ts = a.get("timestamp", 0)
        if ts >= cutoff:
            alerts.append(a)
    return alerts


def get_risk_score(command: str = "", path: str = "", intent: str = "") -> dict:
    try:
        r = httpx.post(
            f"{APPROVAL_URL}/v1/risk-score",
            json={"command": command, "path": path, "intent": intent},
            timeout=5.0,
        )
        r.raise_for_status()
        return r.json()
    except Exception as exc:
        return {"score": 0.0, "blocked": False, "reasons": [f"approval-gateway unreachable: {exc}"]}


def _openclaw_get(path: str) -> dict | list | None:
    if not OPENCLAW_BASE:
        return None
    try:
        r = httpx.get(f"{OPENCLAW_BASE.rstrip('/')}{path}", timeout=10.0)
        r.raise_for_status()
        return r.json()
    except Exception:
        return None


# Minimal MCP server over stdio (JSON-RPC lines)
TOOLS = [
    {
        "name": "get_recent_alerts",
        "description": "Recent system alerts from OpenClaw Task Flows or local fallback",
        "inputSchema": {
            "type": "object",
            "properties": {"hours": {"type": "integer", "default": 4}},
        },
    },
    {
        "name": "memory_search",
        "description": "Search long-term memory wiki (provenance-aware entries)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "limit": {"type": "integer", "default": 10},
            },
            "required": ["query"],
        },
    },
    {
        "name": "get_risk_score",
        "description": "Visual Guards: risk score for command/path/intent",
        "inputSchema": {
            "type": "object",
            "properties": {
                "command": {"type": "string"},
                "path": {"type": "string"},
                "intent": {"type": "string"},
            },
        },
    },
    {
        "name": "enqueue_background_task",
        "description": "Enqueue non-critical OpenClaw Task Flow (local log if gateway offline)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "payload": {"type": "object"},
            },
            "required": ["name"],
        },
    },
]


def handle_tool(name: str, arguments: dict) -> str:
    if name == "get_recent_alerts":
        remote = _openclaw_get("/api/alerts/recent")
        if remote is not None:
            return json.dumps(remote, ensure_ascii=False, indent=2)
        return json.dumps(get_recent_alerts(int(arguments.get("hours", 4))), indent=2)

    if name == "memory_search":
        remote = _openclaw_get(f"/api/memory/search?q={arguments.get('query', '')}")
        if remote is not None:
            return json.dumps(remote, ensure_ascii=False, indent=2)
        return json.dumps(
            memory_search(arguments.get("query", ""), int(arguments.get("limit", 10))),
            indent=2,
        )

    if name == "get_risk_score":
        result = get_risk_score(
            command=arguments.get("command", ""),
            path=arguments.get("path", ""),
            intent=arguments.get("intent", ""),
        )
        score = float(result.get("score", 0))
        if score >= 0.7:
            result["visual"] = "🔴 **CRITICAL RISK** — YubiKey required before execution."
        elif score >= 0.4:
            result["visual"] = "🟠 **ELEVATED RISK** — review before proceeding."
        return json.dumps(result, indent=2)

    if name == "enqueue_background_task":
        task = {
            "name": arguments.get("name"),
            "payload": arguments.get("payload", {}),
            "enqueued_at": datetime.now(timezone.utc).isoformat(),
        }
        queue = STAGING_ROOT / "data" / "task-queue"
        queue.mkdir(parents=True, exist_ok=True)
        path = queue / f"{task['name']}_{int(datetime.now(timezone.utc).timestamp())}.json"
        path.write_text(json.dumps(task, indent=2), encoding="utf-8")
        return json.dumps({"status": "queued", "path": str(path)})

    return json.dumps({"error": f"unknown tool {name}"})


def send(msg: dict) -> None:
    sys.stdout.write(json.dumps(msg) + "\n")
    sys.stdout.flush()


def main() -> None:
    manifest_path = STAGING_ROOT / "config" / "SOVEREIGN_MANIFEST.yaml"
    if manifest_path.exists():
        yaml.safe_load(manifest_path.read_text(encoding="utf-8"))

    while True:
        line = sys.stdin.readline()
        if not line:
            break
        try:
            req = json.loads(line)
        except json.JSONDecodeError:
            continue
        rid = req.get("id")
        method = req.get("method", "")
        params = req.get("params", {})

        if method == "initialize":
            send(
                {
                    "jsonrpc": "2.0",
                    "id": rid,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {"tools": {}},
                        "serverInfo": {"name": "unified-openclaw-bridge", "version": "1.0.0"},
                    },
                }
            )
        elif method == "tools/list":
            send({"jsonrpc": "2.0", "id": rid, "result": {"tools": TOOLS}})
        elif method == "tools/call":
            name = params.get("name", "")
            args = params.get("arguments", {}) or {}
            content = handle_tool(name, args)
            send(
                {
                    "jsonrpc": "2.0",
                    "id": rid,
                    "result": {"content": [{"type": "text", "text": content}]},
                }
            )
        elif method == "notifications/initialized":
            pass
        else:
            if rid is not None:
                send(
                    {
                        "jsonrpc": "2.0",
                        "id": rid,
                        "error": {"code": -32601, "message": f"Method not found: {method}"},
                    }
                )


if __name__ == "__main__":
    main()
