#!/bin/bash
# Universal login skill
# Usage: ./login.sh "URL" "email_selector=email" "pass_selector=password" "submit_selector"

NDC="/Users/macbook/Documents/Unified_System/Agent_Context/Knowledge_Base/Sessions/nodriver_implementation/ndc"

URL="$1"
EMAIL_PAIR="$2"
PASS_PAIR="$3"
SUBMIT="$4"

if [ -z "$URL" ] || [ -z "$EMAIL_PAIR" ] || [ -z "$PASS_PAIR" ] || [ -z "$SUBMIT" ]; then
    echo '{"ok":false,"error":"Usage: login.sh URL \"email_sel=email\" \"pass_sel=pass\" \"submit_sel\""}'
    exit 1
fi

EMAIL_SEL="${EMAIL_PAIR%%=*}"
EMAIL_VAL="${EMAIL_PAIR#*=}"
PASS_SEL="${PASS_PAIR%%=*}"
PASS_VAL="${PASS_PAIR#*=}"

# Navigate
$NDC goto "$URL" >/dev/null
sleep 1

# Fill credentials
$NDC fill "$EMAIL_SEL" "$EMAIL_VAL" >/dev/null
$NDC fill "$PASS_SEL" "$PASS_VAL" >/dev/null

# Submit
$NDC clicksel "$SUBMIT"
sleep 2

# Return current state
$NDC js "({url: location.href, title: document.title})"
