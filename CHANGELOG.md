# Changelog

All notable changes to the AQI Forecast & Environmental Analytics Platform
are documented in this file.

## [Unreleased]

### Added
- Initial project folder structure (Milestone 1: Project Initialization).
- Centralized configuration module (`config/paths.py`, `config/constants.py`, `config/settings.py`).
- `requirements.txt` with core dependencies.
- `.gitignore` configured for Python/data-science projects.
- MIT `LICENSE`.
- Initial `README.md`.
- Dataset selection and provenance documentation (`data/metadata/DATASET_SOURCE.md`):
  Delhi AQI dataset from `cp099/India-Air-Quality-Dataset` (CC BY 4.0), confirmed
  schema matches ML-DATA-002 mandatory fields.
- Data loading module `src/preprocessing/data_loader.py` (FR-DATA-001).
- Data validation module `src/preprocessing/data_validator.py` (FR-DATA-002).
- Shared `src/utils/exceptions.py` and `src/utils/logger.py` utilities.
- Unit tests for loader and validator (15 verified passing checks) plus a
  synthetic, clearly-labeled test fixture (`tests/test_data/synthetic_aqi_fixture.csv`).
