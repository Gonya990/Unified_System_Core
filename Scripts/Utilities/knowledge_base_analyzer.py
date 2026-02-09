import argparse
import hashlib
import logging
import os
import zipfile
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent.parent
CONTEXTS_DIR = ROOT_DIR / "contexts"
EXTRACT_DIR = CONTEXTS_DIR / "temp_extract"
GDRIVE_PATH = Path(
    "/Users/igorgoncharenko/Library/CloudStorage/GoogleDrive-gonya90.gg@gmail.com/My Drive"
)  # Assuming 'My Drive' is the root


def get_file_hash(path):
    """Calculate SHA256 hash of a file."""
    sha256 = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
        return sha256.hexdigest()
    except Exception as e:
        logger.error(f"Error hashing {path}: {e}")
        return None


def analyze_archives():
    """Extract and analyze archives."""
    if not EXTRACT_DIR.exists():
        EXTRACT_DIR.mkdir(parents=True)

    archives = list(CONTEXTS_DIR.glob("*.zip"))
    logger.info(f"Found {len(archives)} archives: {[a.name for a in archives]}")

    file_index = {}  # hash -> [list of paths]

    for archive in archives:
        logger.info(f"Processing {archive.name}...")
        try:
            with zipfile.ZipFile(archive, "r") as z:
                # We can list first to avoid extracting if mostly dupes?
                # For now, let's extract to a specific subfolder per archive
                archive_extract_path = EXTRACT_DIR / archive.stem
                z.extractall(archive_extract_path)

                logger.info(f"Extracted to {archive_extract_path}")

                # Walk and Hash
                for root, _, files in os.walk(archive_extract_path):
                    for file in files:
                        file_path = Path(root) / file
                        fhash = get_file_hash(file_path)
                        if fhash:
                            if fhash not in file_index:
                                file_index[fhash] = []
                            file_index[fhash].append(file_path)

        except Exception as e:
            logger.error(f"Failed to process {archive.name}: {e}")

    return file_index


def find_gdrive_duplicates(local_index, gdrive_root):
    """Scan Google Drive and find duplicates."""
    logger.info(f"Scanning Google Drive at {gdrive_root}...")
    duplicates = []

    for root, _, files in os.walk(gdrive_root):
        for file in files:
            g_path = Path(root) / file
            # Optimization: Check size first?
            # For now, just hash.
            g_hash = get_file_hash(g_path)

            if g_hash and g_hash in local_index:
                logger.warning(f"DUPLICATE FOUND: {g_path}")
                duplicates.append(g_path)
                # local_paths = local_index[g_hash]
                # logger.info(f"Matches local files: {local_paths}")

    return duplicates


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--delete", action="store_true", help="Actually delete duplicates from Google Drive")
    args = parser.parse_args()

    # 1. Analyze Local Archives
    index = analyze_archives()
    logger.info(f"Indexed {len(index)} unique files.")

    # 2. Deduplicate
    if GDRIVE_PATH and GDRIVE_PATH.exists():
        dupes = find_gdrive_duplicates(index, GDRIVE_PATH)
        logger.info(f"Found {len(dupes)} duplicates in Google Drive.")

        if args.delete:
            logger.info("DELETE MODE ACTIVE. Removing duplicates...")
            for d in dupes:
                try:
                    os.remove(d)
                    logger.info(f"Deleted: {d}")
                except Exception as e:
                    logger.error(f"Failed to delete {d}: {e}")
        else:
            logger.info("Dry Run. Use --delete to remove files.")
            for d in dupes:
                print(f"Would delete: {d}")
    else:
        logger.error(f"Google Drive path not found: {GDRIVE_PATH}")
