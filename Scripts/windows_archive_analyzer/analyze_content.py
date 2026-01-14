import json
import os
import subprocess
import glob
from pathlib import Path
from datetime import datetime


def find_latest_report():
    report_dir = Path("reports")
    if not report_dir.exists():
        return None
    files = list(report_dir.glob("scan_*.json"))
    if not files:
        return None
    return max(files, key=os.path.getctime)


def get_7zip_path():
    # Common paths for 7-Zip on Windows
    paths = [
        r"C:\Program Files\7-Zip\7z.exe",
        r"C:\Program Files (x86)\7-Zip\7z.exe",
        "7z",  # In PATH
    ]
    for p in paths:
        if p == "7z":
            # Check PATH
            try:
                subprocess.run(["7z"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return "7z"
            except FileNotFoundError:
                continue
        elif os.path.exists(p):
            return p
    return None


def analyze_archive(archive_path, seven_zip_path):
    if not seven_zip_path:
        return "7-Zip not found. Cannot inspect contents."

    try:
        # List contents (limited to top 20 lines to avoid spam)
        cmd = [seven_zip_path, "l", archive_path]
        result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")

        if result.returncode != 0:
            return f"Error reading archive: {result.stderr}"

        lines = result.stdout.splitlines()
        # Parse for file list (skip header/footer heuristic)
        files = []
        listing = False
        for line in lines:
            if "   Date      Time" in line:
                listing = True
                continue
            if "-------------------" in line:
                listing = not listing  # Toggle
                continue
            if listing and line.strip():
                # Extract filename (last column usually)
                parts = line.split()
                if len(parts) > 5:
                    files.append(" ".join(parts[5:]))

        return files[:30]  # Return first 30 files
    except Exception as e:
        return f"Exception during analysis: {e}"


def generate_copilot_prompt(archive_name, file_list):
    prompt = f"I have an archive named '{archive_name}' containing the following files:\n"
    for f in file_list:
        prompt += f"- {f}\n"
    prompt += "\nBased on these files, what is the likely content of this archive? Can it be safely deleted if I don't play this game or use this software anymore?"
    return prompt


def main():
    print("Windows Archive AI Analyzer")
    print("===============================")

    report_path = find_latest_report()
    if not report_path:
        print("X No scan reports found in 'reports/' folder.")
        return

    print(f"Loading report: {report_path}")
    with open(report_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    archives = data.get("Archives", [])
    if not archives:
        print("? No archives found in report.")
        return

    # Sort by size (descending)
    archives.sort(key=lambda x: x.get("SizeGB", 0), reverse=True)

    seven_zip = get_7zip_path()
    if seven_zip:
        print(f"Found 7-Zip at: {seven_zip}")
    else:
        print("! 7-Zip not found. analysis will be limited to metadata.")

    top_n = 5
    print(f"\nAnalyzing Top {top_n} Largest Archives:\n")

    analysis_output = f"# Archive Analysis Report - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"

    for i, arc in enumerate(archives[:top_n]):
        name = arc.get("Name", "Unknown")
        path = arc.get("Path", "Unknown")
        size = arc.get("SizeGB", 0)

        print(f"{i + 1}. {name} ({size} GB)")
        print(f"   path: {path}")

        analysis_output += f"## {i + 1}. {name} ({size} GB)\n"
        analysis_output += f"**Path**: `{path}`\n\n"

        if seven_zip and os.path.exists(path):
            files = analyze_archive(path, seven_zip)
            if isinstance(files, list):
                print(f"   Contains {len(files)}+ files. Examples: {', '.join(files[:3])}...")

                # Heuristic
                is_game = any(f.endswith(".exe") or "data" in f.lower() for f in files)

                analysis_output += "### 📦 Content Preview\n"
                analysis_output += "```text\n" + "\n".join(files) + "\n```\n\n"

                prompt = generate_copilot_prompt(name, files)
                analysis_output += "### 🤖 Copilot Prompt\n"
                analysis_output += "> Copy this into Copilot to decide:\n\n"
                analysis_output += f"```text\n{prompt}\n```\n\n"

            else:
                print(f"   X {files}")
                analysis_output += f"**Error**: {files}\n\n"
        else:
            analysis_output += "**Status**: File not found or 7-Zip missing.\n\n"

        analysis_output += "---\n\n"

    out_file = "analysis_report.md"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(analysis_output)

    print(f"\nAnalysis complete! Report saved to: {out_file}")
    print(f"Open {out_file} to see Copilot prompts.")


if __name__ == "__main__":
    main()
