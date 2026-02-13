import os

from dotenv import load_dotenv
from pybit.unified_trading import HTTP

load_dotenv("/Users/igorgoncharenko/Documents/Unified_System_Core/Projects/AI_Core/.env")

API_KEY = os.getenv("BYBIT_API_KEY")
API_SECRET = os.getenv("BYBIT_API_SECRET")


def check_balances():
    session = HTTP(testnet=False, api_key=API_KEY, api_secret=API_SECRET)

    account_types = ["UNIFIED", "FUNDING", "SPOT"]

    print("--- BYBIT BALANCE CHECK ---")

    for acc in account_types:
        try:
            print(f"\nChecking {acc}...")
            if acc == "FUNDING":
                result = session.get_coins_balance(accountType=acc)
            else:
                result = session.get_wallet_balance(accountType=acc)

            if result["retCode"] == 0:
                print(f"Success! {acc} Data:")
                # Simplified output
                if acc == "FUNDING":
                    for item in result["result"]["rows"]:
                        if float(item.get("walletBalance", 0)) > 0 or float(item.get("balance", 0)) > 0:
                            print(f"  - {item['coin']}: {item.get('walletBalance') or item.get('balance')}")
                else:
                    for item in result["result"]["list"]:
                        for coin in item.get("coin", []):
                            if float(coin.get("walletBalance", 0)) > 0:
                                print(f"  - {coin['coin']}: {coin['walletBalance']}")
            else:
                print(f"Error {acc}: {result['retMsg']}")
        except Exception as e:
            print(f"Exception for {acc}: {e}")


if __name__ == "__main__":
    check_balances()
