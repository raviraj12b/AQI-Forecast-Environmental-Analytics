# Dataset Source & Provenance (ML-DATA-001)

## Selected dataset

**India Air Quality Index (AQI) & Estimated Pollutant Levels** — Delhi

- **Repository:** https://github.com/cp099/India-Air-Quality-Dataset
- **File used:** `Delhi_AQI_Dataset.csv`
- **Confirmed schema:** `City, Date, AQI, PM2.5, PM10, NO2, SO2, CO, O3`
  — exact match for `ML-DATA-002`'s mandatory fields.
- **Confirmed size:** 2,191 rows (daily records), 2018-01-01 to 2024-12-31.
- **License:** CC BY 4.0 — share and adapt permitted, **attribution required**.
  Attribute as: *"AQI data: Central Pollution Control Board (CPCB), via
  cp099/India-Air-Quality-Dataset (CC BY 4.0)."*

### ⚠️ Confirmed data-quality caveat: pollutant columns are derived, not measured

CPCB publishes **AQI values** directly; the repository author
**mathematically estimated** PM2.5/PM10/NO2/SO2/CO/O3 from AQI. This was
disclosed by the source and is now **directly confirmed** by our own
analysis (`notebooks/03_exploratory_data_analysis.ipynb`, Chart 4 and 16):
`PM2.5 = 0.55 × AQI` exactly, for every row, and every pollutant correlates
with AQI at r = 1.00. **Pollutant columns must not be used as model input
features to predict AQI** (Milestone 4) — doing so would be data leakage,
since they are a fixed linear function of the target, not independent
measurements. The AQI column itself is the real, directly-sourced CPCB
value and remains the actual forecasting target.

## Acquisition

Placed at `data/raw/Delhi_AQI_Dataset.csv` — provided directly by the
project owner (uploaded to the development session) rather than
auto-downloaded, since this sandbox has no outbound network access and
GitHub's `robots.txt` blocks automated fetching of the raw file.

## Not to be confused with: the test fixture

`tests/test_data/synthetic_aqi_fixture.csv` is a small **synthetic** file
used only to unit-test the loader/validator/cleaner code. Never used for
EDA, modeling, or dashboard content.
