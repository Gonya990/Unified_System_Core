#!/usr/bin/env python3
import json
import logging

import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MashovExplorer")


def find_school(query):
    url = "https://web.mashov.info/api/schools"
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "X-Mashov-Client": "Web",
        }
        resp = requests.get(url, headers=headers)
        schools = resp.json()

        matches = [s for s in schools if query in str(s.get("name", "")) or query in str(s.get("semel", ""))]
        return matches
    except Exception as e:
        logger.error(f"Failed to fetch schools: {e}")
        return []


if __name__ == "__main__":
    import sys

    search = sys.argv[1] if len(sys.argv) > 1 else "7490303"
    results = find_school(search)
    print(json.dumps(results, indent=2, ensure_ascii=False))
