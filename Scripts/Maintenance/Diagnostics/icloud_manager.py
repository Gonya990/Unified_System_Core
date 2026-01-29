import os
import sys

from pyicloud import PyiCloudService

# Folder to store session data
SESSION_DIR = os.path.expanduser("~/.icloud_session")
os.makedirs(SESSION_DIR, exist_ok=True)

def authenticate(username, password):
    print(f"🍏 Attempting login for {username}...")
    try:
        api = PyiCloudService(username, password, cookie_directory=SESSION_DIR)

        if api.requires_2fa:
            print(f"⚠️ Two-factor authentication required for {username}")

            # Request code via SMS if not auto-sent to devices
            # devices = api.trusted_devices
            # print(f"Trusted devices: {devices}")

            # This triggers the code to be sent
            # code = input("Enter the code you received: ")
            print("2FA_REQUIRED")
            # We exit here so the orchestrator knows to ask user for code
            return None

        if api.requires_2sa:
            print("⚠️ Two-step authentication required")
            print("2SA_REQUIRED")
            return None

        print("✅ iCloud Authenticated successfully!")
        print(f"User: {api.user}")
        return api

    except Exception as e:
        print(f"❌ iCloud Login Error: {e}")
        return None

def validate_2fa(username, password, code):
    print(f"🔐 Validating 2FA code for {username}...")
    try:
        api = PyiCloudService(username, password, cookie_directory=SESSION_DIR)
        result = api.validate_2fa_code(code)

        if result:
            print("✅ 2FA Code Verified!")
            if not api.is_trusted_session:
                print("Trusting this session...")
                api.trust_session()
            return True
        else:
            print("❌ Invalid 2FA Code")
            return False

    except Exception as e:
        print(f"❌ 2FA Validation Error: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 icloud_manager.py <login|verify> <username> <password> [code]")
        sys.exit(1)

    command = sys.argv[1]
    user = sys.argv[2]
    pwd = sys.argv[3]

    if command == "login":
        authenticate(user, pwd)
    elif command == "verify":
        if len(sys.argv) < 5:
            print("Missing 2FA code")
            sys.exit(1)
        code = sys.argv[4]
        validate_2fa(user, pwd, code)
    else:
        print("Unknown command")
