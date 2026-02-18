import sys

# Add paths for TokenBroker
sys.path.insert(0, "/Users/igorgoncharenko/Documents/Unified_System_Core/Projects/AI_Core/src")
from token_broker import TokenBroker


def add_telegram_token():
    broker = TokenBroker()

    # Decrypt current store
    store = broker.key_store

    # Add telegram
    store['telegram'] = [{
        'key': '8518131338:AAFQJFjzEIEGVd7_6ER9aKcGB5Gcylade8I',
        'alias': 'GonyaHomeBot-Main',
        'tier': 'pro'
    }]

    # Save back to encrypted vault
    broker.save_vault(store)
    print("✅ Telegram token added to encrypted vault.")

if __name__ == "__main__":
    add_telegram_token()
