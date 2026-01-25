import os
import re

patterns = [
    r'AIzaSy[A-Za-z0-9_-]{33}', # Google API Key
    r'sk-[A-Za-z0-9]{48}',       # OpenAI Key
    r'xox[bap]-[0-9]{12}-[0-9]{12}-[A-Za-z0-9]{24}', # Slack
    r'ghp_[A-Za-z0-9]{36}',      # GitHub PAT
    r'sq0csp-[A-Za-z0-9_-]{43}', # Square
    r'access_token$[A-Za-z0-9_-]{40}', # Instagram/FB
]

def scan_files():
    for root, dirs, files in os.walk('.'):
        if any(d in root for d in ['.git', 'venv', 'node_modules']): continue
        for file in files:
            if file.endswith(('.py', '.sh', '.json', '.txt', '.env')):
                path = os.path.join(root, file)
                try:
                    with open(path, 'r', errors='ignore') as f:
                        content = f.read()
                        for p in patterns:
                            matches = re.findall(p, content)
                            if matches:
                                print(f"FOUND in {path}: {matches}")
                except: pass

scan_files()
