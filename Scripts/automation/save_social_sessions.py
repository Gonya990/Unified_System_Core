import json
import os
from pathlib import Path

# Paths to store browser session data for the cloud node
REMOTE_SESSION_DIR = Path("/Users/igorgoncharenko/Documents/Unified_System_Core/Secrets/Browser_Sessions")
REMOTE_SESSION_DIR.mkdir(parents=True, exist_ok=True)

vk_cookies = [
    {"name": "remixnttpid", "value": "vk1.a.dSAPkERvdRlQHNK_pUDs08G2qObKiKXWr5isZoH7cE-YdVYKR2tS44EN7YPcb0aE0Jq6nv9M24Q7Yt5rzmtt5pmhknt5UwB_1GuPSWhkwgGGEu8EtJxk_G2DBc6rQpi8HumWJNHTuc8ku9YagdNF69xDCOP0RlyoRZG96L05MGRzVwNm1fLf6m4u7lUtvda_", "domain": ".vk.com", "path": "/"},
    {"name": "remixsid", "value": "1_85GPdi8vmTtAv0KPEGEp51WWcds4vjL7bTuEkXXozYQsBb8_XzlI7QCcthUsAt32uXM3AFWZVlLqCizYjyil2w", "domain": ".vk.com", "path": "/"}
]

fb_cookies = [
    {"name": "c_user", "value": "100001001089589", "domain": ".facebook.com", "path": "/"},
    {"name": "xs", "value": "8%3Aa5sNv-YeGygySA%3A2%3A1769119344%3A-1%3A-1%3AxC0-fs0_2mwvxQ%3AAczg7PcbN9m8O-BlD-8WEjU8XJt7Yb90YyvryIQA7g", "domain": ".facebook.com", "path": "/"}
]

def save_cookies():
    with open(REMOTE_SESSION_DIR / "vk_cookies.json", "w") as f:
        json.dump(vk_cookies, f, indent=2)
    with open(REMOTE_SESSION_DIR / "fb_cookies.json", "w") as f:
        json.dump(fb_cookies, f, indent=2)
    print(f"✅ Cookies saved to {REMOTE_SESSION_DIR}")

if __name__ == "__main__":
    save_cookies()
