import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Orchestration"))

from Orchestration.agent_mail_client import AgentMailClient


def cleanup_inbox():
    client = AgentMailClient()
    print("🧹 Cleaning up VioletCastle loop garbage...")

    # Fetch a batch
    messages = client.fetch_inbox(limit=100)
    if not messages:
        print("Inbox empty!")
        return

    count = 0
    for msg in messages:
        sender = msg.get("from", "")
        subject = msg.get("subject", "")
        msg_id = msg.get("id")

        # Heuristic: Delete if from VioletCastle AND subject contains "Concilium"
        if sender == "VioletCastle" and "Concilium" in subject:
            print(f"Adding #{msg_id} to mark-read queue...")
            try:
                client.mark_read(msg_id)
                count += 1
            except Exception as e:
                print(f"Failed to mark #{msg_id}: {e}")

    print(f"✅ Marked {count} messages as read.")


if __name__ == "__main__":
    cleanup_inbox()
