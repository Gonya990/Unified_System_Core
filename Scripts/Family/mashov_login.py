
import logging
import os
import sys
from pathlib import Path

import requests

# Setup Paths
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(ROOT_DIR))

try:
    from dotenv import load_dotenv
    load_dotenv(ROOT_DIR / ".env")
except ImportError:
    pass

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
            data = res.json()
            # Mashov usually returns a user object. We need the student's UUID/ID.
            # Structure usually: { "credential": { "userId": "...", ... }, "accessToken": "..." }
            # But let's return the whole data for inspection on first run.
            return session, data
        else:
            logger.error(f"Login Failed: {res.status_code} - {res.text}")
            return None, None

    except Exception as e:
        logger.error(f"Connection Error: {e}")
        return None, None

def fetch_grades(session, user_id):
    """Fetch recent grades"""
    url = f"{MASHOV_URL}/students/{user_id}/grades"
    try:
        res = session.get(url)
        if res.status_code == 200:
            return res.json()
        return []
    except:
        return []

def fetch_homework(session, user_id):
    """Fetch pending homework"""
    url = f"{MASHOV_URL}/students/{user_id}/homework"
    try:
        res = session.get(url)
        if res.status_code == 200:
            return res.json()
        return []
    except:
        return []

def get_all_schools():
    """Fetch all schools from Mashov API"""
    try:
        res = requests.get(f"{MASHOV_URL}/schools")
        if res.status_code == 200:
            return res.json()
        return []
    except Exception as e:
        logger.error(f"Failed to fetch schools: {e}")
        return []

def search_school(query):
    """Search for a school by name"""
    schools = get_all_schools()
    return [s for s in schools if query in s['name']]

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Mashov Login & Test")
    parser.add_argument("--user", help="Username", default=os.getenv("MASHOV_USER"))
    parser.add_argument("--pwd", help="Password", default=os.getenv("MASHOV_PASS"))
    parser.add_argument("--school", help="School Symbol", default=os.getenv("MASHOV_SCHOOL"))
    parser.add_argument("--search", help="Search string for school name")
    
    args = parser.parse_args()

    if args.search:
        results = search_school(args.search)
        print(f"🔍 Found {len(results)} schools matching '{args.search}':")
        for s in results:
            print(f"  🏫 {s['name']} (Symbol: {s['semel']}) - Years: {s.get('years')}")
        sys.exit(0)

    if not args.user or not args.pwd:
        print("❌ Please provide user/pass via --user/--pwd or .env")
        sys.exit(1)
    
    school_id = args.school
    if not school_id or school_id == "0":
        # Try to guess or ask? For now, fail.
        print("❌ School Symbol required. Use --search to find it.")
        sys.exit(1)

    log, data = login_mashov(args.user, args.pwd, int(school_id))
    if log:
        print("✅ Mashov Login Successful!")
        print(f"Student Data: {json.dumps(data, indent=2, ensure_ascii=False)}")
        
        # Try fetching grades
        if 'credential' in data:
            uid = data['credential'].get('userId')
            if uid:
                print("\n📊 Fetching Grades...")
                grades = fetch_grades(log, uid)
                print(f"Found {len(grades)} grades.")
                if grades:
                    print(grades[:5]) # Show first 5
    else:
        print("❌ Login Failed.")
