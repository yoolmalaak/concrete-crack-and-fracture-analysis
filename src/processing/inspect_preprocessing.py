from pathlib import Path
import random

import cv2
import numpy as np
import matplotlib.pyplot as plt


# Project paths

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATASET_DIR = PROJECT_ROOT / "data" / "raw" / "sdnet2018"


# Select representative cracked images

SURFACES = ["deck", "pavement", "wall"]

random.seed(42)


def get_cracked_images(surface):
    folder = DATASET_DIR / surface / "crack_dataset"

    images = [
        p for p in folder.rglob("*")
        if p.is_file()
        and p.suffix.lower() in {".jpg", ".jpeg", ".png"}
    ]

    return images

# Preprocessing functions

def preprocess_image(image):
    """
    Generate candidate preprocessing representations.
    """

    # RGB image loaded by OpenCV is BGR
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Mild Gaussian smoothing
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # CLAHE contrast enhancement
    clahe = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8)
    )

    enhanced = clahe.apply(blurred)

    return rgb, gray, blurred, enhanced


# Main inspection

def main():

    print("=" * 70)
    print("SDNET2018 IMAGE PREPROCESSING INSPECTION")
    print("=" * 70)

    for surface in SURFACES:

        images = get_cracked_images(surface)

        if not images:
            print(f"No images found for {surface}.")
            continue

        selected = random.choice(images)

        image = cv2.imread(str(selected))

        if image is None:
            print(f"Could not read: {selected}")
            continue

        rgb, gray, blurred, enhanced = preprocess_image(image)

        print()
        print(f"Surface: {surface}")
        print(f"Image:   {selected.name}")
        print(f"Size:    {rgb.shape[1]} x {rgb.shape[0]}")
        print()

        # Display

        fig, axes = plt.subplots(1, 4, figsize=(16, 4))

        axes[0].imshow(rgb)
        axes[0].set_title("Original RGB")
        axes[0].axis("off")

        axes[1].imshow(gray, cmap="gray")
        axes[1].set_title("Grayscale")
        axes[1].axis("off")

        axes[2].imshow(blurred, cmap="gray")
        axes[2].set_title("Gaussian Filter")
        axes[2].axis("off")

        axes[3].imshow(enhanced, cmap="gray")
        axes[3].set_title("CLAHE Enhanced")
        axes[3].axis("off")

        fig.suptitle(
            f"SDNET2018 Preprocessing Inspection — {surface}",
            fontsize=14
        )

        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    main()
