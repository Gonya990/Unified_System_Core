import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add project root to path
sys.path.append("/home/gonya/Documents/Unified_System/Windows_AI_Core")

from src.gmail_client import GmailClient
from src.config_manager import ConfigManager

def scan_bills():
    # Authenticate (uses existing token.pickle)
    # No args needed as paths are default
    client = GmailClient()
    
    if not client.authenticated:
        print("❌ Gmail auth failed")
        return

    # Keywords to search
    keywords = [
        "invoice", "bill", "receipt", "payment", "счет", "квитанция", "оплата",
        "Bezeq", "Partner", "Electric", "Arnona", "Water", "GCP", "Google Cloud"
    ]
    
    # Search last 30 days
    query = f"after:{(datetime.now() - timedelta(days=30)).strftime('%Y/%m/%d')}"
    query += " (" + " OR ".join(keywords) + ")"
    
    print(f"🔍 Scanning Gmail for bills (Last 30 days)...")
    messages = client.search_emails(query, max_results=20)
    
    if not messages:
        print("📭 No recent bills found.")
        return

    total_est = 0
    print("\n📄 **Found Documents:**")
    for msg in messages:
        subject = msg.get('subject', 'No Subject')
        sender = msg.get('from', 'Unknown')
        date = msg.get('date', '')
        
        # Simple extraction (naive)
        print(f"- **{date[:10]}** | {sender}: {subject}")

if __name__ == "__main__":
    scan_bills()
