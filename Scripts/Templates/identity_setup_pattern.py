#!/usr/bin/env python3
"""
Identity Setup Pattern for Unified System
-----------------------------------------
This script demonstrates the secure pattern for establishing "Agent Awareness"
of detailed human identities (Family/Team) WITHOUT leaking sensitive data to git.

USE CASE:
Give your local Agent context about who is who (Real Name <-> System ID),
so it can intelligently route messages, manage permissions, or understand
"Child Accounts" (Agent Identities), strictly on the host machine.

INSTRUCTIONS FOR KOSTYA/COUNCIL:
1. Run this script locally on the node where the Agent operates.
2. Input the real-world identities of your circle.
3. The script generates a `secrets/family_map.json` file.
4. Ensure `secrets/` is in `.gitignore`.

SECURITY:
- Data is stored in JSON.
- Never commit the output JSON.
- This creates a "Local Truth" for the Agent.
"""

import json
import os

# Configuration
SECRETS_DIR = "secrets"
OUTPUT_FILE = os.path.join(SECRETS_DIR, "identity_map.json")


def ensure_secrets_dir():
    if not os.path.exists(SECRETS_DIR):
        print(f"Creating {SECRETS_DIR} directory...")
        os.makedirs(SECRETS_DIR)
        # Verify it's ignored (suggested check)
        print(f"⚠️  IMPORTANT: Ensure '{SECRETS_DIR}/' is added to your .gitignore!")


def get_input(prompt):
    return input(prompt).strip()


def main():
    print("=== 🛡️  Secure Identity Setup (Local Context) 🛡️  ===")
    print("This utility creates a local map of human identities for the AI System.")

    ensure_secrets_dir()

    structure = {
        "manager": {},
        "members": [],
        "meta_layer": {"description": "Local Identity Map", "security_policy": "LOCAL_ONLY"},
    }

    print("\n--- 👑 Manager (You) ---")
    structure["manager"]["name"] = get_input("Enter your full real name: ")
    structure["manager"]["role"] = "admin"
    structure["manager"]["system_id"] = "root_admin"

    print("\n--- 👥 Members (Family/Team) ---")
    while True:
        choice = get_input("Add a member? (y/n): ").lower()
        if choice != "y":
            break

        print("adding member...")
        name = get_input("  Name: ")
        role = get_input("  Role (parent/member/child/ally): ")
        sys_id = get_input("  System ID (e.g., agent_arthur, trusted_ally_bob): ")

        member = {"name": name, "role": role, "system_id": sys_id}
        structure["members"].append(member)
        print("  ✅ Member added.")

    # Save
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(structure, f, indent=2, ensure_ascii=False)

    print(f"\n🎉 Success! Identity Map saved to: {OUTPUT_FILE}")
    print("Your Agent now has local awareness of these identities without API calls.")
    print("DO NOT COMMIT THIS FILE.")


if __name__ == "__main__":
    main()
