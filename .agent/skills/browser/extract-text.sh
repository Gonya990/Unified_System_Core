#!/bin/bash
# Extract text from multiple elements
# Usage: ./extract-text.sh "selector1" "selector2" ...

NDC="/Users/macbook/Documents/Unified_System/Agent_Context/Knowledge_Base/Sessions/nodriver_implementation/ndc"

if [ $# -eq 0 ]; then
    echo '{"ok":false,"error":"Usage: extract-text.sh \"selector1\" \"selector2\" ..."}'
    exit 1
fi

echo "["
FIRST=true
for SELECTOR in "$@"; do
    if [ "$FIRST" = true ]; then
        FIRST=false
    else
        echo ","
    fi
    $NDC text "$SELECTOR"
done
echo "]"
