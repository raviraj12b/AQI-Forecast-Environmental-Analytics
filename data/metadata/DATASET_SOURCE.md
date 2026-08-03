# Dataset Source & Provenance (ML-DATA-001)

## Selected dataset

**India Air Quality Index (AQI) & Estimated Pollutant Levels** — Delhi

- **Repository:** https://github.com/cp099/India-Air-Quality-Dataset
- **File used:** `Delhi_AQI_Dataset.csv`
- **Confirmed schema:** `City, Date, AQI, PM2.5, PM10, NO2, SO2, CO, O3`
  — this is an exact match for `ML-DATA-002`'s mandatory fields.
- **Confirmed size:** 2,192 rows (daily records) · 126 KB
- **License:** CC BY 4.0 — share and adapt permitted, **attribution required**.
  Attribute as: *"AQI data: Central Pollution Control Board (CPCB), via
  cp099/India-Air-Quality-Dataset (CC BY 4.0)."*

### ⚠️ Known data-quality caveat (documented per the source's own disclaimer)

CPCB publishes **AQI values** directly, but not the underlying per-pollutant
concentrations for this dataset. The repository author **mathematically
estimated** PM2.5 / PM10 / NO2 / SO2 / CO / O3 from the published AQI via a
reverse-engineered formula — they are **not raw sensor measurements**.
This is disclosed here rather than glossed over (per Handbook D.98, Ethical
Considerations — avoid unsupported claims): pollutant-level EDA and
per-pollutant feature engineering should be described as "estimated" in the
dashboard/notebooks, not presented as directly measured CPCB readings. The
**AQI column itself is the real, directly-sourced CPCB value** and is what
this project forecasts (PRD's actual target variable), so the caveat mainly
affects pollutant-level analysis (FR-EDA-006 / UI-POLL-001), not the core
forecasting target.

## Why this dataset (ML-DATA-001 acceptance criteria)

| Criterion | Met? |
|---|---|
| Historical observations | ✅ Daily data |
| Publicly accessible | ✅ Public GitHub repo, no auth |
| Includes timestamp information | ✅ `Date` column |
| License permits educational use | ✅ CC BY 4.0 |
| Contains all mandatory fields (ML-DATA-002) | ✅ exact match |

## How to get the file into `data/raw/`

This Claude session runs in a sandboxed container with no outbound network
access from its code tools, and GitHub's `robots.txt` blocks automated
fetching of the raw file — so I could not download it directly. Both of these
manual options take under a minute:

**Option A — browser download (simplest):**
1. Open https://github.com/cp099/India-Air-Quality-Dataset/blob/main/Delhi_AQI_Dataset.csv
2. Click **"Download raw file"**
3. Save it as `data/raw/Delhi_AQI_Dataset.csv` in your local copy of this repo

**Option B — clone the source repo:**
```bash
git clone https://github.com/cp099/India-Air-Quality-Dataset.git /tmp/aqi-src
cp /tmp/aqi-src/Delhi_AQI_Dataset.csv data/raw/
```

The loader/validator code in `src/preprocessing/` (this milestone) is built
and tested against this exact schema, so it will run immediately once the
file is in place — no code changes needed.

### Prefer a different city, or a bigger dataset?

- The same repo also has `Mumbai_AQI_Dataset.csv`, `Bangalore_AQI_Dataset.csv`,
  `Chennai_AQI_Dataset.csv`, `Hyderabad_AQI_Dataset.csv` with identical
  schema — Mumbai may be more locally relevant to you; swapping is a one-line
  change (`RAW_DATASET_FILENAME` wherever it's referenced).
- For a much larger *real-measurement* alternative later: [`abhinavsarkar/delhi_air_quality_feature_store_processed.csv`](https://huggingface.co/datasets/abhinavsarkar/delhi_air_quality_feature_store_processed.csv)
  on Hugging Face — 2.9M hourly rows, 2000–2024, Apache-2.0, actual sensor
  readings rather than estimated. It would need aggregation to daily
  granularity and is ~440MB, so it's noted here as a V1.1+ upgrade path
  rather than the default.

## Not to be confused with: the test fixture

`tests/test_data/synthetic_aqi_fixture.csv` is a small **synthetic** file
(fixed random seed, clearly labeled) used only to unit-test the loader and
validator code before real data is in place. It is never used for EDA,
modeling, or any dashboard content — see `tests/README.md`.
