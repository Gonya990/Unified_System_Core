#!/bin/bash
# Click element and wait for result
# Usage: ./click-and-wait.sh "button text or selector" [wait_selector] [use_selector]

NDC="/Users/macbook/Documents/Unified_System/Agent_Context/Knowledge_Base/Sessions/nodriver_implementation/ndc"
TARGET="$1"
WAIT_FOR="${2:-body}"
USE_SELECTOR="${3:-}"

if [ -z "$TARGET" ]; then
    echo '{"ok":false,"error":"Usage: click-and-wait.sh \"target\" [wait_selector] [use_selector]"}'
    exit 1
fi

# Click by text or selector
if [ -n "$USE_SELECTOR" ]; then
    $NDC clicksel "$TARGET"
else
    $NDC click "$TARGET"
fi

sleep 0.5
$NDC wait "$WAIT_FOR" 10
