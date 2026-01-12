"""
Agent Mail Client Implementation
"""
import json
import os
from dataclasses import dataclass
from typing import Any, Optional

import requests
from dotenv import load_dotenv

# Default load of env
load_dotenv()


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
        # Normalize legacy key if needed
        if project_key == "home-gonya-unified-system":
            project_key = "/home/gonya/Unified_System"

        return cls(
            server=os.getenv("AGENT_MAIL_SERVER", "http://100.110.209.49:8765"),
            token=os.getenv("AGENT_MAIL_TOKEN", "c2bb2cf043ec2ae56a0dec69024e6129eb5cde36a22bddb93afcfa2e71e72afb"),
            project_key=project_key,
            agent_name=os.getenv("AGENT_MAIL_NAME", "OrangeStone"),
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

    def _call_tool(self, tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        """Call MCP tool"""
        payload = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {"name": tool_name, "arguments": arguments},
            "id": 1,
        }

        try:
            response = self.session.post(f"{self.config.server}/mcp", json=payload, timeout=30)
            response.raise_for_status()

            result = response.json()

            if result.get("result", {}).get("isError"):
                error_msg = result["result"]["content"][0]["text"]
                raise Exception(f"MCP Error: {error_msg}")

            return result.get("result", {})
        except requests.exceptions.RequestException as e:
            raise Exception(f"Connection failed: {e}")

    def ensure_project(self, human_key: Optional[str] = None) -> dict[str, Any]:
        """Ensure project exists on server"""
        key = human_key or self.config.project_key
        return self._call_tool(
            "ensure_project",
            {"human_key": key},
        )

    def health_check(self) -> bool:
        """Check server health"""
        try:
            response = self.session.get(f"{self.config.server}/health/liveness", timeout=5)
            return response.status_code == 200
        except:
            return False

    def register(
        self,
        agent_name: Optional[str] = None,
        program: Optional[str] = None,
        model: Optional[str] = None,
        task_description: str = "Active session",
    ) -> dict[str, Any]:
        """
        Register agent with server.
        Returns dict with 'name', 'id', etc.
        """
        name = agent_name or self.config.agent_name
        prog = program or os.getenv("AGENT_MAIL_PROGRAM", "python-sdk")
        mod = model or os.getenv("AGENT_MAIL_MODEL", "generic")

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

        if "structuredContent" in result:
            return result["structuredContent"]
        elif "content" in result:
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
        to: list[str],
        subject: str,
        body_md: str,
        importance: str = "normal",
        cc: Optional[list[str]] = None,
        ack_required: bool = False,
    ) -> dict[str, Any]:
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

    def fetch_inbox(self, limit: int = 20) -> list[dict[str, Any]]:
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

    def whois(self, agent_name: str) -> Optional[dict[str, Any]]:
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

    def list_agents(self, include_inactive: bool = False) -> list[dict[str, Any]]:
        """List all agents"""
        try:
            result = self._call_tool(
                "list_agents",
                {
                    "project_key": self.config.project_key,
                    "include_inactive": include_inactive,
                },
            )
            agents = result.get("structuredContent", {}).get("agents", [])
            for a in agents:
                if a.get("name") == self.config.agent_name:
                    a["is_self"] = True
            return agents
        except Exception:
            return []

    def broadcast(self, subject: str, body_md: str, importance: str = "normal"):
        """Broadcast message to all agents"""
        agents_data = self.list_agents()
        agent_names = [str(a["name"]) for a in agents_data if a.get("name")]

        if not agent_names:
            raise Exception("No agents found to broadcast to")

        return self.send_message(to=agent_names, subject=subject, body_md=body_md, importance=importance)

    def reserve_files(
        self,
        paths: list[str],
        reason: str,
        exclusive: bool = True,
        duration: int = 300,
    ) -> dict[str, Any]:
        """Reserve files for editing"""
        result = self._call_tool(
            "file_reservation_paths",
            {
                "project_key": self.config.project_key,
                "agent_name": self.config.agent_name,
                "paths": paths,
                "exclusive": exclusive,
                "reason": reason,

            },
        )
        return result.get("structuredContent", {})

    def check_reservations(self, paths: list[str]) -> dict[str, Any]:
        """Check file reservations"""
        # Note: Using the same tool but with check_only=True or relying on the return of reservation
        # However, typically we just try to reserve.
        # Let's check the workflow definition again.
        # It says `agent_mail_file_reservation_paths`
        # We'll use a separate call or list call if available, but for now we implement the reservation action.
        # If we need to just check, we might need a different tool.
        # Let's stick to reserve_files for now as per US-l54.
        pass

    def acknowledge(self, message_id: int, note: str = "Acknowledged"):
        """Acknowledge a message requiring ACK"""
        self._call_tool(
            "acknowledge_message",
            {
                "project_key": self.config.project_key,
                "agent_name": self.config.agent_name,
                "message_id": message_id,
                "note": note,
            },
        )
