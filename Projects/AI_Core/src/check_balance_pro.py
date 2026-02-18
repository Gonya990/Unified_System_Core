import os
import sys
from pybit.unified_trading import HTTP

# Add src to path for TokenBroker
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from token_broker import TokenBroker

def check_balances():
    broker = TokenBroker()
    # In TokenBroker key_store, 'bybit' is a list
    bybit_data = broker.key_store.get("bybit", [{}])[0]
    api_key = bybit_data.get("key")
    api_secret = bybit_data.get("secret")
    
    if not api_key or not api_secret:
        print("❌ Bybit keys not found in TokenBroker!")
        return

    session = HTTP(testnet=False, api_key=api_key, api_secret=api_secret)

    account_types = ["UNIFIED", "FUNDING", "SPOT"]

    print("--- BYBIT BALANCE CHECK (PRO) ---")
    print(f"Using Key: {api_key[:5]}...")

    for acc in account_types:
        try:
            print(f"\nChecking {acc}...")
            if acc == "FUNDING":
                result = session.get_coins_balance(accountType=acc)
            else:
                result = session.get_wallet_balance(accountType=acc)

            if result["retCode"] == 0:
                print(f"✅ Success! {acc} Data:")
                found = False
                if acc == "FUNDING":
                    for item in result["result"].get("rows", []):
                        balance = float(item.get("walletBalance") or item.get("balance") or 0)
                        if balance > 0:
                            print(f"  - {item['coin']}: {balance}")
                            found = True
                else:
                    for item in result["result"].get("list", []):
                        for coin in item.get("coin", []):
                            balance = float(coin.get("walletBalance", 0))
                            if balance > 0:
                                print(f"  - {coin['coin']}: {balance}")
                                found = True
                if not found:
                    print("  - No balance found.")
            else:
                print(f"❌ Error {acc}: {result['retMsg']} (Code: {result['retCode']})")
        except Exception as e:
            print(f"⚠️ Exception for {acc}: {e}")

if __name__ == "__main__":
    check_balances()
