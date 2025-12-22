
import os
import csv
import datetime
import re

ROOT_DIR = "/home/gonya"
OUTPUT_FILE = os.path.join(ROOT_DIR, "00_NAV/INVENTORY.csv")

# Directories to exclude from scanning (System & Output folders)
EXCLUDE_DIRS = {
    "00_NAV", "01_Projects", "02_Shared", "03_Operations", 
    "90_Inbox_ToSort", "99_Archive_Original",
    "node_modules", "__pycache__", "dist", "build",
    ".git", ".vscode", ".vscode-server", ".cache", ".local", 
    ".config", ".ssh", ".npm", ".nvm", "miniconda3", "snap", 
    ".venv", ".gemini", ".homeassistant", ".node-red", "ha_env", 
    "tuya_env", "ml_env", "ha_condavenv", "ha_venv", "lib", "bin"
}

# Files to exclude (System files)
EXCLUDE_FILES = {
    ".bashrc", ".profile", ".bash_history", ".bash_logout", ".wget-hsts",
    ".sudo_as_admin_successful", "ha.log"
}

PROJECT_PATTERNS = [
    ("PRJ-001_HomeAssistant", r"(ha_|homeassistant|hass|dashboard_|secrets\.yaml|verify_config|energy_|backup_|hubs_|paradox_|zigbee|mosquitto)"),
    ("PRJ-002_Tuya_IoT", r"(tuya|tinytuya|scan_|broadlink|monitor_|find_|sonoff|tasmota|smartthings|get_tuya)"),
    ("PRJ-003_N8N_Automation", r"(n8n|nodered|workflow|flow_)"),
    ("PRJ-004_AI_Agents", r"(llm|agent|ollama|codex|copilot|browser_agent)"),
    ("PRJ-005_Media_TV", r"(tv_|dlna|cast|android_tv|airplay|remote_|channel)"),
]

def get_file_info(filepath):
    stat = os.stat(filepath)
    size = stat.st_size
    mtime = datetime.datetime.fromtimestamp(stat.st_mtime).isoformat()
    return size, mtime

def guess_project(filename):
    lower_name = filename.lower()
    best_match = None
    
    for project, pattern in PROJECT_PATTERNS:
        if re.search(pattern, lower_name):
            return project, 0.9 # High confidence based on keyword
            
    return "UNKNOWN", 0.0

def main():
    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['path', 'filename', 'ext', 'size', 'modified_time', 'guessed_project', 'confidence', 'guessed_category', 'notes']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for root, dirs, files in os.walk(ROOT_DIR):
            # Modify dirs in-place to skip excluded directories
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith('.')]
            
            # Special check: Do not exclude hidden *files* if they are relevant (user said no .git, but maybe .env?)
            # But for safety in root, ignore all starting with .
            
            for name in files:
                if name.startswith('.') or name in EXCLUDE_FILES:
                    continue
                    
                filepath = os.path.join(root, name)
                rel_path = os.path.relpath(filepath, ROOT_DIR)
                
                # Double check we are not in an excluded dir (os.walk modifies dirs BUT for the current root it might be one)
                parts = rel_path.split(os.sep)
                if any(p in EXCLUDE_DIRS or p.startswith('.') for p in parts[:-1]):
                    continue

                ext = os.path.splitext(name)[1]
                try:
                    size, mtime = get_file_info(filepath)
                    project, confidence = guess_project(name)
                    
                    category = "Doc" if ext in ['.md', '.txt', '.pdf', '.csv'] else "Code"
                    
                    writer.writerow({
                        'path': rel_path,
                        'filename': name,
                        'ext': ext,
                        'size': size,
                        'modified_time': mtime,
                        'guessed_project': project,
                        'confidence': confidence,
                        'guessed_category': category,
                        'notes': ''
                    })
                except Exception as e:
                    print(f"Error processing {filepath}: {e}")

if __name__ == "__main__":
    main()
