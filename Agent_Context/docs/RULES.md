# Organization Rules

## Structure Overview
- **00_NAV/**: Navigation data, registries, logs.
- **01_Projects/**: Active and archived project folders.
- **02_Shared/**: Resources used across multiple projects (Scripts, Installers).
- **03_Operations/**: Operational documents (Credentials? - Handle with care).
- **90_Inbox_ToSort/**: Things that need manual review.
- **99_Archive_Original/**: Only for original structure snapshots (empty by default).

## Project Assignment Logic
1. **Home Assistant (PRJ-001)**:
   - Filenames starting with `ha_`, `hass`, `dashboard_`.
   - `.homeassistant` and `hass` directories.
   - Files containing "Home Assistant" or related entity reports.
   - `wyoming` folder.

2. **IoT & Tuya (PRJ-002)**:
   - Filenames with `tuya`, `tinytuya`, `scan_`, `broadlink`.
   - `matter-data` directory (Moved to `01_Docs/Credentials` inside project, or similar).
   - Python scripts for scanning networks/devices.

3. **N8N & Automation (PRJ-003)**:
   - `n8n` directory and `n8n_*.json` workflows.
   - `nodered` related files and logs.
   - `node_red` directory.

4. **AI Agents (PRJ-004)**:
   - `llm-council` folder.
   - `ollama` related files and logs.
   - AI agent scripts (`browser_agent.py`, etc.).

5. **Media (PRJ-005)**:
   - `tv_*` yaml/scripts.
   - `dlna_` and `cast_` documents.

6. **OpenCode (PRJ-006)**:
   - `opencode-server` folder.

## Special Handling
- **System Files**: `.bashrc`, `.profile`, `.status`, `.ssh`, `.config` -> **DO NOT MOVE**. Leave in Root.
- **Installers**: `miniconda.sh`, `install.sh` -> Move to `02_Shared/Installers` or keep in Project if specific.
- **Unknowns**: If confidence < 0.7, move to `90_Inbox_ToSort/NEEDS_REVIEW` with a note.
- **Naming Conflicts**: Append `_v2`, `_v3` etc.

## Folder template for Projects
- `00_README.md`
- `01_Docs` (Markdown reports, docs)
- `02_Dev` (Code, scripts, configs, JSONs)
- `03_Design` (Images, layouts)
- `04_Research` (Notes, ideas)
- `05_Meetings` (Logs)
- `99_Archive` (Old files)
