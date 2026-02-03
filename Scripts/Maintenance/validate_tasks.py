#!/usr/bin/env python3
import os
import re
import sys
from pathlib import Path

# Colors for output
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
BILLBOARD_DIR = ROOT_DIR / "billboard/tasks"

def validate_tasks():
    print(f"{GREEN}📋 Validating Billboard Tasks...{RESET}")
    
    if not BILLBOARD_DIR.exists():
        print(f"{RED}❌ Billboard directory not found: {BILLBOARD_DIR}{RESET}")
        return False

    tasks = list(BILLBOARD_DIR.glob("*.md"))
    if not tasks:
        print(f"{YELLOW}⚠️ No tasks found in {BILLBOARD_DIR}{RESET}")
        return True

    errors = 0
    for task_file in tasks:
        if task_file.name == "TEMPLATE.md":
            continue
            
        with open(task_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Check for Frontmatter
        if not content.startswith("---"):
            print(f"{RED}❌ Task {task_file.name} missing frontmatter!{RESET}")
            errors += 1
            continue

        # Extract values
        task_id = re.search(r"Task-Id:\s*(GH-\d+)", content)
        status = re.search(r"Status:\s*(\w+)", content)
        
        if not task_id:
            print(f"{RED}❌ Task {task_file.name} missing Task-Id!{RESET}")
            errors += 1
        else:
            print(f"✅ Found {task_id.group(1)}: {task_file.name}")

    if errors > 0:
        print(f"\n{RED}❌ Validation failed with {errors} errors.{RESET}")
        return False
    
    print(f"\n{GREEN}✨ All tasks are valid!{RESET}")
    return True

if __name__ == "__main__":
    success = validate_tasks()
    sys.exit(0 if success else 1)
