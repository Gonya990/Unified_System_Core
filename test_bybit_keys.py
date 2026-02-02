
import os

from dotenv import load_dotenv
from pybit.unified_trading import HTTP

env_path = '/home/gonya/Unified_System_Core/Projects/AI_Core/.env'
load_dotenv(env_path)

api_key = os.getenv('BYBIT_API_KEY')
api_secret = os.getenv('BYBIT_API_SECRET')

for is_testnet in [True, False]:
    print(f"--- TESTING {'TESTNET' if is_testnet else 'MAINNET'} ---")
    try:
        session = HTTP(
            testnet=is_testnet,
            api_key=api_key,
            api_secret=api_secret,
        )
        result = session.get_wallet_balance(accountType="UNIFIED")
        if 'result' in result and 'list' in result['result']:
            for acc in result['result']['list']:
                total_equity = acc.get('totalEquity', '0')
                print(f"  Total Equity: {total_equity}")
        else:
            print(f"  No balance info for {'TESTNET' if is_testnet else 'MAINNET'}")
    except Exception as e:
        print(f"  Query failed: {e}")
