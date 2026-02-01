---
description: Full system initialization and sync on startup
---
# 🚀 System Bootstrap (Init)

This workflow updates the local repository and verifies connectivity to all nodes.

// turbo-all

1. Pull latest changes from GitHub:
   `git -C /Users/igorgoncharenko/Documents/Unified_System_Core pull --rebase \
   origin main`

2. Check Tailscale network status:
   `tailscale status | grep -E "active|idle"`

3. Verify reachability of primary nodes:
   `ping -c 1 100.115.17.68 && ping -c 1 100.87.208.56 && ping -c 1 100.67.107.71`

4. Run system status check:
   `git -C /Users/igorgoncharenko/Documents/Unified_System_Core status --short`

5. Check GPU Council progress:
   `ssh igor-gaming-1 "/home/gonya/Unified_System_Core/Projects/AI_Core/\
venv/bin/python3 -c \"\
import sqlite3; \
conn = sqlite3.connect('/home/gonya/Unified_System_Core/Projects/AI_Core/\
knowledge_base.db'); \
c = conn.cursor(); \
c.execute('SELECT COUNT(*) FROM assets'); \
total = c.fetchone()[0]; \
c.execute('SELECT COUNT(*) FROM assets WHERE concept_summary \
IS NOT NULL'); \
summarized = c.fetchone()[0]; \
print(f'GPU Progress: {round(summarized/total*100, 2)}% \
({summarized}/{total})')\""`
