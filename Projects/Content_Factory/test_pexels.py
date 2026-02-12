import os
from pathlib import Path

import requests
from dotenv import load_dotenv

ROOT_DIR = Path('/home/gonya/Unified_System_Core')
load_dotenv(ROOT_DIR / '.env')
load_dotenv(ROOT_DIR / 'Projects/AI_Core/.env', override=True)

api_key = os.getenv('PEXELS_API_KEY')
print(f'Using key: {api_key[:10]}...')

url = 'https://api.pexels.com/v1/search?query=business&per_page=1'
headers = {'Authorization': api_key}

try:
    response = requests.get(url, headers=headers)
    print(f'Status: {response.status_code}')
    if response.status_code == 200:
        print('✅ Pexels API Key is VALID and working!')
        print(f'Result: {response.json()["photos"][0]["url"]}')
    else:
        print(f'❌ Pexels API Error: {response.text}')
except Exception as e:
    print(f'❌ Connection Error: {e}')
