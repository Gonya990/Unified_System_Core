
import json

import requests


def find_school(query):
    url = "https://web.mashov.info/api/schools"
    try:
        res = requests.get(url)
        schools = res.json()
        print(f"Total schools: {len(schools)}")

        matches = []
        for s in schools:
            # Search in all string values
            found_key = False
            for k, v in s.items():
                 if isinstance(v, str) and query in v:
                     found_key = True
            if found_key:
                matches.append(s)

        return matches
    except Exception as e:
        print(e)
        return []

if __name__ == "__main__":
    q = "ביאליק" # Kiryat Bialik
    print(f"--- Searching for {q} ---")
    found = find_school(q)
    for f in found:
        print(f"Symbol: {f['semel']}, Name: {f['name']}")

    # Also Check Psagot specifically to see structure
    print("--- Psagot Structure ---")
    for s in find_school("פסגות"):
         if "316" in str(s['semel']): # Random guess or just first one
             pass # just print first
    # Just print first Psagot found match
    psagots = find_school("פסגות")
    if psagots:
        print(json.dumps(psagots[0], ensure_ascii=False))
