# Changelog

All notable changes to the AQI Forecast & Environmental Analytics Platform
are documented in this file.

## [Unreleased]

### Added (Milestone 5, Part B — Dashboard UI, checkpoint 1 of 2)
- `.streamlit/config.toml` — "Clear Sky" base theme (bright, blue accent;
  deliberately not the cream/terracotta or dark/acid-green AI-dashboard
  defaults).
- `dashboard/styles/theme.py` — Sora/Inter font pairing, the AQI category
  color scale reused functionally throughout (not decoration).
- `dashboard/components/kpi.py`, `aqi_badge.py`, `sidebar.py` — reusable,
  self-contained HTML/CSS components (not dependent on guessing
  Streamlit's internal class names, since this couldn't be visually
  verified with Streamlit installed).
- `dashboard/app.py` — Home page (FR-DASH-001 / UI-HOME-001): hero AQI
  number colored by live category, 4 supporting KPI panels, 90-day trend
  chart, calls `forecast_service`/`health_service`/`data_service` only —
  no business logic in the page itself.
- **New verification technique**, since Streamlit itself isn't installed:
  a mock `streamlit` module (`mock_streamlit.py`, dev-only, not part of
  the delivered project) that stubs UI calls but lets real page logic
  execute — catches integration bugs (wrong service signatures, KeyErrors)
  that pure syntax-checking can't. Found and fixed one real bug in the
  mock itself (context-manager protocol on stub objects) before
  confirming `app.py` runs end-to-end against real data with zero errors.

### Remaining for Milestone 5, Part B (next session)
8 more pages: Dataset Overview, EDA, Pollutant Analysis, Forecast,
Model Performance, Health Recommendations, Reports, About.
