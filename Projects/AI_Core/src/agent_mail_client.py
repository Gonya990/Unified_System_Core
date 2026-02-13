#!/usr/bin/env python3
"""
Agent Mail MCP Client (AI Core)
Unified interface for inter-agent communication via Agent Mail server.
"""

import json
import os
import sys
from datetime import datetime

# Add SDK to path
# Path: Projects/AI_Core/src -> ../../../External_Tools/Stack/agent_mail_sdk/src
sdk_dir = "../../../External_Tools/Stack/agent_mail_sdk/src"
sdk_path = os.path.abspath(os.path.join(os.path.dirname(__file__), sdk_dir))
if sdk_path not in sys.path:
    sys.path.append(sdk_path)

try:
    from agent_mail import AgentMailClient, AgentMailConfig
except ImportError:
    warn_msg = f"⚠️ Warning: Could not import 'agent_mail' SDK from {sdk_path}. Continuing in degraded mode."
    print(warn_msg)
    AgentMailClient = None
    AgentMailConfig = None


def main():
    """CLI interface"""
    import argparse

    description = "Agent Mail MCP Client (AI Core)"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "action",
        choices=[
            "health",
            "register",
            "inbox",
            "send",
            "broadcast",
            "read",
            "agents",
            "reserve",
            "ack",
        ],
    )
    parser.add_argument("--to", nargs="+", help="Recipients (for send)")
    parser.add_argument("--subject", help="Message subject")
    parser.add_argument("--body", help="Message body (markdown)")
    parser.add_argument(
        "--importance",
        choices=["low", "normal", "high"],
        default="normal",
    )
    parser.add_argument("--limit", type=int, default=20, help="Inbox limit")
    parser.add_argument("--id", type=int, help="Message ID for read")
    parser.add_argument("--files", nargs="+", help="Files to reserve")
    parser.add_argument("--reason", help="Reason for reservation")
    parser.add_argument(
        "--note",
        help="Note for acknowledgement",
        default="Acknowledged via CLI",
    )

    def format_ts(ts_str):
        """Format timestamp to local time"""
        if not ts_str:
            return "N/A"
        try:
            # Handle standard ISO format
            dt = datetime.fromisoformat(ts_str)
            # Convert to local time
            return dt.astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")
        except Exception:
            return ts_str

    args = parser.parse_args()

    # AI Core specific config default if needed, otherwise uses env
    client = AgentMailClient() if AgentMailClient else None
    if not client:
        print("❌ AgentMailClient not available")
        exit(1)

    if args.action == "health":
        if client.health_check():
            print("✅ Server healthy")
        else:
            print("❌ Server unavailable")
            exit(1)

    elif args.action == "register":
        result = client.register()
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
                print(f"   {format_ts(msg['created_ts'])}")
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
        msg_id = result["deliveries"][0]["payload"]["id"]
        print(f"✅ Message sent (ID: {msg_id})")

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
            print(f"Time: {format_ts(target['created_ts'])}")
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
            subject=args.subject,
            body_md=args.body,
            importance=args.importance,
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
                marker = " (you)" if agent.get("is_self") else ""
                print(f"  • {name}{marker}: {status}")

    elif args.action == "reserve":
        if not args.files or not args.reason:
            print("❌ --files and --reason required")
            exit(1)

        try:
            result = client.reserve_files(
                paths=args.files,
                reason=args.reason,
            )
            print(f"✅ Reservation request sent for {len(args.files)} files")
            print(f"Response: {json.dumps(result, indent=2)}")
        except Exception as e:
            print(f"❌ Reservation failed: {e}")
            exit(1)

    elif args.action == "ack":
        if not args.id:
            print("❌ --id <message_id> required")
            exit(1)

        try:
            client.acknowledge(message_id=args.id, note=args.note)
            print(f"✅ Message #{args.id} acknowledged")
        except Exception as e:
            print(f"❌ Acknowledgement failed: {e}")
            exit(1)


if __name__ == "__main__":
    main()
