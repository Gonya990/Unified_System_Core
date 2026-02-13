import os

import yaml

ROOT_DIR = "/home/gonya"
NAV_DIR = os.path.join(ROOT_DIR, "00_NAV")
PLAN_FILE = os.path.join(NAV_DIR, "MIGRATION_PLAN.md")
PROJECTS_FILE = os.path.join(NAV_DIR, "PROJECTS.yaml")

# Load Projects
with open(PROJECTS_FILE) as f:
    config = yaml.safe_load(f)
    PROJECTS = {p["id"]: p for p in config["projects"]}

# Regex helpers (simplified/duplicated from inventory but applied to Top Level items)
import re

PATTERNS = [
    (
        "PRJ-001",
        r"^(ha_|hass|homeassistant|dashboard_|secrets\.yaml|verify_config|energy_|backup_|hubs_|paradox_|zigbee|wyoming|\.homeassistant)",
    ),
    ("PRJ-002", r"^(tuya|tinytuya|scan_|broadlink|monitor_|find_|sonoff|tasmota|smartthings|get_tuya|matter-data)"),
    ("PRJ-003", r"^(n8n|nodered|node_red|workflow|flow_|\.node-red)"),
    ("PRJ-004", r"^(llm-council|ollama|codex|copilot|browser_agent)"),
    ("PRJ-005", r"^(tv_|dlna|cast|android_tv|airplay|remote_|channel)"),
    ("PRJ-006", r"^(opencode)"),
]

# Items to ignore (System)
IGNORE_NAMES = {
    "00_NAV",
    "01_Projects",
    "02_Shared",
    "03_Operations",
    "90_Inbox_ToSort",
    "99_Archive_Original",
    "node_modules",
    ".git",
    ".vscode",
    ".vscode-server",
    ".cache",
    ".local",
    ".config",
    ".ssh",
    ".npm",
    ".nvm",
    "miniconda3",
    "snap",
    ".venv",
    ".gemini",
    ".bashrc",
    ".profile",
    ".bash_history",
    ".bash_logout",
    ".wget-hsts",
    ".sudo_as_admin_successful",
    ".pki",
    ".fluxbox",
    ".lesshst",
    ".conda",
    ".docker",
    ".docker-temp",
    ".dotnet",
    ".factory",
    ".iec_diag",
    ".kube",
    ".landscape",
    ".minikube",
    ".motd_shown",
    ".nv",
    ".redhat",
    ".che",
    ".antigravity-server",
    ".aws",
    ".azure",
    ".bun",
    ".codex",
    ".copilot",
    ".fehbg",
    ".ollama",
    "bin",
    "lib",
}


def guess(name):
    name_lower = name.lower()
    for pid, pattern in PATTERNS:
        if re.search(pattern, name_lower):
            return pid
    # Specific file overrides
    if name in ["install.sh", "miniconda.sh", "gpu-op-install.log"]:
        return "SHARED_INSTALLERS"
    if name.endswith(".log"):
        return "LOGS"
    return "UNKNOWN"


def main():
    migration_steps = []

    # Get top level items
    try:
        items = os.listdir(ROOT_DIR)
    except PermissionError:
        print("Permission error reading root")
        return

    for item in sorted(items):
        if item in IGNORE_NAMES:
            continue

        # Determine strict type
        full_path = os.path.join(ROOT_DIR, item)
        is_dir = os.path.isdir(full_path)

        pid = guess(item)

        source = item
        target = ""
        reason = ""

        if pid in PROJECTS:
            prj = PROJECTS[pid]
            base = prj["path"]

            # Determine subfolder
            if is_dir:
                # If it's a main folder like 'hass' or 'n8n', maybe keep it as root of project or move to 02_Dev?
                # User wants standard structure.
                # If 'hass' -> PRJ-001/02_Dev/hass_config ? Or just PRJ-001/hass ?
                # Let's put directories in 02_Dev if they are code/data, or root of project?
                # To minimize nesting hell, let's put:
                # 'hass' -> PRJ-001/hass (Directly in project root) - Actually user said "Standard subfolders".
                # If I put it in 02_Dev, it's cleaner.
                target = f"{base}/02_Dev/{item}"
            else:
                # File
                ext = os.path.splitext(item)[1].lower()
                if ext in [".md", ".txt", ".pdf", ".csv", ".doc", ".docx", ".odt"]:
                    target = f"{base}/01_Docs/{item}"
                elif ext in [".yaml", ".json", ".py", ".js", ".sh", ".ini", ".cfg", ".db", ".log"]:
                    target = f"{base}/02_Dev/{item}"
                elif ext in [".jpg", ".png", ".svg"]:
                    target = f"{base}/03_Design/{item}"
                else:
                    target = f"{base}/02_Dev/{item}"  # Fallback to dev

            reason = f"Matched Project {pid}"

        elif pid == "SHARED_INSTALLERS":
            target = f"02_Shared/Installers/{item}"
            reason = "Installer/Script"

        elif pid == "LOGS":
            target = f"90_Inbox_ToSort/LOGS/{item}"
            reason = "Log file, needs review"

        else:
            # Unknown
            target = f"90_Inbox_ToSort/NEEDS_REVIEW/{item}"
            reason = "Low confidence / Unknown"

        migration_steps.append({"source": source, "target": target, "reason": reason, "project": pid})

    # Generate Markdown Plan
    with open(PLAN_FILE, "w") as f:
        f.write("# Migration Plan\n\n")
        f.write("| Source (Root Relative) | Target | Reason | Project |\n")
        f.write("|---|---|---|---|\n")

        for step in migration_steps:
            f.write(f"| `{step['source']}` | `{step['target']}` | {step['reason']} | {step['project']} |\n")

    print(f"Plan generated at {PLAN_FILE}")


if __name__ == "__main__":
    main()
