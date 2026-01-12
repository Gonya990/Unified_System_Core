#!/usr/bin/env python3
import requests
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MashovExplorer")

def find_school(query):
    url = f"https://web.mashov.info/api/login/schools"
    try:
        resp = requests.get(url)
        schools = resp.json()
        
        matches = [s for s in schools if query in str(s.get('name', '')) or query in str(s.get('semel', ''))]
        return matches
    except Exception as e:
        logger.error(f"Failed to fetch schools: {e}")
        return []

if __name__ == "__main__":
    import sys
    search = sys.argv[1] if len(sys.argv) > 1 else "7490303"
    results = find_school(search)
    print(json.dumps(results, indent=2, ensure_ascii=False))
