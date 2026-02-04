
import os
import sys
from pathlib import Path
import importlib.util

def is_lib_installed(name):
    return importlib.util.find_spec(name) is not None

# Try to load dotenv
try:
    from dotenv import load_dotenv
except ImportError:
    print("❌ python-dotenv not installed. Please run: pip install python-dotenv")
    sys.exit(1)

# Paths
ROOT_DIR = Path("/Users/igorgoncharenko/Documents/Unified_System_Core")
ENV_PATH = ROOT_DIR / "Projects/AI_Core/.env"

if not ENV_PATH.exists():
    print(f"❌ .env not found at {ENV_PATH}")
    # Try looking in current directory just in case
    ENV_PATH = Path(".env")
    if not ENV_PATH.exists():
         print("❌ No .env found.")
else:
    print(f"✅ Found .env at {ENV_PATH}")

load_dotenv(ENV_PATH)

def check_openai():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key: return "SKIPPED (No OPENAI_API_KEY in .env)"
    
    if not is_lib_installed("openai"): return "SKIPPED (openai library missing)"
    
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        # Quick robust check
        client.models.list()
        return "✅ OK"
    except Exception as e:
        return f"❌ FAILED: {str(e)}"

def check_gemini():
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key: return "SKIPPED (No GEMINI_API_KEY or GOOGLE_API_KEY)"
    
    if not is_lib_installed("google.generativeai"): return "SKIPPED (google-generativeai library missing)"

    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        # List models to verify access
        list(genai.list_models())
        return "✅ OK"
    except Exception as e:
        return f"❌ FAILED: {str(e)}"

def check_telegram():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token: return "SKIPPED (No TELEGRAM_BOT_TOKEN)"
    
    if not is_lib_installed("requests"): return "SKIPPED (requests library missing)"

    try:
        import requests
        response = requests.get(f"https://api.telegram.org/bot{token}/getMe", timeout=10)
        if response.status_code == 200:
            data = response.json()
            bot_name = data.get('result', {}).get('username', 'Unknown')
            return f"✅ OK (Bot: @{bot_name})"
        else:
            return f"❌ FAILED (Status: {response.status_code})"
    except Exception as e:
        return f"❌ FAILED: {str(e)}"

def check_bybit():
    key = os.getenv("BYBIT_API_KEY")
    secret = os.getenv("BYBIT_API_SECRET")
    if not key or not secret: return "SKIPPED (No BYBIT_API_KEY/SECRET)"
    
    if not is_lib_installed("pybit"): return "SKIPPED (pybit library missing)"

    try:
        from pybit.unified_trading import HTTP
        session = HTTP(testnet=False, api_key=key, api_secret=secret)
        # Just check server time or something simple that requires auth if possible,
        # otherwise basic connectivity
        # get_wallet_balance requires auth
        session.get_wallet_balance(accountType="UNIFIED")
        return "✅ OK"
    except Exception as e:
        # Check if error is related to authentication
        return f"❌ FAILED: {str(e)}"

def check_github():
    token = os.getenv("GITHUB_TOKEN") or os.getenv("GITHUB_ACCESS_TOKEN")
    if not token: return "SKIPPED (No GITHUB_TOKEN)"
    
    if not is_lib_installed("requests"): return "SKIPPED (requests library missing)"

    try:
        import requests
        headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
        response = requests.get("https://api.github.com/user", headers=headers, timeout=10)
        if response.status_code == 200:
            user = response.json().get('login', 'Unknown')
            return f"✅ OK (User: {user})"
        else:
            return f"❌ FAILED (Status: {response.status_code})"
    except Exception as e:
        return f"❌ FAILED: {str(e)}"

print("\n════════════════════════════════════════════════════════════")
print("   🔍 SYSTEM KEY VERIFICATION")
print("════════════════════════════════════════════════════════════")
print(f"OpenAI:   {check_openai()}")
print(f"Gemini:   {check_gemini()}")
print(f"Telegram: {check_telegram()}")
print(f"Bybit:    {check_bybit()}")
print(f"GitHub:   {check_github()}")
print("════════════════════════════════════════════════════════════\n")
