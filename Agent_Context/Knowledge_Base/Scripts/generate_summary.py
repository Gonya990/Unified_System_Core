import csv
import os

ROOT_DIR = "/home/gonya"
NAV_DIR = os.path.join(ROOT_DIR, "00_NAV")
LOG_FILE = os.path.join(NAV_DIR, "MIGRATION_LOG.csv")
NAV_FILE = os.path.join(NAV_DIR, "NAVIGATION.md")
SUMMARY_FILE = os.path.join(NAV_DIR, "POST_MIGRATION_SUMMARY.md")
PROJECTS_ROOT = os.path.join(ROOT_DIR, "01_Projects")


def main():
    # Read Log
    succeeded = 0
    failed = 0
    by_project = {}
    inbox_count = 0
    inbox_items = []

    with open(LOG_FILE) as f:
        reader = csv.DictReader(f)
        for row in reader:
            if "Moved" in row["status"]:
                succeeded += 1
                target = row["target_final"]
                if "01_Projects" in target:
                    # Extract PRJ id
                    parts = target.split("/")
                    if len(parts) > 1:
                        prj = parts[1]
                        by_project[prj] = by_project.get(prj, 0) + 1
                elif "NEEDS_REVIEW" in target:
                    inbox_count += 1
                    if len(inbox_items) < 20:
                        inbox_items.append(row["source"])
            else:
                failed += 1

    # Generate Navigation
    with open(NAV_FILE, "w") as f:
        f.write("# Project Navigation\n\n")
        f.write("## 🚀 Projects\n")
        f.write("| Project | Status | Path | Key Files |\n")
        f.write("|---|---|---|---|\n")

        if os.path.exists(PROJECTS_ROOT):
            projects = sorted(os.listdir(PROJECTS_ROOT))
            for p in projects:
                f.write(f"| **{p}** | Active | `01_Projects/{p}` | [README](01_Projects/{p}/00_README.md) |\n")

        f.write("\n## 📬 Inbox / Needs Review\n")
        f.write(f"**{inbox_count}** items require attention in `90_Inbox_ToSort/NEEDS_REVIEW`.\n")
        f.write("\n## 📚 Shared & Operations\n")
        f.write("- **Shared**: `02_Shared/` (Installers, Global Scripts)\n")
        f.write("- **Operations**: `03_Operations/`\n")

        f.write("\n## Quick Jump\n")
        f.write("- [Migration Log](MIGRATION_LOG.csv)\n")
        f.write("- [Full Inventory](INVENTORY.csv)\n")
        f.write("- [Rules](RULES.md)\n")

    # Generate Summary
    with open(SUMMARY_FILE, "w") as f:
        f.write("# Post-Migration Summary\n\n")
        f.write(f"**Total Moves**: {succeeded + failed}\n")
        f.write(f"**Successful**: {succeeded}\n")
        f.write(f"**Failed/Skipped**: {failed}\n")
        f.write(f"**Items in Inbox**: {inbox_count}\n\n")

        f.write("## Project Breakdown\n")
        for prj, count in by_project.items():
            f.write(f"- {prj}: {count} items\n")

        f.write("\n## Top 20 Inbox Items\n")
        for item in inbox_items:
            f.write(f"- {item}\n")


if __name__ == "__main__":
    main()
