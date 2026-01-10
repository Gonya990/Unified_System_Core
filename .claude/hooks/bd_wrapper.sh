#!/bin/bash
# Wrapper for beads CLI to provide automatic status syncing

# Execute the actual bd command
/usr/local/bin/bd "$@"
RESULT=$?

# If command was 'update' or 'close' and succeeded, trigger the hook
if [ $RESULT -eq 0 ]; then
    case "$1" in
        update|close)
            # Extract ID and search for status/notes in args
            # Simple version: just notify that a change happened
            # A more complex version would parse the specific changes
            /home/kosta/Documents/Unified_System_Core/.claude/hooks/beads_status_hook.sh "$2" "updated/closed" "Check beads for details"
            ;;
    esac
fi

exit $RESULT
