from token_broker import TokenBroker


def dump_keys():
    broker = TokenBroker()
    # Let's try to list all keys in the vault
    # Since TokenBroker might not have a 'list_keys' method,
    # we'll look at its implementation or try common keys.
    keys_to_try = [
        "bybit_api_key", "bybit_api_secret",
        "telegram_bot_token", "admin_chat_id",
        "openai_api_key", "gemini_api_key",
        "github_token", "pexels_api_key",
        "elevenlabs_api_key"
    ]

    print("--- VAULT KEY DUMP ---")
    for key in keys_to_try:
        val = broker.get_key(key)
        if val:
            print(f"{key}: {val[:5]}...{val[-5:]}")
        else:
            print(f"{key}: NOT FOUND")

if __name__ == "__main__":
    dump_keys()
