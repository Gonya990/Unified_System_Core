---
description: Check progress of the GPU Council Asset Indexing
---

1. Check indexer log:
\`\`\`bash
ssh igor-gaming-1 "tail -n 20 /home/gonya/Unified_System_Core/Projects/Content_Factory/scripts/indexer.log"
\`\`\`

2. Check database statistics:
\`\`\`bash
ssh igor-gaming-1 "/home/gonya/Unified_System_Core/Projects/AI_Core/venv/bin/python3 -c \"import sqlite3; conn = sqlite3.connect('/home/gonya/Unified_System_Core/Projects/AI_Core/knowledge_base.db'); c = conn.cursor(); c.execute('SELECT COUNT(*) FROM assets'); total = c.fetchone()[0]; c.execute('SELECT COUNT(*) FROM assets WHERE concept_summary IS NOT NULL'); summarized = c.fetchone()[0]; print(f'Total: {total}, Summarized: {summarized}, Progress: {round(summarized/total*100, 2)}%')\""
\`\`\`
