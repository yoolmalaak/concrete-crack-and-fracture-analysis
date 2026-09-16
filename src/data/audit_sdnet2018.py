from pathlib import Path
from collections import Counter
from PIL import Image

# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# SDNET2018 raw-data directory
DATASET_DIR = PROJECT_ROOT / "data" / "raw" / "sdnet2018"

SURFACE_TYPES = ["deck", "pavement", "wall"]

CLASS_FOLDERS = {
    "crack_dataset": "cracked",
    "uncrack_dataset": "uncracked",
}

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}

# Number of images to inspect from each folder
SAMPLE_SIZE = 5


def audit_dataset():

    print("=" * 70)
    print("SDNET2018 DATASET AUDIT")
    print("=" * 70)
    print(f"Dataset path: {DATASET_DIR}")
    print()

    if not DATASET_DIR.exists():
        print("ERROR: Dataset directory was not found.")
        return

    total_images = 0

    print("IMAGE COUNTS")
    print("-" * 70)

    for surface in SURFACE_TYPES:

        for folder, label in CLASS_FOLDERS.items():

            folder_path = DATASET_DIR / surface / folder

            if not folder_path.exists():
                print(f"WARNING: Missing folder: {folder_path}")
                continue

            # Find image files recursively
            image_files = [
                p for p in folder_path.rglob("*")
                if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS
            ]

            count = len(image_files)
            total_images += count

            print(
                f"{surface:<12} "
                f"{label:<12} "
                f"{count:>8}"
            )

    print("-" * 70)
    print(f"{'TOTAL':<24} {total_images:>8}")
    print()

    # Sample image inspection

    print("SAMPLE IMAGE INSPECTION")
    print("-" * 70)

    for surface in SURFACE_TYPES:

        for folder, label in CLASS_FOLDERS.items():

            folder_path = DATASET_DIR / surface / folder

            if not folder_path.exists():
                continue

            image_files = [
                p for p in folder_path.rglob("*")
                if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS
            ]

            sample = image_files[:SAMPLE_SIZE]

            dimensions = Counter()
            modes = Counter()
            unreadable = 0

            for image_path in sample:

                try:
                    with Image.open(image_path) as img:
                        dimensions[img.size] += 1
                        modes[img.mode] += 1

                except Exception:
                    unreadable += 1

            print(f"{surface} / {label}")
            print(f"  Sample size: {len(sample)}")
            print(f"  Dimensions: {dict(dimensions)}")
            print(f"  Modes: {dict(modes)}")
            print(f"  Unreadable in sample: {unreadable}")

    print()
    print("AUDIT COMPLETE")


if __name__ == "__main__":
    audit_dataset()
