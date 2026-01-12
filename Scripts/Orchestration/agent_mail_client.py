#!/usr/bin/env python3
"""
Agent Mail MCP Client
Unified interface for inter-agent communication via Agent Mail server.
"""

import json
import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import requests

try:
    from pathlib import Path

    from dotenv import load_dotenv

    # Load .env from project root (2 levels up from this script)
    env_path = Path(__file__).resolve().parent.parent.parent / ".env"
    load_dotenv(env_path)
except ImportError:
    pass


@dataclass
class AgentMailConfig:
    """Agent Mail configuration"""

    server: str
    token: str
    project_key: str
    agent_name: str

    @classmethod
    def from_env(cls):
        """Load config from environment"""
        project_key = (
            os.getenv("AGENT_MAIL_PROJECT")
            or os.getenv("AGENT_MAIL_PROJECT_KEY")
            or os.getenv("PROJECT_KEY")
            or "/home/gonya/Unified_System"
        )
        if project_key == "home-gonya-unified-system":
            project_key = "/home/gonya/Unified_System"

        return cls(
            server=os.getenv("AGENT_MAIL_SERVER", "http://100.110.209.49:8765"),
            token="c2bb2cf043ec2ae56a0dec69024e6129eb5cde36a22bddb93afcfa2e71e72afb",
            project_key=project_key,
            agent_name=os.getenv("AGENT_MAIL_NAME", "Antigravity"),
        )


class AgentMailClient:
    """MCP client for Agent Mail"""

    def __init__(self, config: Optional[AgentMailConfig] = None):
        self.config = config or AgentMailConfig.from_env()
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {self.config.token}",
                "Content-Type": "application/json",
            }
        )

    def _call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call MCP tool"""
        payload = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {"name": tool_name, "arguments": arguments},
            "id": 1,
        }

        response = self.session.post(f"{self.config.server}/mcp", json=payload)
        response.raise_for_status()

        result = response.json()

        if result.get("result", {}).get("isError"):
            error_msg = result["result"]["content"][0]["text"]
            raise Exception(f"MCP Error: {error_msg}")

        return result.get("result", {})

    def ensure_project(self, human_key: Optional[str] = None) -> Dict[str, Any]:
        """Ensure project exists on server"""
        key = human_key or self.config.project_key
        result = self._call_tool(
            "ensure_project",
            {"human_key": key},
        )
        return result

    def health_check(self) -> bool:
        """Check server health"""
        try:
            response = self.session.get(f"{self.config.server}/health/liveness")
            # Check for alive status or ok
            return response.status_code == 200
        except:
            return False

    def register(
        self,
        agent_name: Optional[str] = None,
        program: Optional[str] = None,
        model: Optional[str] = None,
        task_description: str = "Active session",
    ) -> Dict[str, Any]:
        """Register agent with server"""
        name = agent_name or self.config.agent_name
        prog = program or os.getenv("AGENT_MAIL_PROGRAM", "claude-code")
        mod = model or os.getenv("AGENT_MAIL_MODEL", "opus-4.5")

        result = self._call_tool(
            "register_agent",
            {
                "project_key": self.config.project_key,
                "name": name,
                "program": prog,
                "model": mod,
                "task_description": task_description,
            },
        )

        # Handle both structuredContent and content formats
        if "structuredContent" in result:
            return result["structuredContent"]
        elif "content" in result:
            # Parse from text content if needed
            content = result["content"]
            if isinstance(content, list) and content:
                text = content[0].get("text", "{}")
                try:
                    return json.loads(text)
                except:
                    return {"raw": text}
        return result

    def send_message(
        self,
        to: List[str],
        subject: str,
        body_md: str,
        importance: str = "normal",
        cc: Optional[List[str]] = None,
        ack_required: bool = False,
    ) -> Dict[str, Any]:
        """Send message to agents"""
        result = self._call_tool(
            "send_message",
            {
                "project_key": self.config.project_key,
                "sender_name": self.config.agent_name,
                "to": to,
                "subject": subject,
                "body_md": body_md,
                "importance": importance,
                "cc": cc or [],
                "ack_required": ack_required,
            },
        )

        return result.get("structuredContent", {})

    def fetch_inbox(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Fetch inbox messages"""
        result = self._call_tool(
            "fetch_inbox",
            {
                "project_key": self.config.project_key,
                "agent_name": self.config.agent_name,
                "limit": limit,
                "include_bodies": True,
            },
        )

        return result.get("structuredContent", {}).get("result", [])

    def mark_read(self, message_id: int):
        """Mark message as read"""
        self._call_tool(
            "mark_message_read",
            {
                "project_key": self.config.project_key,
                "agent_name": self.config.agent_name,
                "message_id": message_id,
            },
        )

    def reply(self, message_id: int, body_md: str):
        """Reply to message"""
        self._call_tool(
            "reply_message",
            {
                "project_key": self.config.project_key,
                "sender_name": self.config.agent_name,
                "message_id": message_id,
                "body_md": body_md,
            },
        )

    def whois(self, agent_name: str) -> Optional[Dict[str, Any]]:
        """Look up agent info by name"""
        try:
            result = self._call_tool(
                "whois",
                {
                    "project_key": self.config.project_key,
                    "agent_name": agent_name,
                },
            )
            return result.get("structuredContent", {})
        except:
            return None

    def list_agents(self, include_inactive: bool = False) -> List[Dict[str, Any]]:
        try:
            result = self._call_tool(
                "list_agents",
                {
                    "project_key": self.config.project_key,
                    "include_inactive": include_inactive,
                },
            )
            agents_data = result.get("structuredContent", {}).get("agents", [])
            return [a for a in agents_data if a.get("name") != self.config.agent_name]
        except Exception:
            return []

    def broadcast(self, subject: str, body_md: str, importance: str = "normal"):
        agents_data = self.list_agents()
        agent_names: List[str] = [str(a["name"]) for a in agents_data if a.get("name")]

        if not agent_names:
            raise Exception("No agents found to broadcast to")

        return self.send_message(
            to=agent_names, subject=subject, body_md=body_md, importance=importance
        )


def main():
    """CLI interface"""
    import argparse

    parser = argparse.ArgumentParser(description="Agent Mail MCP Client")
    parser.add_argument(
        "action",
        choices=["health", "register", "inbox", "send", "broadcast", "read", "agents"],
    )
    parser.add_argument("--to", nargs="+", help="Recipients (for send)")
    parser.add_argument("--subject", help="Message subject")
    parser.add_argument("--body", help="Message body (markdown)")
    parser.add_argument(
        "--importance", choices=["low", "normal", "high"], default="normal"
    )
    parser.add_argument("--limit", type=int, default=20, help="Inbox limit")
    parser.add_argument("--id", type=int, help="Message ID for read")

    args = parser.parse_args()

    client = AgentMailClient()

    if args.action == "health":
        if client.health_check():
            print("✅ Server healthy")
        else:
            print("❌ Server unavailable")
            exit(1)

    elif args.action == "register":
        result = client.register()
        # Server returns 'name' and 'id', not 'agent_name'/'agent_id'
        print(f"✅ Registered as: {result.get('name')} (ID: {result.get('id')})")

    elif args.action == "inbox":
        messages = client.fetch_inbox(limit=args.limit)
        if not messages:
            print("📭 Inbox empty")
        else:
            print(f"📬 {len(messages)} messages:\n")
            for msg in messages:
                status = "📖" if msg.get("read") else "✉️"
                print(f"{status} [{msg['id']}] From: {msg['from']} | {msg['subject']}")
                print(f"   {msg['created_ts']}")
                print()

    elif args.action == "send":
        if not args.to or not args.subject or not args.body:
            print("❌ --to, --subject, and --body required")
            exit(1)

        result = client.send_message(
            to=args.to,
            subject=args.subject,
            body_md=args.body,
            importance=args.importance,
        )
        print(f"✅ Message sent (ID: {result['deliveries'][0]['payload']['id']})")

    elif args.action == "read":
        if not args.id:
            print("❌ --id <message_id> required")
            exit(1)
        messages = client.fetch_inbox(limit=100)
        target = next((m for m in messages if m["id"] == args.id), None)
        if target:
            print(f"DEBUG: {json.dumps(target, indent=2)}")
            print(f"📧 Message #{target['id']}")
            print(f"From: {target['from']}")
            print(f"Subject: {target['subject']}")
            print(f"Time: {target['created_ts']}")
            print("-" * 40)
            print(target.get("body_md") or target.get("body"))
            client.mark_read(target["id"])
        else:
            print(f"❌ Message #{args.id} not found")

    elif args.action == "broadcast":
        if not args.subject or not args.body:
            print("❌ --subject and --body required")
            exit(1)

        result = client.broadcast(
            subject=args.subject, body_md=args.body, importance=args.importance
        )
        print(f"✅ Broadcast sent to {result['count']} agents")

    elif args.action == "agents":
        agents = client.list_agents()
        if not agents:
            print("📭 No registered agents found")
        else:
            print(f"👥 {len(agents)} registered agents:\n")
            for agent in agents:
                name = agent.get("name", "Unknown")
                status = agent.get("task_description", "Unknown")
                print(f"  • {name}: {status}")


if __name__ == "__main__":
    main()
