# Concrete Crack and Fracture Analysis

A data-driven study of concrete crack patterns and fracture energy using **deep learning, image processing, and machine learning**.

## Overview

This project uses three public datasets, analysed in two independent parts:

| Dataset | Content | Used for |
| --- | --- | --- |
| **CrackSeg9K** | Crack images with segmentation masks | Training the U-Net segmentation model |
| **SDNET2018** | 56,092 concrete images (cracked / uncracked) | CNN classification; U-Net transfer and crack morphology analysis |
| **ConcreteTBF** | 330 three-point-bending fracture observations | Fracture-energy (`Gc`) prediction |

The image datasets and ConcreteTBF are analysed independently because they do not contain specimen-level correspondence.

## Methodology

### 1. Crack image analysis

- **CNN classification:** cracked / uncracked classification on SDNET2018, used as a baseline.
- **U-Net segmentation:** trained on CrackSeg9K, then transferred to SDNET2018 (transfer learning) to segment crack regions.
- **Morphology extraction** from predicted crack masks (6,000 SDNET2018 images analysed): crack area, length, width, orientation, and branching.

### 2. Fracture energy analysis

Machine-learning regression models predict the reported fracture energy (`Gc`) from:

`d` (specimen depth), `S` (span), `bw` (specimen width), `a0` (initial notch length), `ft` (tensile strength), `E` (elastic modulus)

Models: Linear Regression, Random Forest, Gradient Boosting, XGBoost.

Models were trained with five-fold cross-validation and evaluated on an independent test set, using fixed, manually specified hyperparameters. No systematic hyperparameter search was performed.

## Key Results

### Crack classification (CNN baseline, SDNET2018 test set, 8,414 images)

| Metric | Value |
| --- | ---: |
| ROC-AUC | **0.8553** |
| Cracked-class recall | 68.00% |
| Cracked-class precision | 47.21% |
| Cracked-class F1 | 55.73% |
| Accuracy | 83.67% |

> Only about 15% of the test images are cracked, so accuracy is not a reliable measure here (always predicting "uncracked" would score about 85%). ROC-AUC, recall, and F1 are more informative. This CNN is a baseline; class-imbalance handling and threshold tuning are future work.

### Crack segmentation (U-Net, CrackSeg9K)

| Split | Dice | IoU |
| --- | ---: | ---: |
| Validation | 0.7215 | 0.6061 |
| Test | **0.6855** | **0.5659** |

### Crack morphology (SDNET2018, U-Net predictions)

Of 6,000 images, 2,601 (43.35%) contained predicted crack regions (1,896 labelled cracked and 705 labelled uncracked in the original dataset). Descriptors were computed for these 2,601 images, in pixel units.

| Descriptor | Mean | Median | Maximum |
| --- | ---: | ---: | ---: |
| Crack area (%) | 3.05 | 2.07 | 26.14 |
| Crack length (px) | 221.6 | 211.4 | 1023.2 |
| Mean crack width (px) | 5.87 | 5.29 | 23.42 |
| Maximum crack width (px) | 15.76 | 13.42 | 72.80 |
| Branching points | 3.57 | 0 | 66 |

Most predicted cracks are unbranched (median 0 branching points), with a minority of heavily branched cracks.

### Fracture energy prediction (`Gc`, ConcreteTBF)

| Model | CV R² | CV RMSE (N/mm) | Test R² | Test RMSE (N/mm) | Test MAE (N/mm) |
| --- | ---: | ---: | ---: | ---: | ---: |
| Linear Regression | 0.077 | 0.0261 | 0.125 | 0.0259 | 0.0205 |
| **Random Forest** | **0.438** | **0.0204** | **0.605** | **0.0174** | 0.0127 |
| Gradient Boosting | 0.380 | 0.0215 | 0.540 | 0.0188 | **0.0124** |
| XGBoost | 0.426 | 0.0207 | 0.549 | 0.0186 | 0.0138 |

Nonlinear ensemble models clearly outperformed Linear Regression, indicating a nonlinear relationship between the inputs and fracture energy. Predictive accuracy remains moderate, which is expected with only 330 observations.

## Limitations

- The two parts (crack images and fracture energy) are not linked at specimen level.
- Segmentation scores (Dice 0.69, IoU 0.57) reflect the difficulty of thin, irregular cracks; some predicted cracks in images labelled "uncracked" may be false positives or unlabelled cracks.
- Morphology measurements are in pixels and are not calibrated to physical units.
- The fracture-energy dataset is small, and no hyperparameter search was performed.

## Scope

This project does **not** establish a direct image-to-fracture-energy or
image-to-fracture-toughness relationship. The datasets are analyzed independently
and interpreted as complementary sources of information.

## Datasets

- [CrackSeg9K](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/EGIEBY)
crack segmentation dataset.
- [SDNET2018](https://www.kaggle.com/datasets/atharv0919/sdnet2018-a-concrete-crack-image-dataset)
Concrete crack dataset
- [ConcreteTBF](https://figshare.com/articles/dataset/ML_Dataset_Concrete_Three-Point_Bending_Fracture/25529512?file=45422050)
**Concrete Three-Point Bending Fracture dataset.**

The original datasets are not redistributed in this repository. Download them
from their original sources and place them in `data/` (see the notebooks for
the expected folder layout).
The links to the data source has been provided above.

## Repository Structure

```text
concrete-crack-and-fracture-analysis/
│
├── notebooks/
│   ├── crack_classification/
│   ├── crack_segmentation/
│   ├── crack_morphology/
│   └── fracture_energy/
│
├── data/              # empty: download datasets separately
├── models/
├── results/
├── figures/
├── requirements.txt
└── README.md
```

## Getting Started

```bash
git clone https://github.com/yoolmalaak/concrete-crack-and-fracture-analysis.git
cd concrete-crack-and-fracture-analysis
pip install -r requirements.txt
```

Download the datasets into `data/`, then run the notebooks in this order: `crack_classification`,
`crack_segmentation`
`crack_morphology`, `fracture_energy`.

## Tools

**Python · PyTorch · torchvision
· OpenCV · NumPy · pandas · scikit-learn · XGBoost · Matplotlib**

## Author

**Yool Malaak Yool Ajak**
Civil Engineering | Data Science | Machine Learning

[GitHub](https://github.com/yoolmalaak) · [LinkedIn](https://www.linkedin.com/in/yoolmalaak/)
