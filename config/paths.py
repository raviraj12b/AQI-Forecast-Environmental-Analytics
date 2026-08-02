"""
Centralized path configuration for the AQI Forecast & Environmental
Analytics Platform.

All file and directory paths used throughout the project should be
imported from this module rather than hardcoded, per NFR-SEC-002
(Path Safety) and Master Development Handbook Section 5.8
(Configuration Management).
"""

from pathlib import Path

# Project root (this file lives at <root>/config/paths.py)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Data directories (ML-DATA-001/002)
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
INTERIM_DATA_DIR = DATA_DIR / "interim"
EXTERNAL_DATA_DIR = DATA_DIR / "external"
SAMPLE_DATA_DIR = DATA_DIR / "samples"
METADATA_DIR = DATA_DIR / "metadata"

# Model artifact directories (ML-REG-001)
MODELS_DIR = PROJECT_ROOT / "models"
TRAINED_MODELS_DIR = MODELS_DIR / "trained"
MODEL_CHECKPOINTS_DIR = MODELS_DIR / "checkpoints"
MODEL_METADATA_DIR = MODELS_DIR / "metadata"
MODEL_EXPERIMENTS_DIR = MODELS_DIR / "experiments"
MODEL_ARCHIVE_DIR = MODELS_DIR / "archive"

# Generated output directories
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
FORECASTS_DIR = OUTPUTS_DIR / "forecasts"
REPORTS_DIR = OUTPUTS_DIR / "reports"
CHARTS_DIR = OUTPUTS_DIR / "charts"
EXPORTS_DIR = OUTPUTS_DIR / "exports"
LOGS_DIR = OUTPUTS_DIR / "logs"
PERFORMANCE_DIR = OUTPUTS_DIR / "performance"

# Application code
SRC_DIR = PROJECT_ROOT / "src"
DASHBOARD_DIR = PROJECT_ROOT / "dashboard"

# Documentation and static assets
DOCS_DIR = PROJECT_ROOT / "docs"
ASSETS_DIR = PROJECT_ROOT / "assets"


def ensure_directories_exist() -> None:
    """
    Create every generated-output directory if it does not already exist.

    This lets the application run safely even if an optional output
    directory was pruned or excluded from version control, without
    requiring manual setup (NFR-REL-003, Error Recovery).
    """
    directories = [
        RAW_DATA_DIR, PROCESSED_DATA_DIR, INTERIM_DATA_DIR,
        EXTERNAL_DATA_DIR, SAMPLE_DATA_DIR, METADATA_DIR,
        TRAINED_MODELS_DIR, MODEL_CHECKPOINTS_DIR, MODEL_METADATA_DIR,
        MODEL_EXPERIMENTS_DIR, MODEL_ARCHIVE_DIR,
        FORECASTS_DIR, REPORTS_DIR, CHARTS_DIR, EXPORTS_DIR,
        LOGS_DIR, PERFORMANCE_DIR,
    ]
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
