
import os
import glob
from pathlib import Path

BRAIN_DIR = "/Users/macbook/.gemini/antigravity/brain"
OUTPUT_FILE = "/Users/macbook/Documents/Unified_System/TODO_CONSOLIDATED.md"

def collect_tasks():
    all_tasks = {}
    
    # Iterate through all subdirectories in brain dir
    for root, dirs, files in os.walk(BRAIN_DIR):
        for file in files:
            if file == "task.md":
                file_path = os.path.join(root, file)
                conversation_id = os.path.basename(root)
                
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        lines = f.readlines()
                        
                    pending_tasks = []
                    current_context = "General"
                    
                    for line in lines:
                        line = line.strip()
                        # Simple markdown task detection
                        if line.startswith("- [ ]") or line.startswith("* [ ]"):
                            task_text = line[5:].strip()
                            pending_tasks.append(task_text)
                            
                    if pending_tasks:
                        all_tasks[conversation_id] = pending_tasks
                        
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")

    # Write consolidated file
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        out.write("# Consolidated Pending Tasks\n\n")
        out.write(f"Generated from {len(all_tasks)} conversation contexts.\n\n")
        
        for cid, tasks in all_tasks.items():
            out.write(f"## Context: {cid}\n")
            for task in tasks:
                out.write(f"- [ ] {task}\n")
            out.write("\n")
            
    print(f"Successfully collected tasks from {len(all_tasks)} files into {OUTPUT_FILE}")

if __name__ == "__main__":
    collect_tasks()
