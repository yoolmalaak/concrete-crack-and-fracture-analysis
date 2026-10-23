from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


# Set paths
REPO_ROOT = Path(
    r"C:\Users\yoolm\Documents\concrete-crack-and-fracture-analysis"
)

CSV_PATH = (
    REPO_ROOT
    / "results"
    / "tables"
    / "sdnet2018_morphology_6000.csv"
)

FIGURES_DIR = REPO_ROOT / "results" / "figures"

FIGURES_DIR.mkdir(parents=True, exist_ok=True)


# Load morphology dataset
morphology = pd.read_csv(CSV_PATH)

print(f"Loaded: {CSV_PATH.name}")
print(f"Rows: {len(morphology)}")
print(f"Columns: {len(morphology.columns)}")


# Check required columns
required_columns = [
    "crack_area_percentage",
    "crack_length_pixels",
    "mean_width_pixels",
    "max_width_pixels",
    "dominant_orientation_deg",
    "branching_points",
]

missing_columns = [
    column
    for column in required_columns
    if column not in morphology.columns
]

if missing_columns:
    raise ValueError(
        f"Missing columns: {missing_columns}"
    )


# Keep only images with predicted crack regions
morphology = morphology[
    morphology["crack_area_percentage"] > 0
].copy()

print(f"Images with predicted crack regions: {len(morphology)}")


# Create figure
fig = plt.figure(figsize=(12, 16), constrained_layout=True)

ax1 = fig.add_subplot(3, 2, 1)
ax2 = fig.add_subplot(3, 2, 2)
ax3 = fig.add_subplot(3, 2, 3)
ax4 = fig.add_subplot(3, 2, 4)
ax5 = fig.add_subplot(3, 2, 5, projection="polar")
ax6 = fig.add_subplot(3, 2, 6)


# Crack area
ax1.hist(
    morphology["crack_area_percentage"],
    bins=30
)
ax1.set_title("(a) Predicted Crack Area", fontsize=11)
ax1.set_xlabel("Crack area (%)")
ax1.set_ylabel("Number of images")


# Crack length
ax2.hist(
    morphology["crack_length_pixels"],
    bins=30
)
ax2.set_title("(b) Predicted Crack Length", fontsize=11)
ax2.set_xlabel("Crack length (pixels)")
ax2.set_ylabel("Number of images")


# Mean crack width
ax3.hist(
    morphology["mean_width_pixels"],
    bins=30
)
ax3.set_title("(c) Predicted Mean Crack Width", fontsize=11)
ax3.set_xlabel("Mean width (pixels)")
ax3.set_ylabel("Number of images")


# Maximum crack width
ax4.hist(
    morphology["max_width_pixels"],
    bins=30
)
ax4.set_title("(d) Predicted Maximum Crack Width", fontsize=11)
ax4.set_xlabel("Maximum width (pixels)")
ax4.set_ylabel("Number of images")


# Crack orientation
angles = morphology[
    "dominant_orientation_deg"
].dropna()

angles_rad = np.deg2rad(angles)

ax5.hist(
    angles_rad,
    bins=18
)
ax5.set_title(
    "(e) Predicted Crack Orientation",
    fontsize=11,
    pad=15
)
ax5.set_theta_zero_location("E")
ax5.set_theta_direction(1)


# Branching points
ax6.hist(
    morphology["branching_points"],
    bins=30
)
ax6.set_title("(f) Predicted Crack Branching Points", fontsize=11)
ax6.set_xlabel("Number of branching points")
ax6.set_ylabel("Number of images")


# Overall title
fig.suptitle(
    "Distributions of Predicted Crack Morphology Descriptors",
    fontsize=15
)


# Save figure
output_path = (
    FIGURES_DIR
    / "crack_morphology_distributions.png"
)

plt.savefig(
    output_path,
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("\nFigure created successfully.")
print(f"Saved to: {output_path}")
