#!/usr/bin/env python3
import os
import re
import sys
from pathlib import Path

# Colors for output
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
BILLBOARD_DIR = ROOT_DIR / "billboard/tasks"

# Expanded valid statuses
VALID_STATUSES = {
    "Claimed", "In-Progress", "Completed", "Paused", "Open", "Done", 
    "InPrg", "Blocked", "Proposed", "Merged", "Rejected"
}
MANDATORY_FIELDS = ["Task-Id", "Status", "Context", "Task-Semantic"]

def validate_tasks():
    print(f"{BLUE}📋 Enhanced Billboard Task Validation...{RESET}")
    
    if not BILLBOARD_DIR.exists():
        print(f"{RED}❌ Billboard directory not found: {BILLBOARD_DIR}{RESET}")
        return False

    tasks = list(BILLBOARD_DIR.glob("*.md"))
    if not tasks:
        print(f"{YELLOW}⚠️ No tasks found in {BILLBOARD_DIR}{RESET}")
        return True

    errors = 0
    total_tasks = 0
    
    for task_file in tasks:
        if task_file.name == "TEMPLATE.md":
            continue
            
        total_tasks += 1
        file_errors = 0
        task_name = task_file.name
        
        with open(task_file, "r", encoding="utf-8") as f:
            content = f.read()

        # 1. Check for Frontmatter
        frontmatter_match = re.search(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
        if not frontmatter_match:
            print(f"{RED}❌ {task_name}: Missing or malformed frontmatter (--- block){RESET}")
            errors += 1
            continue
            
        frontmatter = frontmatter_match.group(1)
        
        # 2. Field Validation
        fields = {}
        for line in frontmatter.split("\n"):
            if ":" in line:
                key, val = line.split(":", 1)
                fields[key.strip()] = val.strip()

        # Mandatory fields check
        for field in MANDATORY_FIELDS:
            if field not in fields:
                print(f"{RED}❌ {task_name}: Missing mandatory field '{field}'{RESET}")
                file_errors += 1
            elif not fields[field]:
                print(f"{RED}❌ {task_name}: Field '{field}' is empty{RESET}")
                file_errors += 1

        # 3. Task-Id Consistency
        tid = fields.get("Task-Id")
        if tid:
            if not task_name.startswith(tid):
                print(f"{RED}❌ {task_name}: Task-Id '{tid}' does not match filename prefix{RESET}")
                file_errors += 1
            if not re.match(r"^GH-\d{3}$", tid):
                # Just a warning for non-standard IDs
                print(f"{YELLOW}⚠️ {task_name}: Task-Id '{tid}' doesn't match standard GH-XXX format{RESET}")

        # 4. Status Validation
        status = fields.get("Status")
        if status and status not in VALID_STATUSES:
            print(f"{RED}❌ {task_name}: Invalid status '{status}'.{RESET}")
            file_errors += 1

        # 5. Semantic Structure Check (Flexible with Emojis)
        if not re.search(r"^# .*", content, re.MULTILINE):
            print(f"{RED}❌ {task_name}: Missing main H1 header{RESET}")
            file_errors += 1
        
        if not re.search(r"^##.*Objective", content, re.IGNORECASE | re.MULTILINE):
            print(f"{RED}❌ {task_name}: Missing Objective section (## Objective){RESET}")
            file_errors += 1
            
        if not re.search(r"^##.*Acceptance Criteria", content, re.IGNORECASE | re.MULTILINE):
            print(f"{RED}❌ {task_name}: Missing Acceptance Criteria section (## Acceptance Criteria){RESET}")
            file_errors += 1

        if file_errors == 0:
            print(f"{GREEN}✅ {tid or 'UNKNOWN'}: {task_name} PASSED{RESET}")
        else:
            errors += file_errors

    print(f"\n{BLUE}--- Validation Summary ---{RESET}")
    print(f"Total tasks checked: {total_tasks}")
    
    if errors > 0:
        print(f"{RED}❌ Validation failed with {errors} total errors.{RESET}")
        return False
    
    print(f"{GREEN}✨ All tasks are valid and consistency checks passed!{RESET}")
    return True

if __name__ == "__main__":
    success = validate_tasks()
    sys.exit(0 if success else 1)
