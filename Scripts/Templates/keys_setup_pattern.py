
import json
import os
import sys

# Define path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SECRETS_DIR = os.path.join(BASE_DIR, "secrets")
KEYS_FILE = os.path.join(SECRETS_DIR, "keys.json")

def ensure_secrets_dir():
    if not os.path.exists(SECRETS_DIR):
        print(f"Creating secrets directory: {SECRETS_DIR}")
        os.makedirs(SECRETS_DIR)

def get_input(prompt, default=None):
    if default:
        user_input = input(f"{prompt} [{default}]: ")
        return user_input if user_input else default
    return input(f"{prompt}: ")

def main():
    print("=== 🔐 Resource Key Setup (Local Vault) 🔐 ===")
    print("This utility creates a secure local map of API Keys for the Family Swarm.")
    print("Keys are stored in 'secrets/keys.json' and are NOT committed to Git.\n")

    ensure_secrets_dir()

    # Load existing if available
    current_data = {"gemini": [], "openai": [], "claude": [], "other": []}
    if os.path.exists(KEYS_FILE):
         try:
            with open(KEYS_FILE, 'r') as f:
                current_data = json.load(f)
            print(f"✅ Found existing keys file with {sum(len(v) for v in current_data.values())} keys.")
         except:
            print("⚠️ Existing file corrupted, starting fresh.")

    while True:
        print("\n--- Providers ---")
        print("1. Gemini (Google)")
        print("2. OpenAI (GPT)")
        print("3. Claude (Anthropic)")
        print("4. Other")
        print("5. Save & Exit")
        
        choice = get_input("\nSelect Provider (1-5)")
        
        if choice == '5':
            break
            
        provider_map = {'1': 'gemini', '2': 'openai', '3': 'claude', '4': 'other'}
        provider = provider_map.get(choice)
        
        if not provider:
            print("Invalid choice.")
            continue
            
        print(f"\nAdding key for {provider.upper()}...")
        alias = get_input("  Key Alias (e.g., 'Igor_Primary', 'Child_Account')", "My_Key")
        key_value = get_input("  API Key Value (sk-...)")
        
        if not key_value:
            print("❌ Skipped empty key.")
            continue

        # Add to list
        new_entry = {
            "alias": alias,
            "key": key_value,
            "tier": get_input("  Tier (free/paid/high-throughput)", "free"),
            "owner": get_input("  Owner Name (for billing)", "Igor")
        }
        
        # Check duplicates
        # Simple list append for now, can be sophisticated later
        current_data[provider].append(new_entry)
        print("  ✅ Key added to pool.")

    # Save
    print(f"\n💾 Saving to {KEYS_FILE}...")
    with open(KEYS_FILE, 'w') as f:
        json.dump(current_data, f, indent=2)
    
    print("Done! The TokenBroker can now use these keys.")

if __name__ == "__main__":
    main()
