# tests/test_data/

Small fixtures used **only** by the automated test suite.

## `synthetic_aqi_fixture.csv`

**This is not real air-quality data.** It's a 61-row synthetic file
(`numpy` `default_rng(42)`, matching `config.constants.DEFAULT_RANDOM_SEED`)
generated purely to exercise `data_loader.py` / `data_validator.py` with the
same column schema as the real dataset (`City, Date, AQI, PM2.5, PM10, NO2,
SO2, CO, O3` — see `data/metadata/DATASET_SOURCE.md`).

It deliberately contains three missing `PM2.5` values and one duplicated row
so the validator's missing-value and duplicate-row detection have something
real to catch in tests. It is never read by any notebook, dashboard page, or
EDA/reporting code — only by `tests/unit/`.
