import os
import sys

from pyicloud import PyiCloudService

SESSION_DIR = os.path.expanduser("~/.icloud_session")

def check_status(username, password):
    print(f"🍏 Checking iCloud status for {username}...")
    try:
        api = PyiCloudService(username, password, cookie_directory=SESSION_DIR)

        if api.requires_2fa:
            print("⚠️ 2FA still required.")
            return False

        print(f"✅ Authenticated as: {api.user['data']['fullName']}")

        # Try to list devices to prove access
        devices = api.devices
        print(f"📱 Devices found: {len(devices)}")
        for dev in list(devices.keys())[:3]: # Show first 3 IDs keys
             print(f" - {dev}")

        return True

    except Exception as e:
        print(f"❌ Check Error: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 icloud_check.py <username> <password>")
        sys.exit(1)

    check_status(sys.argv[1], sys.argv[2])
