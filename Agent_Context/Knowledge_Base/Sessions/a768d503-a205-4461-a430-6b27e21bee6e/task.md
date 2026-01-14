# Unified System Tasks

> [!CAUTION]
> **STRICT SECURITY PROTOCOL ACTIVE**
>
> - No external code/repo downloads without deep analysis + User Approval.
> - No structural system changes ("Evolution Leaps") without **Biometric Approval** (iPhone/Mac).
> - `global1sim` repo is RESTRICTED (Kostik's private secondary account). DO NOT TOUCH without explicit authorization.

## Current High Priority

- [x] **Knowledge Base Migration & De-duplication** <!-- id: 11 -->
  - [x] **Transfer**: `OneDrive_1` (Done), `OneDrive_3` (Done), `File 3` (Done).
  - [x] **Analysis**: ~2900 files extracted to `contexts/temp_extract`.
  - [x] **De-duplication**: Deleted 1 duplicate from Google Drive (`503725.pdf`).
- [ ] **Family Assistant (Webtop Integration)** <!-- id: 9 -->
  - [x] **Pivot**: Confirmed School uses Webtop/SmartSchool. Found existing Token.
  - [/] **API Fix**: Logic for `webtop_client.py` is hitting HTML. Need to RE the JSON API.
  - [ ] **Data Fetch**: Get Grades/Homework via correct API (POST payload?).
  - [ ] **Integration**: Connect to `morning_brief.py`.
- [ ] **MCP Mail Intelligence** <!-- id: 10 -->
  - [ ] **Server Setup**: Locate/Create MCP Mail Server.
  - [ ] **Intelligence**: Add AI summarization/sorting to mail.

## Infrastructure & Security

- [x] **Security Scan for new modules** <!-- id: 8 -->
  - [x] Audited `Scripts/windows_optimizer` & `archive_analyzer`.
  - [x] Grep Check: No hardcoded secrets found.
  - [x] Permissions: `wait_for_windows.sh` (+x), others (rw-).
- [ ] `global1sim` Submodule Integration (⛔️ **LOCKED**: Requires Biometric Auth/Access Keys)

## Completed Tasks

- [x] **Google Developer Benefits Research**
- [x] **Windows System Optimization**
- [x] **Content Factory Status Monitoring**
- [x] **Google Cloud Verification**
- [x] **Windows Archive Analyzer**
