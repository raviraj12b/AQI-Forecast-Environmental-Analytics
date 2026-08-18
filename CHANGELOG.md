# Changelog

All notable changes to the AQI Forecast & Environmental Analytics Platform
are documented in this file.

## [Unreleased]

### Added
- Initial project folder structure (Milestone 1).
- Centralized configuration module (`config/`).
- `requirements.txt`, `.gitignore`, MIT `LICENSE`, initial `README.md`.
- Dataset selection/provenance documentation (`data/metadata/DATASET_SOURCE.md`).
- Data loading, validation, and cleaning modules (`src/preprocessing/`, FR-DATA-001/002/003/004/005).
- Shared `src/utils/exceptions.py` and `src/utils/logger.py`.
- Full unit test suite for the data layer (synthetic fixture-based).
- **Real Delhi AQI dataset placed at `data/raw/Delhi_AQI_Dataset.csv`** (2,191 rows, 2018–2024).
- **`01_data_understanding.ipynb`, `02_data_cleaning.ipynb`, `03_exploratory_data_analysis.ipynb`**
  — real, executed notebooks (18 charts across 10 required ML-EDA-002 chart types, each interpreted).
- **`data/metadata/DATA_QUALITY_REPORT.md`** — Milestone 2 quality report deliverable.
- Cleaned dataset persisted to `data/processed/delhi_aqi_cleaned.csv`.

### Fixed
- **Date-parsing bug** in `data_loader.py`: default parsing silently
  corrupted 36% of the real dataset's dates (ambiguous `DD/MM/YY` vs
  `MM/DD/YY`). Added `dayfirst`/`date_format` parameters; regression test added.

### Key findings
- Pollutant columns are exact linear transforms of AQI (`PM2.5 = 0.55 × AQI`,
  r = 1.00) — excluded from future model input features (data-leakage risk).
- 366 calendar-day gaps (14.3%) in the date range — flagged for Milestone 3.
- Strong seasonal signal (winter ≈ 2× monsoon AQI); weak day-of-week signal.
