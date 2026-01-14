import logging

import requests

logging.basicConfig(level=logging.INFO)
MASHOV_URL = "https://web.mashov.info/api"


def find_school_advanced():
    print("Fetch schools...")
    res = requests.get(f"{MASHOV_URL}/schools")
    schools = res.json()

    matches = []
    carmiel_schools = []

    for s in schools:
        name = s.get("name", "")
        semel = s.get("semel", "")

        # 1. Broad Carmiel capture
        if "כרמיאל" in name:
            carmiel_schools.append(s)

        # 2. Specific 'Ort' check
        if "אורט" in name and "כרמיאל" in name:
            matches.append(s)

        # 3. Check for specific IDs mentioned
        if "244368" in str(semel):
            print(f"!!! FOUND HIDDEN 244368: {name}")

    print(f"\n--- Found {len(carmiel_schools)} schools in Carmiel ---")
    for m in carmiel_schools:
        print(f"{m['semel']} - {m['name']}")

    print(f"\n--- ORT Carmiel Candidates ({len(matches)}) ---")
    for m in matches:
        print(f"-> {m['semel']} - {m['name']}")


if __name__ == "__main__":
    find_school_advanced()
