import firebase_admin
from firebase_admin import credentials, firestore
import sys

def reset_user_google(user_id):
    cred = credentials.Certificate("gcp-service-account.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    
    user_ref = db.collection("users").document(str(user_id))
    user_ref.update({
        "is_google_connected": False,
        "google_creds": None
    })
    print(f"✅ Reset Google status for user {user_id} in Firestore")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        reset_user_google(sys.argv[1])
    else:
        print("Usage: python reset_google.py <user_id>")
