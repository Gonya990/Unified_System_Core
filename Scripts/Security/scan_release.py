#!/usr/bin/env python3
"""
VirusTotal Security Check Script for Release Artifacts.
Based on OpenClaw/VirusTotal partnership principles:
1. Deterministic Packaging
2. Hash Computation
3. VirusTotal Lookup (Manual link provision or API if enabled)

Usage:
    python scan_release.py <directory_to_scan>
"""

import hashlib
import os
import shutil
import sys
import time


def compute_sha256(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def package_and_scan(target_dir):
    if not os.path.isdir(target_dir):
        print(f"❌ Error: {target_dir} is not a directory.")
        return

    project_name = os.path.basename(os.path.abspath(target_dir))
    timestamp = int(time.time())
    archive_name = f"{project_name}_release_{timestamp}"
    archive_path = shutil.make_archive(archive_name, "zip", target_dir)

    print(f"📦 Packaged: {archive_path}")

    file_hash = compute_sha256(archive_path)
    print(f"🔑 SHA-256: {file_hash}")

    vt_url = f"https://www.virustotal.com/gui/file/{file_hash}"
    print(f"🔍 VirusTotal Link: {vt_url}")
    print("\n✅ Steps for Release:")
    print("1. Upload this ZIP to VirusTotal if 'File not found'.")
    print("2. Verify 'Code Insight' report.")
    print("3. If benign, proceed with deployment.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scan_release.py <directory>")
    else:
        package_and_scan(sys.argv[1])
