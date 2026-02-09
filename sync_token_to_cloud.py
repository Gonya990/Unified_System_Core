import firebase_admin
from firebase_admin import credentials, firestore
import json
import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent
SERVICE_ACCOUNT_PATH = BASE_DIR / "Projects/AI_Core/gcp-service-account.json"
TOKEN_PATH = BASE_DIR / "Scripts/automation/.credentials/gmail_token.json"

def sync_token_to_firestore(user_id):
    if not TOKEN_PATH.exists():
        print(f"❌ Local token not found at {TOKEN_PATH}")
        return

    print(f"🔄 Syncing token to Firestore for user {user_id}...")
    
    # Initialize Firestore
    cred = credentials.Certificate(str(SERVICE_ACCOUNT_PATH))
    firebase_admin.initialize_app(cred)
    db = firestore.client()

    with open(TOKEN_PATH, 'r') as f:
        token_data = json.load(f)

    # User document in Firestore
    user_ref = db.collection('users').document(str(user_id))
    
    # Update data
    user_ref.set({
        'is_google_connected': True,
        'google_tokens': json.dumps(token_data),
        'last_interaction': firestore.SERVER_TIMESTAMP
    }, merge=True)

    print(f"✅ Successfully updated Firestore for user {user_id}")

if __name__ == "__main__":
    # Igor's ID from USER_ALIASES in ai_telegram_bot_v2.py
    IGOR_ID = 708531393
    sync_token_to_firestore(IGOR_ID)
