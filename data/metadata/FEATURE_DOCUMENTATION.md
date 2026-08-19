# Feature Documentation — `data/processed/delhi_aqi_features.csv`

**Milestone:** MS-003 (Feature Engineering) · Produced by `notebooks/04_feature_engineering.ipynb`

32 columns, 2,101 rows (2018-01-31 to 2024-12-31, excluding the entire
missing year 2022 and the ~30-day warmup window at the start of the series
and immediately after the 2022 gap — see "Row attrition" below).

## ⚠️ Read this before Milestone 4

Columns are split into two groups. **Using a Group B column as a model
input feature to predict AQI is data leakage** — confirmed in EDA
(`03_exploratory_data_analysis.ipynb`) that they are exact linear
transforms of AQI itself (e.g. `PM2.5 = 0.55 × AQI`, r = 1.00).

### Group A — safe to use as model input features

| Column | Type | Description |
|---|---|---|
| `Year`, `Month`, `Quarter`, `Week`, `Day`, `DayOfYear` | int | Calendar components of `Date`. |
| `DayOfWeek` | int (0–6) | 0 = Monday. Found weak in EDA but kept — let the model decide. |
| `IsWeekend` | bool | `DayOfWeek` in {Saturday, Sunday}. |
| `Season` | category | Winter/Summer/Monsoon/Post-Monsoon. **Strongest signal found in EDA** (Chart 13). |
| `Lag_1`, `Lag_3`, `Lag_7`, `Lag_14`, `Lag_30` | float | AQI value N calendar days earlier — computed on a gap-corrected continuous daily calendar (see "How the 2022 gap was handled" below), never naive row-shift. |
| `Rolling_Mean_7/14/30`, `Rolling_Median_7/14/30`, `Rolling_Std_7/14/30` | float | Rolling statistics of AQI over the trailing N days, `min_periods` = full window (no partial-window values). |

### Group B — reference/display only, EXCLUDE from model input features

| Column | Why excluded |
|---|---|
| `PM2.5`, `PM10`, `NO2`, `SO2`, `CO`, `O3` | Exact linear transforms of `AQI` in this dataset (confirmed, not assumed — see `data/metadata/DATASET_SOURCE.md`). Retained in the file only because they're useful for the dashboard's Pollutant Analysis page (UI-POLL-001), which displays them for context, not for prediction. |
| `City` | Constant ("Delhi") — zero variance, zero predictive value, single-city scope. |

### Target variable
`AQI` (int) — the actual PRD forecasting target (Business Objective BO-002).

## How the 2022 gap was handled

All of 2022 (365 days) is absent from the source data — confirmed a
structural gap, not scattered missing values (EDA Chart 18). Interpolating
across an entire missing year would fabricate data, so instead:

1. The cleaned dataset was reindexed to a continuous daily calendar
   (`time_series_prep.reindex_to_daily_calendar`), inserting NaN
   placeholder rows for the 366 missing days (365 in 2022 + Feb 29, 2020)
   so that row position and calendar time coincide again.
2. Lag and rolling features were computed **on this continuous calendar**
   — `.shift(n)` and `.rolling(window)` now correctly mean "n calendar days
   back", not "n rows back". This was verified directly: the first real row
   after the gap (2023-01-01) has `NaN` `Lag_1`, proving the feature
   doesn't silently reach back into December 2021.
3. The 366 placeholder rows were then dropped (never real observations).
4. Any remaining row with an incomplete lag/rolling feature (start of
   series, or within the 30-day warmup window right after the gap) was
   also dropped.

## Row attrition (fully accounted for)

| Stage | Rows |
|---|---|
| Cleaned dataset (`delhi_aqi_cleaned.csv`) | 2,191 |
| + gap-filler rows (reindexing) | 2,557 |
| − gap-filler rows removed | 2,191 |
| − rows with incomplete lag/rolling features | **2,101** (final) |

429 rows had at least one incomplete lag/rolling value before this final
drop (mostly the ~30-day warmup at the very start of the series, plus a
~30-day warmup immediately following the 2022 gap).

## Files produced

- `data/processed/delhi_aqi_features.csv` — full 2,101-row feature set (reference).
- `data/processed/train.csv` — 1,470 rows, 2018-01-31 to 2023-04-10 (70%).
- `data/processed/val.csv` — 315 rows, 2023-04-11 to 2024-02-19 (15%).
- `data/processed/test.csv` — 316 rows, 2024-02-20 to 2024-12-31 (15%).

Split is purely chronological (ML-TS-002 — no random shuffling), zero
overlap between sets, verified by assertion in the notebook itself.

## Scaling — deliberately not applied here

`src/feature_engineering/scaling.py` provides `scale_features()`
(StandardScaler/MinMaxScaler/RobustScaler), fully implemented and tested,
but **not called** in this pipeline. Per Handbook policy (D.23), scaling is
never applied automatically — it's a Milestone 4 decision made per model
(Random Forest doesn't need it; Linear Regression likely will).
