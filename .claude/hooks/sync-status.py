import sys
import subprocess
import os

def update_mail(issue_id, status, notes=""):
    project_key = "/home/kosta/Documents/Unified_System_Core"
    agent_name = "VioletCastle" # From .env
    
    # Get issue title
    try:
        title = subprocess.check_output(["bd", "show", issue_id, "--format", "{{title}}"], text=True).strip()
    except:
        title = "Unknown Task"
    
    desc = f"Beads: {issue_id} [{status}] - {title}. {notes}"
    
    # We can't easily call MCP from python, but we can emit a signal for the agent 
    # or use a pre-commit guard style approach.
    # For ULW mode, we will print the exact MCP call for the agent to execute.
    print(f"ACTION_REQUIRED: Execute register_agent with task_description='{desc}'")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: sync-status.py <issue_id> <status> [notes]")
        sys.exit(1)
    update_mail(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "")
