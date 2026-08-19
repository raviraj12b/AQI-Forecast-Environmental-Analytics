# Changelog

All notable changes to the AQI Forecast & Environmental Analytics Platform
are documented in this file.

## [Unreleased]

### Added (Milestone 3 — Feature Engineering)
- `src/feature_engineering/date_features.py` (ML-FE-001): Year, Month,
  Quarter, Week, Day, DayOfWeek, IsWeekend, DayOfYear, Season.
- `src/feature_engineering/time_series_prep.py` (ML-TS-001/002):
  `reindex_to_daily_calendar()` and `chronological_train_val_test_split()`.
- `src/feature_engineering/lag_features.py` (ML-FE-002): Lag_1/3/7/14/30,
  with a guard that rejects non-continuous-calendar input rather than
  silently computing wrong values across a gap.
- `src/feature_engineering/rolling_features.py` (ML-FE-003): rolling
  mean/median/std over 7/14/30-day windows, same continuity guard.
- `src/feature_engineering/scaling.py` (ML-FE-004): StandardScaler/
  MinMaxScaler/RobustScaler support — implemented but not auto-applied
  (Handbook policy: scaling is a per-model Milestone 4 decision).
- 35 unit tests across the 5 new modules, including a dedicated test
  proving the gap-guard prevents lag values from crossing the 2022 gap.
- `notebooks/04_feature_engineering.ipynb` — real, executed pipeline on
  the actual dataset producing `delhi_aqi_features.csv`, `train.csv`,
  `val.csv`, `test.csv`.
- `data/metadata/FEATURE_DOCUMENTATION.md` — MS-003 deliverable, including
  an explicit Group A (safe for modeling) / Group B (exclude — leakage
  risk) column split.

### Key finding
- The 366 "missing days" found in EDA are not scattered — it's **all of
  2022 missing** (365 consecutive days) plus one isolated day. Naive
  `.shift()`/`.rolling()` on row-ordered data would have silently reached
  back into December 2021 for early-2023 rows. Fixed by reindexing to a
  continuous daily calendar before computing any lag/rolling feature.
