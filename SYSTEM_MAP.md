# 🗺 SYSTEM MAP | КАРТА СИСТЕМЫ

This document defines the logical structure and connections of the
Unified System workspace. **Always refer to this map for navigation.**

## 📂 Root Directory Structure

| Directory | Purpose | Key Contents |
| :--- | :--- | :--- |
| `Projects/` | Main application codebases | `AI_Core`, `connect-landing-page` |
| `Scripts/` | Automation & specialized logic | `Orchestration`, `External` |
| `Career/` | Personal professional assets | Resumes, Vacancy scans |
| `Reports/` | System status & audit history | `Archived_Status`, Audit logs |
| `Management/` | Planning & tasks | `MASTER_TASKS.md`, `CHANGELOG.md` |
| `Infra/` | System setup & config | HA states, Setup guides |
| `Data/` | Local data | `Local/` (SQLite DBs) |
| `Docs/` | Documentation & Guides | Tool guides, Scenario plans, Manuals |
| `Local_Dev/` | Transient dev files | `Cache`, `Venv`, `Media` (inputs) |
| `Archive/` | Legacy & obsolete files | Versioned backups, old orchestrators |

## 🔗 Logical Connections

- **AI Bot**: Located in `Projects/AI_Core`.
- **Sync Logic**: `Scripts/Orchestration/full_sync.sh` links.
- **Production Pipeline**: `Scripts/Production_Factory/` handles generation.
- **Memory & Context**: Stored in `Agent_Context/` and `Agent_Workflows/`.
- **Architecture (VASER-Hub)**: `docs/architecture/vaser-hub.md`.

## 🛠 Maintenance Rules

1. **No Clutter**: Root should only contain essential config files and this map.
2. **Standardized Moves**: New reports go to `Reports/`. New tools go to `Scripts/`.
3. **Documentation First**: Update this map if a new top-level category is created.

---

### Management Notes
