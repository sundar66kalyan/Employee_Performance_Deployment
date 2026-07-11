"""
=========================================================
Project Configuration
=========================================================
"""

import os

# ---------------------------------------------------------
# Project Root
# ---------------------------------------------------------

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

# ---------------------------------------------------------
# Data Folders
# ---------------------------------------------------------

DATA_FOLDER = os.path.join(PROJECT_ROOT, "data")

RAW_DATA_FOLDER = os.path.join(DATA_FOLDER, "raw")

PROCESSED_DATA_FOLDER = os.path.join(DATA_FOLDER, "processed")

EXTERNAL_DATA_FOLDER = os.path.join(DATA_FOLDER, "external")

# ---------------------------------------------------------
# Output Folders
# ---------------------------------------------------------

MODELS_FOLDER = os.path.join(PROJECT_ROOT, "models")

RESULTS_FOLDER = os.path.join(PROJECT_ROOT, "results")

FIGURES_FOLDER = os.path.join(PROJECT_ROOT, "figures")

# ---------------------------------------------------------
# Dataset
# ---------------------------------------------------------

DATASET_NAME = "INX_Future_Inc_Employee_Performance_CDS_Project2_Data_V1.8.xls"

DATASET_PATH = os.path.join(
    RAW_DATA_FOLDER,
    DATASET_NAME
)

# ---------------------------------------------------------
# Standard Project Aliases
# ---------------------------------------------------------

MODEL_DIR = MODELS_FOLDER

RESULT_DIR = RESULTS_FOLDER