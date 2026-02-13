#!/usr/bin/env python3
"""
System Health Check Tool
Diagnoses common issues in the Unified System Core
"""

import os
import subprocess
import sys
from pathlib import Path


def check_python_version() -> tuple[bool, str]:
    """Check if Python version is adequate"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 9:
        return True, f"✓ Python {version.major}.{version.minor}.{version.micro}"
    return False, f"✗ Python {version.major}.{version.minor}.{version.micro} (need 3.9+)"


def check_ai_core_dependencies() -> tuple[bool, str]:
    """Check if AI Core dependencies are installed"""
    ai_core_path = Path(__file__).parent.parent.parent / "Projects" / "AI_Core"
    requirements_file = ai_core_path / "requirements.txt"

    if not requirements_file.exists():
        return False, "✗ AI Core requirements.txt not found"

    dependencies = ["google.generativeai", "openai", "telegram"]
    missing = []

    import importlib.util

    for dep in dependencies:
        if importlib.util.find_spec(dep) is None:
            missing.append(dep)

    if not missing:
        return True, "✓ AI Core dependencies installed"

    return False, f"✗ Missing dependencies: {', '.join(missing)}"


def check_env_files() -> tuple[bool, str]:
    """Check if environment files exist"""
    root = Path(__file__).parent.parent.parent
    env_files = [".env.example", ".env.local"]

    found = []
    for env_file in env_files:
        if (root / env_file).exists():
            found.append(env_file)

    if found:
        return True, f"✓ Environment files: {', '.join(found)}"
    return False, "✗ No environment files found"


def check_git_status() -> tuple[bool, str]:
    """Check git repository status"""
    try:
        result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, check=True)
        if result.stdout.strip():
            lines = len(result.stdout.strip().split("\n"))
            return True, f"⚠ {lines} uncommitted changes"
        return True, "✓ Working tree clean"
    except subprocess.CalledProcessError:
        return False, "✗ Git status check failed"


def check_scripts_executable() -> tuple[bool, str]:
    """Check if key scripts are executable"""
    root = Path(__file__).parent.parent.parent
    scripts = [
        "check_system.sh",
        "start_brain.sh",
    ]

    executable = []
    for script in scripts:
        script_path = root / script
        if script_path.exists() and os.access(script_path, os.X_OK):
            executable.append(script)

    if executable:
        return True, f"✓ Executable scripts: {len(executable)}/{len(scripts)}"
    return False, "✗ No executable scripts found"


def check_project_directories() -> tuple[bool, str]:
    """Check if main project directories exist"""
    root = Path(__file__).parent.parent.parent
    required_dirs = [
        "Projects/AI_Core",
        "Scripts",
        "Agent_Context",
    ]

    missing = []
    for dir_path in required_dirs:
        if not (root / dir_path).exists():
            missing.append(dir_path)

    if not missing:
        return True, f"✓ All {len(required_dirs)} project directories exist"
    return False, f"✗ Missing: {', '.join(missing)}"


def run_health_check():
    """Run all health checks"""
    print("=" * 60)
    print("🏥 Unified System Core - Health Check")
    print("=" * 60)
    print()

    checks = [
        ("Python Version", check_python_version),
        ("Project Directories", check_project_directories),
        ("Environment Files", check_env_files),
        ("Git Status", check_git_status),
        ("Executable Scripts", check_scripts_executable),
        ("AI Core Dependencies", check_ai_core_dependencies),
    ]

    results = []
    for name, check_func in checks:
        success, message = check_func()
        results.append((name, success, message))
        print(f"{message}")

    print()
    print("=" * 60)

    passed = sum(1 for _, success, _ in results if success)
    total = len(results)

    if passed == total:
        print(f"✓ All checks passed ({passed}/{total})")
        print("=" * 60)
        return 0
    else:
        print(f"⚠ Some checks failed ({passed}/{total} passed)")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    sys.exit(run_health_check())
