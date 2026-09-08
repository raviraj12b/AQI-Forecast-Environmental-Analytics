# Changelog

All notable changes to the AQI Forecast & Environmental Analytics Platform
are documented in this file.

## [Unreleased]

### Added (Milestone 5, Part A — Dashboard Services Layer)
- `src/services/forecast_service.py` (FR-FORECAST-001/002): **recursive
  multi-day forecasting engine** — predicts real future dates beyond the
  dataset's last known date (2024-12-31), by feeding each day's own
  prediction forward as the next day's `Lag_1`/rolling inputs. This was
  explicitly flagged as missing at the end of Milestone 4.
  - Rejects non-continuous seed history (reuses the same gap-safety
    guarantee as `lag_features.py`/`rolling_features.py`).
  - Includes an honestly-labeled (not statistical) confidence heuristic
    that decreases with forecast horizon, since recursive forecasts
    compound uncertainty.
  - Verified against a real trained model + real data: forecasts Jan 2025
    as "Very Unhealthy" (240-278 AQI), consistent with the strong winter
    seasonality found in EDA.
- `src/services/health_service.py` (UI-HEALTH-001): health guidance for
  all 6 AQI categories (description, health risk, outdoor recommendation,
  safety advice), with an explicit non-medical-advice disclaimer.
- `src/services/data_service.py`: dashboard-facing data/model loading
  (thin wrappers over already-tested modules — no new business logic, no
  Streamlit dependency, independently testable).
- `src/services/report_service.py` (FR-REPORT-001/002): CSV export
  (always available) and PDF export via `reportlab` (confirmed available;
  raises a clear error if missing rather than an opaque traceback).
- 49 new unit tests across the 4 new services, including a dedicated
  identity-model test proving the forecast recursion mechanics are
  correct in isolation from any real model's prediction error.

### Known limitation (documented, not hidden)
- **Streamlit itself is not installed in this development sandbox** (no
  outbound network to `pip install`), so the actual dashboard UI pages
  (Milestone 5, Part B) cannot be execute-tested here the way the
  notebooks were. The services layer above has zero Streamlit dependency
  and is fully tested; UI pages will need local verification once you run
  `pip install -r requirements.txt && streamlit run dashboard/app.py`.
