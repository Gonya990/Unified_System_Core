#!/usr/bin/env python3
"""
Run this script locally to generate Google OAuth token.
The token will be saved and can be uploaded to the server.
"""

import json
import os

from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/calendar"]
CLIENT_SECRET_FILE = "client_secret.json"
TOKEN_FILE = "google_token.json"


def main():
    # Check for client_secret.json
    if not os.path.exists(CLIENT_SECRET_FILE):
        # Try config folder
        if os.path.exists(f"config/{CLIENT_SECRET_FILE}"):
            client_file = f"config/{CLIENT_SECRET_FILE}"
        else:
            print(f"Error: {CLIENT_SECRET_FILE} not found!")
            print("Please place your Google OAuth client_secret.json in current directory")
            return
    else:
        client_file = CLIENT_SECRET_FILE

    print(f"Using credentials from: {client_file}")

    # Run the OAuth flow - this will open browser
    flow = InstalledAppFlow.from_client_secrets_file(client_file, SCOPES)
    credentials = flow.run_local_server(port=8085)

    # Save credentials to file
    token_data = {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes,
    }

    with open(TOKEN_FILE, "w") as f:
        json.dump(token_data, f, indent=2)

    print(f"\n✅ Token saved to {TOKEN_FILE}")
    print("Now upload this token to the server for user authentication.")


if __name__ == "__main__":
    main()
