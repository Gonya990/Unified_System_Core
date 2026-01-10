
import os
import sys
import logging
import requests
import json
from pathlib import Path

# Setup Paths
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(ROOT_DIR))

# Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("MashovLogin")

# MASHOV CONFIG
# TODO: User to fill this or provide via ENV
MASHOV_URL = "https://web.mashov.info/api"
SCHOOL_SYMBOL = 0 # Replace with School ID
YEAR = 2026

def login_mashov(username, password, school_id):
    """
    Attempt to login to Mashov.
    Returns session cookie or token.
    """
    logger.info(f"Attempting login for user {username} at school {school_id}...")
    
    # 1. Get Schools (Optional, to verify symbol)
    # schools_url = "https://web.mashov.info/api/schools"
    # ...
    
    # 2. Login
    login_url = f"{MASHOV_URL}/login"
    payload = {
        "username": username,
        "password": password,
        "semel": school_id,
        "year": YEAR
    }
    
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        session = requests.Session()
        res = session.post(login_url, json=payload, headers=headers)
        
        if res.status_code == 200:
            logger.info("Login Successful!")
            # Extract token/simbol/uniqueid
            # Note: Mashov API changes properly. This is a generic robust attempt.
            data = res.json()
            return session, data
        else:
            logger.error(f"Login Failed: {res.status_code} - {res.text}")
            return None, None
            
    except Exception as e:
        logger.error(f"Connection Error: {e}")
        return None, None

if __name__ == "__main__":
    # Test Credentials (ENV or Hardcoded for test)
    user = os.getenv("MASHOV_USER", "PLACEHOLDER")
    pwd = os.getenv("MASHOV_PASS", "PLACEHOLDER")
    school = os.getenv("MASHOV_SCHOOL", "0")
    
    if user == "PLACEHOLDER":
        print("❌ Please set MASHOV_USER, MASHOV_PASS, MASHOV_SCHOOL env vars or edit script.")
    else:
        log, data = login_mashov(user, pwd, school)
        if log:
            print("✅ Mashov Test Passed.")
            print(data)
