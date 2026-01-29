
import csv
import datetime
import os
import shutil

ROOT_DIR = "/home/gonya"
NAV_DIR = os.path.join(ROOT_DIR, "00_NAV")
PLAN_FILE = os.path.join(NAV_DIR, "MIGRATION_PLAN.md")
LOG_FILE = os.path.join(NAV_DIR, "MIGRATION_LOG.csv")

def parse_plan():
    steps = []
    with open(PLAN_FILE) as f:
        lines = f.readlines()

    start_reading = False
    for line in lines:
        if line.startswith("|---|"):
            start_reading = True
            continue
        if start_reading and line.startswith("|"):
            parts = [p.strip().strip('`').strip() for p in line.split("|")]
            # parts[0] is empty (split left of first |)
            # parts[1] Source
            # parts[2] Target
            # parts[3] Reason
            # parts[4] Project
            if len(parts) >= 5:
                source = parts[1]
                target = parts[2]
                reason = parts[3]
                steps.append((source, target, reason))
    return steps

def safe_move(source_path, target_path):
    if not os.path.exists(source_path):
        return "Source Missing", target_path

    if os.path.abspath(source_path) == os.path.abspath(target_path):
        return "Skipped (Same Path)", target_path

    target_dir = os.path.dirname(target_path)
    if not os.path.exists(target_dir):
        os.makedirs(target_dir, exist_ok=True)

    final_target = target_path
    if os.path.exists(final_target):
        # Collision
        base, ext = os.path.splitext(final_target)
        counter = 2
        while os.path.exists(final_target):
            final_target = f"{base}_v{counter}{ext}"
            counter += 1

    try:
        shutil.move(source_path, final_target)
        return "Moved", final_target
    except Exception as e:
        return f"Error: {e}", final_target

def main():
    steps = parse_plan()

    with open(LOG_FILE, 'w', newline='') as csvfile:
        fieldnames = ['timestamp', 'source', 'target_original', 'target_final', 'status', 'reason']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for source_rel, target_rel, reason in steps:
            source_abs = os.path.join(ROOT_DIR, source_rel)
            target_abs = os.path.join(ROOT_DIR, target_rel)

            # Additional safety check regarding system files
            if source_rel.startswith(".") and "Projects" not in target_rel:
                 # Paranoid check: if we are trying to move a dotfile to inbox, skip if it's in our Ignore list?
                 # But we filtered plan. Trust plan.
                 pass

            status, final_target_abs = safe_move(source_abs, target_abs)

            final_target_rel = os.path.relpath(final_target_abs, ROOT_DIR)

            writer.writerow({
                'timestamp': datetime.datetime.now().isoformat(),
                'source': source_rel,
                'target_original': target_rel,
                'target_final': final_target_rel,
                'status': status,
                'reason': reason
            })
            print(f"{status}: {source_rel} -> {final_target_rel}")

    # Create READMEs for projects
    # Scan for project folders
    projects_root = os.path.join(ROOT_DIR, "01_Projects")
    if os.path.exists(projects_root):
        for prj_dir in os.listdir(projects_root):
            p_path = os.path.join(projects_root, prj_dir)
            if os.path.isdir(p_path) and prj_dir.startswith("PRJ-"):
                readme_path = os.path.join(p_path, "00_README.md")
                if not os.path.exists(readme_path):
                    with open(readme_path, 'w') as f:
                        f.write(f"# {prj_dir}\n\nAuto-generated structure.\n\n## Overview\nStatus: Active\n\n## Contents\n- 01_Docs: Documentation\n- 02_Dev: Code and Configs\n")

if __name__ == "__main__":
    main()
