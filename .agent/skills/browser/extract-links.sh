#!/bin/bash
# Extract links and titles from current page
# Usage: ./extract-links.sh ".g a"

NDC="/Users/macbook/Documents/Unified_System/Agent_Context/Knowledge_Base/Sessions/nodriver_implementation/ndc"
SELECTOR="${1:-a}"

$NDC extract "{\"titles\": \"$SELECTOR\", \"hrefs\": \"$SELECTOR\"}" | python3 -c "
import sys, json
data = json.load(sys.stdin)
if data.get('ok'):
    items = data['data']
    for i in range(len(items.get('titles', []))):
        print(f\"{items['titles'][i]}\")
"
