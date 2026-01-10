
import pickle
import json
import os
from google.oauth2.credentials import Credentials

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # Scripts/Utilities -> Scripts -> Root? No.
# Script is in Scripts/Utilities. 
# Pickle is in Scripts/automation/.credentials

CREDS_DIR = os.path.join(os.path.dirname(BASE_DIR), "automation", ".credentials")
PICKLE_PATH = os.path.join(CREDS_DIR, "gmail_token.pickle")
JSON_PATH = os.path.join(CREDS_DIR, "gmail_token.json")

def convert():
    print(f"Reading from {PICKLE_PATH}...")
    if not os.path.exists(PICKLE_PATH):
        print("❌ Pickle file not found.")
        return

    try:
        with open(PICKLE_PATH, 'rb') as token:
            creds = pickle.load(token)
            
        print("✅ Pickle loaded.")
        
        # Convert to JSON
        json_creds = creds.to_json()
        
        with open(JSON_PATH, 'w') as f:
            f.write(json_creds)
            
        print(f"✅ Converted and saved to {JSON_PATH}")
        
    except Exception as e:
        print(f"❌ Conversion failed: {e}")

if __name__ == "__main__":
    convert()
