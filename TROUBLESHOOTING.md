# Troubleshooting Guide

[russian] This guide helps diagnose and fix common issues in the Unified System Core.

## Quick Health Check

Run the system health check to diagnose issues:

```bash
python3 Scripts/Utilities/system_health_check.py
```

## Common Issues

### 1. Missing Dependencies

**Problem**: `✗ Missing dependency: telegram` or other import errors

**Solution**:
```bash
cd Projects/AI_Core
pip install -r requirements.txt
```

### 2. Environment Variables Not Set

**Problem**: Bot not starting, missing API keys

**Solution**:
1. Copy the example environment file:
   ```bash
   cp .env.example .env.local
   ```
2. Edit `.env.local` and add your API keys:
   - `TELEGRAM_BOT_TOKEN`
   - `OPENAI_API_KEY`
   - `GEMINI_API_KEY`
   - etc.

### 3. Permission Issues

**Problem**: Scripts are not executable

**Solution**:
```bash
chmod +x check_system.sh
chmod +x start_brain.sh
chmod +x Scripts/**/*.sh
```

### 4. Git Status Issues

**Problem**: Uncommitted changes or conflicts

**Solution**:
```bash
# Check what changed
git status

# View differences
git diff

# Commit changes
git add .
git commit -m "Your commit message"

# Or discard changes (careful!)
git restore <file>
```

### 5. Python Version Issues

**Problem**: `✗ Python 3.x.x (need 3.9+)`

**Solution**:
- Install Python 3.9 or higher
- Use `python3.9` or higher explicitly
- Consider using `pyenv` to manage Python versions

### 6. AI Core Bot Issues

**Problem**: Bot not responding or crashing

**Check**:
1. Is the bot running?
   ```bash
   ps aux | grep python | grep bot
   ```

2. Check logs:
   ```bash
   tail -f logs/*.log
   ```

3. Test bot configuration:
   ```bash
   cd Projects/AI_Core
   python3 generate_token.py  # Check token validity
   ```

### 7. Project Directory Missing

**Problem**: `✗ Missing: Projects/AI_Core` or similar

**Solution**:
- This indicates repository corruption or incomplete clone
- Re-clone the repository:
  ```bash
  git clone https://github.com/Unified-system-Core/Unified_System_Core.git
  ```

## System Architecture

See [SYSTEM_MAP.md](SYSTEM_MAP.md) for the full system architecture.

Key components:
- **AI Bot**: `Projects/AI_Core/` - Main Telegram bot
- **Scripts**: `Scripts/` - Automation and utilities
- **Agent Context**: `Agent_Context/` - AI agent knowledge base

## Getting Help

1. Run the health check first: `python3 Scripts/Utilities/system_health_check.py`
2. Check this troubleshooting guide
3. Review the relevant project README:
   - [Main README](README.md)
   - [AI Core README](Projects/AI_Core/README.md)
4. Check [CLAUDE.md](CLAUDE.md) for agent guidelines

## Translation Protocol

All system output follows the **English Translation Protocol**:
- Responses are in English
- Tag `[russian]` indicates original Russian context
- Technical terms are preserved for clarity

---

*Last Updated: 2026-01-25*
