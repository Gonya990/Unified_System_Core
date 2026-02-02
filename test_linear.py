import os

import requests
from dotenv import load_dotenv

load_dotenv('/Users/igorgoncharenko/Documents/Unified_System_Core/Projects/AI_Core/.env')

token = os.getenv('LINEAR_API_KEY')
print(f"Testing Linear Token: {token[:4]}...{token[-4:] if token else ''}")

query = '{ viewer { id name email } }'
url = 'https://api.linear.app/graphql'
headers = {"Content-Type": "application/json", "Authorization": token}

r = requests.post(url, headers=headers, json={'query': query})
if r.status_code == 200:
    print("Linear Success!")
    print(r.json())
else:
    print(f"Linear Failed: {r.status_code}")
    print(r.text)
