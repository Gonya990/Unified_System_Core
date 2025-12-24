#!/bin/bash
# Google Search skill
# Usage: ./google-search.sh "search query"

NDC="/Users/macbook/Documents/Unified_System/Agent_Context/Knowledge_Base/Sessions/nodriver_implementation/ndc"
QUERY="$1"

if [ -z "$QUERY" ]; then
    echo '{"ok":false,"error":"Usage: google-search.sh \"query\""}'
    exit 1
fi

# Navigate to Google
$NDC goto "https://google.com" >/dev/null

# Fill search box
$NDC fill "textarea[name=q]" "$QUERY"

# Submit form
$NDC js "document.querySelector('form').submit()" >/dev/null

# Wait for results
sleep 2
$NDC wait "div#search" 10 >/dev/null

# Return result count and title
$NDC js "({results: document.querySelectorAll('div#search .g').length, title: document.title, url: location.href})"
