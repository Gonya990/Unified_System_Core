#!/bin/bash
# Fill form fields
# Usage: ./fill-form.sh "selector1=value1" "selector2=value2" ...

NDC="/Users/macbook/Documents/Unified_System/Agent_Context/Knowledge_Base/Sessions/nodriver_implementation/ndc"

if [ $# -eq 0 ]; then
    echo '{"ok":false,"error":"Usage: fill-form.sh \"selector1=value1\" \"selector2=value2\" ..."}'
    exit 1
fi

FILLED=0
for PAIR in "$@"; do
    SELECTOR="${PAIR%%=*}"
    VALUE="${PAIR#*=}"
    
    RESULT=$($NDC fill "$SELECTOR" "$VALUE")
    if echo "$RESULT" | grep -q '"ok": true'; then
        ((FILLED++))
    else
        echo "$RESULT"
        exit 1
    fi
done

echo "{\"ok\": true, \"filled\": $FILLED}"
