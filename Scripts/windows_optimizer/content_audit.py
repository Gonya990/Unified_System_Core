import json
import os

# Configuration
TARGET_FOLDERS = [
    "SteamLibrary",
    "Epic Games",
    "Games",
    "MyGames",
    ".ollama",
    ".cache/huggingface",
    "ComfyUI",
    "Automatic1111",
    "invokeai",
    "Downloads",
    "Documents",
    "Desktop",
    "Saved Games",
]


def load_hardware_report():
    try:
        with open("hardware_report.json", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("Hardware report not found. Running blind.")
        return []


def get_folder_size_gb(folder_path):
    total_size = 0
    try:
        for dirpath, dirnames, filenames in os.walk(folder_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if not os.path.islink(fp):
                    total_size += os.path.getsize(fp)
    except Exception:
        pass
    return round(total_size / (1024**3), 2)


def main():
    print("SEARCHING FOR HIGH-VALUE ASSETS...")

    disks = load_hardware_report()
    drives = []

    # Map letters to Tiers
    tier_map = {}
    for disk in disks:
        tier = disk.get("PerformanceTier", "Unknown")
        for part in disk.get("Partitions", []):
            drive_letter = part.get("DriveLetter")  # "C:"
            if drive_letter:
                drives.append(drive_letter)
                tier_map[drive_letter] = tier

    recommendations = []
    found_assets = []

    for drive in drives:  # ["C:", "D:", ...]
        tier = tier_map.get(drive, "Unknown")
        print(f"\nScanning {drive} ({tier})...")

        # Check explicit roots
        roots_to_check = [drive + "\\", drive + "\\Users\\gonya\\"]

        for root in roots_to_check:
            if not os.path.exists(root):
                continue

            for target in TARGET_FOLDERS:
                candidate = os.path.join(root, target)
                if os.path.exists(candidate):
                    size = get_folder_size_gb(candidate)
                    asset_info = {
                        "name": target,
                        "path": candidate,
                        "size_gb": size,
                        "current_tier": tier,
                        "drive": drive,
                    }
                    found_assets.append(asset_info)
                    print(f"  FOUND: {candidate} ({size} GB)")

                    # Logic for recommendations
                    if "TIER 3" in tier or "HDD" in tier:
                        if size > 0 and size < 100:  # Small enough to move?
                            # Suggest move to NVMe if available
                            pass

    print("\n" + "=" * 50)
    print("OPTIMIZATION RECOMMENDATIONS")
    print("=" * 50)

    # Identify NVMe drive
    nvme_drive = next((d for d, t in tier_map.items() if "TIER 1" in t), None)

    for asset in found_assets:
        tier = asset["current_tier"]
        name = asset["name"]
        path = asset["path"]
        size = asset["size_gb"]

        if "HDD" in tier or "TIER 3" in tier:
            if nvme_drive:
                print(f"[!] MOVE [ {name} ] ({size} GB) from {tier} -> {nvme_drive} (NVMe)")
                print(f"    Source: {path}")
            else:
                print(f"[!] MOVE [ {name} ] ({size} GB) from {tier} -> SSD (if space permits)")

        elif "TIER 2" in tier and "NVMe" not in tier:
            # SATA SSD
            if name in [".ollama", "ComfyUI"]:
                if nvme_drive:
                    print(f"[+] BOOST [ {name} ] ({size} GB) by moving from SATA SSD -> {nvme_drive} (NVMe)")

    # Save report
    with open("content_report.json", "w", encoding="utf-8") as f:
        json.dump(found_assets, f, indent=4)
    print("\nSaved asset map to content_report.json")


if __name__ == "__main__":
    main()
