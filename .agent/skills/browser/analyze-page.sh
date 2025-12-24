#!/bin/bash
# Analyze current page for general browsing
# Returns a semantic summary of interactable elements

NDC="/Users/macbook/Documents/Unified_System/Agent_Context/Knowledge_Base/Sessions/nodriver_implementation/ndc"

# Get current status
STATUS=$($NDC status)
URL=$(echo "$STATUS" | python3 -c "import sys, json; print(json.load(sys.stdin).get('current_url', ''))")

echo "--- PAGE ANALYSIS ---"
echo "URL: $URL"
echo ""
echo "INTERACTABLE ELEMENTS:"

# Get elements and process directly to avoid shell buffer issues
$NDC elements | python3 - <<EOF
import sys, json
try:
    content = sys.stdin.read()
    if not content:
        print("Error: No output from ndc elements")
        sys.exit(0)
        
    data = json.loads(content)
    if data.get('ok'):
        elements = data.get('elements', [])
        if not elements:
            print("[no interactable elements found]")
        else:
            for el in elements:
                tag = el.get('tag', 'unknown')
                text = el.get('text', '[no text]')
                selector = el.get('selector', 'none')
                print(f"- [{tag}] {text} (Selector: {selector})")
    else:
        print('Failed to get elements: ' + data.get('error', 'unknown error'))
except Exception as e:
    print(f"Error parsing JSON: {e}")
EOF
echo "----------------------"
