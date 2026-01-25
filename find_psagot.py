import json

import requests

url = "https://web.mashov.info/api/schools"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "X-Mashov-Client": "Web",
}
resp = requests.get(url, headers=headers)
schools = resp.json()

search_terms = ["כרמיאל", "פסגות", "Psagot", "Carmiel", "213033", "244103", "244285"]

results = []
for s in schools:
    name = s.get("name", "")
    semel = str(s.get("semel", ""))
    if any(term in name for term in search_terms) or any(term in semel for term in search_terms):
        results.append(s)

print(json.dumps(results, indent=2, ensure_ascii=False))
