import os
import pickle

from google.auth.transport.requests import Request

pickle_path = "Projects/AI_Core/config/gmail_token.pickle"
json_path = "Scripts/automation/.credentials/gmail_token.json"

# Create dir
os.makedirs(os.path.dirname(json_path), exist_ok=True)

try:
    with open(pickle_path, "rb") as token:
        creds = pickle.load(token)

    if not creds:
        print("Empty credentials in pickle")
        exit(1)

    print(f"Loaded credentials from {pickle_path}")
    print(f"Scopes: {creds.scopes}")

    # Refresh if needed/possible (optional, but good)
    if not creds.valid:
        if creds.expired and creds.refresh_token:
            print("Refreshing token...")
            try:
                creds.refresh(Request())
                print("Refreshed!")
            except Exception as e:
                print(f"Refresh failed: {e}")
                # Still try to save, maybe refresh works later or partial

    # Save as JSON
    with open(json_path, "w") as f:
        f.write(creds.to_json())
    print(f"Saved credentials to {json_path}")

except Exception as e:
    print(f"Error: {e}")
    exit(1)
