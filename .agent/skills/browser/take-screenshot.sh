#!/bin/bash
# Take Screenshot skill
# Usage: ./take-screenshot.sh [filename]

NDC="/Users/macbook/Documents/Unified_System/Agent_Context/Knowledge_Base/Sessions/nodriver_implementation/ndc"
FILENAME="${1:-/tmp/screenshot_$(date +%Y%m%d_%H%M%S).png}"

$NDC screenshot "$FILENAME"
