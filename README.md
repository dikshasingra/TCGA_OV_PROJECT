# TCGA_OV_PROJECT

## Overview
This repository contains a reproducible machine learning survival analysis pipeline for ovarian carcinoma.
It integrates TCGA gene expression data with survival information to identify prognostic biomarkers.

## Repository Structure
- **data_raw/** : Original raw input files (expression and survival tables).
- **data_processed/** : Preprocessed combined survival-expression data.
- **results/** : Model outputs, survival analyses, and summary statistics (CSV, TXT).
- **figures/** : Publication-ready plots (KM curves, feature importance, Cox forest plots).
- **manuscript.tex** : Draft manuscript in LaTeX format.
- **environment.yml** : Conda environment file for exact reproducibility.
- **tcga_ov_pipeline.py** : Main pipeline script.
- **ovarian_cancer_modeling.ipynb** : Interactive Jupyter notebook version.

## Reproducibility
1. Install dependencies:
   ```bash
   conda env create -f environment.yml
   conda activate tcga-ov-env
