# Data Quality Report — Delhi AQI Dataset

**Milestone:** MS-002 (Data Preparation) · **Date:** 2026-08 · **Dataset version:** `data/raw/Delhi_AQI_Dataset.csv` (2,191 rows)

This report summarizes the findings from `notebooks/01_data_understanding.ipynb`
and `notebooks/02_data_cleaning.ipynb`. Full detail, code, and charts live in
those notebooks; this is the auditable summary (PRD deliverable, MS-002).

## 1. Structural validation (FR-DATA-002)

| Check | Result |
|---|---|
| Required columns (ML-DATA-002) present | ✅ Pass — all 9 present |
| Duplicate column names | ✅ None |
| Empty dataset | ✅ Not empty (2,191 rows) |
| **Overall validation status** | **VALID** |

## 2. Issues found and how they were handled

| Issue | Severity | Rows/Cols affected | Action taken |
|---|---|---|---|
| 2 fully-empty columns (`Unnamed: 9`, `Unnamed: 10`) from a malformed CSV header (`...,O3,,`) | Low | 2 columns, 100% empty | Dropped explicitly in `02_data_cleaning.ipynb`, after confirming they were 100% null (not a blind column drop) |
| Dates ambiguous under default parsing (`DD/MM/YY` format) | **High** | 792/2,191 rows (36%) would have silently mis-parsed | Fixed in `src/preprocessing/data_loader.py` (added `dayfirst`/`date_format` params); regression test added (`test_load_dataset_dayfirst_prevents_ambiguous_date_corruption`) |
| Missing values in real data columns | None found | 0 | No action needed |
| Duplicate rows | None found | 0 | No action needed |
| Outliers (IQR method, all 7 numeric columns) | None found | 0 | No action needed |
| Outliers (Z-score, threshold 3.0, all 7 numeric columns) | None found | 0 | No action needed |
| 366 missing **calendar days** (14.3% of the 2018–2024 date range) — rows simply absent, not NaN | Medium | 366 of 2,557 expected days | **Not fixable by cleaning** — flagged for Milestone 3 (Feature Engineering) to handle via explicit reindexing before building lag/rolling features |
| Pollutant columns are exact linear transforms of AQI (`PM2.5 = 0.55 × AQI`, r = 1.00 for all pollutants) | **High (methodological)** | All 6 pollutant columns | Documented in `DATASET_SOURCE.md`; **pollutant columns excluded from model input features** in all future milestones (data-leakage risk) |

## 3. Dataset characteristics (post-cleaning)

- **Shape:** 2,191 rows × 9 columns (`data/processed/delhi_aqi_cleaned.csv`)
- **Date range:** 2018-01-01 to 2024-12-31 (single city: Delhi)
- **AQI range:** 41–494 (full severity spectrum represented)
- **AQI mean / median:** ~208 / ~193 ("Unhealthy" per `config.constants.AQI_CATEGORIES`)
- **AQI distribution:** right-skewed (skew > 0) — see Chart 1
- **Strongest signal found:** seasonal (`Month`/`Season`) — winter AQI roughly double monsoon AQI (Charts 11, 13)
- **Weakest signal found:** day-of-week — averages vary by only a few points (Chart 12)
- **No clear multi-year trend** across 2018–2024 (Charts 3, 14)

## 4. Readiness for next milestone

✅ Dataset is clean, valid, and saved to `data/processed/delhi_aqi_cleaned.csv`.
✅ All quality issues found were either fixed or explicitly documented with
a plan (calendar gaps → Milestone 3; pollutant collinearity → excluded from
modeling features).
✅ EDA (`03_exploratory_data_analysis.ipynb`) completed: 18 distinct charts
across the 10 required types (ML-EDA-002), each with a written
interpretation — histogram, line chart, box plot, correlation heatmap,
scatter plot, monthly/weekly/seasonal/yearly trends, AQI distribution, and
6 individual pollutant distributions.

**MS-002 Definition of Done:** clean dataset ✅ · EDA documented ✅ · quality
report completed ✅ (this document).
