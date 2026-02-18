import json
import os


def fix_chromium_ide():
    path = "/Users/igorgoncharenko/.antigravity/extensions/google.cros-ide-0.50.0-universal/package.json"
    if not os.path.exists(path):
        print(f"⚠️ {path} not found")
        return

    with open(path) as f:
        data = json.load(f)

    # Remove activation events to satisfy IDE
    if "activationEvents" in data:
        print(f"  → Cleaning up activationEvents in {path}")
        data["activationEvents"] = [] # Clear them for now

    with open(path, 'w') as f:
        json.dump(data, f, indent=4)

    print("✅ Fixed ChromiumIDE activation events.")

if __name__ == "__main__":
    fix_chromium_ide()
