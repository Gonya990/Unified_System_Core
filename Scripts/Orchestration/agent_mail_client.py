#!/usr/bin/env python3
"""
Agent Mail MCP Client
Unified interface for inter-agent communication via Agent Mail server.
"""

import json
import os
import sys

# Add SDK to path
sdk_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../External_Tools/Stack/agent_mail_sdk/src"))
if sdk_path not in sys.path:
    sys.path.append(sdk_path)

try:
    from agent_mail import AgentMailClient
except ImportError:
    # Fallback for when SDK is not yet fully set up or path is wrong
    print("❌ Critical: Could not import 'agent_mail' SDK. Please ensure External_Tools/Stack/agent_mail_sdk exists.")
    sys.exit(1)


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
    parser.add_argument("--importance", choices=["low", "normal", "high"], default="normal")
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

        result = client.broadcast(subject=args.subject, body_md=args.body, importance=args.importance)
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


if __name__ == "__main__":
    main()
