#!/usr/bin/env python3
"""
Unified System Master Controller
================================
This script acts as the single entry point ("Command Center") for all Unified System modules.
It combines access to Content Factory, System Sync, Mail Intelligence, and Family Assistants.

Usage:
    python3 unified.py [command]

Commands:
    factory     - Run Content Factory (Menu for options)
    mail        - Run/Check Mail Processor
    sync        - Run Vibranium Full Sync
    brief       - Run Morning Brief (Family Assistant)
    status      - Show System Status Overview
    dashboard   - Launch ChatKit Dashboard
    help        - Show this help message
"""

import subprocess
import sys
from pathlib import Path

# Paths
ROOT_DIR = Path(__file__).parent.resolve()
VENV_PYTHON = ROOT_DIR / ".venv/bin/python"
SCRIPTS_DIR = ROOT_DIR / "Scripts"
PROJECTS_DIR = ROOT_DIR / "Projects"

# Import Conscience
sys.path.append(str(SCRIPTS_DIR))  # Ensure Scripts/ is in path
from Core.conscience import Conscience  # noqa: E402

conscience = Conscience(ROOT_DIR / "NOTEBOOK.md")

# Define colors
GREEN = "\033[92m"
BLUE = "\033[94m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"


def print_header():
    print(f"{BLUE}╔════════════════════════════════════════════════════╗{RESET}")
    print(f"{BLUE}║           UNIFIED SYSTEM MASTER CONTROLLER         ║{RESET}")
    print(f"{BLUE}╚════════════════════════════════════════════════════╝{RESET}")


def run_command(cmd, cwd=None, env=None):
    """Run a shell command properly"""
    try:
        if cwd:
            print(f"{YELLOW}📂 CWD: {cwd}{RESET}")
        print(f"{YELLOW}🚀 Executing: {' '.join(cmd)}{RESET}")
        subprocess.run(cmd, cwd=cwd, env=env, check=False)
    except KeyboardInterrupt:
        print(f"\n{RED}⛔ Interrupted by user.{RESET}")
    except Exception as e:
        print(f"{RED}❌ Error: {e}{RESET}")


# ================= MODULES =================


def run_factory():
    print(f"\n{GREEN}🏭 CONTENT FACTORY CONTROLLER{RESET}")
    print("1. Run Daily (Auto-detect)")
    print("2. Run Special (Manual Args)")
    print("3. Start Scheduler (Daemon)")
    print("4. YouTube Inspiration Mode (Search & Create)")

    choice = input(f"{YELLOW}Select option [1-4]: {RESET}")

    factory_script = PROJECTS_DIR / "Content_Factory/src/pipeline/factory_scheduler.py"

    if choice == "1":
        run_command([str(VENV_PYTHON), str(factory_script), "--auto-upload"])
    elif choice == "2":
        args = input("Enter arguments (e.g. --cartoon --style sketch): ")
        run_command([str(VENV_PYTHON), str(factory_script)] + args.split())
    elif choice == "3":
        run_command([str(VENV_PYTHON), str(factory_script), "--scheduler"])
    elif choice == "4":
        topic = input("Enter Inspiration Topic: ")
        outline = input("Enter Inspiration Outline (Optional): ")
        style = input("Choose Style (impact/cartoon/sketch/painting): ")

        cmd = [str(VENV_PYTHON), str(factory_script), "--inspiration-topic", topic, "--auto-upload"]
        if outline:
            cmd.extend(["--inspiration-outline", outline])
        if style:
            cmd.extend(["--style", style])
        run_command(cmd)


def run_mail():
    print(f"\n{GREEN}📧 MAIL PROCESSOR CONTROLLER{RESET}")
    script = SCRIPTS_DIR / "Orchestration/mail_processor.py"
    print("1. Run Once (Process Inbox)")
    print("2. Start Daemon Mode")

    choice = input(f"{YELLOW}Select option [1-2]: {RESET}")
    if choice == "1":
        run_command([str(VENV_PYTHON), str(script), "--once"])
    elif choice == "2":
        run_command([str(VENV_PYTHON), str(script)])


def run_sync():
    print(f"\n{GREEN}🔄 VIBRANIUM SYNC{RESET}")
    script = SCRIPTS_DIR / "Orchestration/vibranium-sync.sh"
    run_command(["bash", str(script)])


def run_brief():
    print(f"\n{GREEN}🌅 MORNING BRIEF (FAMILY ASSISTANT){RESET}")
    script = SCRIPTS_DIR / "Family/morning_brief.py"
    run_command([str(VENV_PYTHON), str(script)])


def run_status():
    print(f"\n{GREEN}📊 SYSTEM STATUS{RESET}")
    # Run the simplified status check
    print("Checking active services...")
    subprocess.run(["ps", "aux"], capture_output=False)  # Simplified, usually we'd grep
    print("\n--- Quick Listeners Check ---")
    subprocess.run(["lsof", "-i", "-P", "-n"], capture_output=False)


def run_dashboard():
    print(f"\n{GREEN}📈 CHATKIT DASHBOARD{RESET}")
    dashboard_dir = PROJECTS_DIR / "ChatKit_Dashboard"
    print("Starting Next.js Dashboard...")
    run_command(["npm", "run", "dev"], cwd=dashboard_dir)


# ================= MENU =================


def main_menu():
    print_header()
    print("1. 🏭 Content Factory")
    print("2. 📧 Mail Intelligence")
    print("3. 🔄 System Sync")
    print("4. 🌅 Family Assistant")
    print("5. 📈 Dashboard")
    print("6. 📊 Status")
    print("7. ⚖️  Conscience")
    print("0. 🚪 Exit")

    choice = input(f"\n{YELLOW}Choose module: {RESET}")

    if choice == "1":
        run_factory()
    elif choice == "2":
        run_mail()
    elif choice == "3":
        if conscience.check_action("deploy status sync"):  # Example check
            run_sync()
    elif choice == "4":
        run_brief()
    elif choice == "5":
        run_dashboard()
    elif choice == "6":
        run_status()
    elif choice == "7":
        conscience.state_rules()
    elif choice == "0":
        sys.exit(0)
    else:
        main_menu()


# ================= MAIN =================


if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        if cmd == "factory":
            run_factory()
        elif cmd == "mail":
            run_mail()
        elif cmd == "sync":
            run_sync()
        elif cmd == "brief":
            run_brief()
        elif cmd == "status":
            run_status()
        elif cmd == "dashboard":
            run_dashboard()
        else:
            print(f"Unknown command: {cmd}")
            print(__doc__)
    else:
        try:
            while True:
                main_menu()
                try:
                    input(f"\n{BLUE}Press Enter to continue...{RESET}")
                except EOFError:
                    break
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
