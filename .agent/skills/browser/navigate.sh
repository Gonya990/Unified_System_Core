#!/bin/bash
# Navigate and wait for page load
# Usage: ./navigate.sh "https://example.com" [wait_selector]

NDC="/Users/macbook/Documents/Unified_System/Agent_Context/Knowledge_Base/Sessions/nodriver_implementation/ndc"
URL="$1"
WAIT_FOR="${2:-body}"

if [ -z "$URL" ]; then
    echo '{"ok":false,"error":"Usage: navigate.sh \"URL\" [wait_selector]"}'
    exit 1
fi

$NDC goto "$URL"
sleep 1
$NDC wait "$WAIT_FOR" 10
$NDC js "({title: document.title, url: location.href})"
