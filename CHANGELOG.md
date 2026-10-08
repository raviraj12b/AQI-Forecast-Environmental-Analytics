# Changelog

All notable changes to the AQI Forecast & Environmental Analytics Platform
are documented in this file.

## [Unreleased]

### Added (Milestone 5, Part B — Dashboard UI, complete)
All 9 required pages (FR-DASH-001) built on the "Clear Sky" theme and
services layer, each verified via `mock_streamlit.py` (real logic
executed, UI calls stubbed) against real data with zero errors:

- `dashboard/app.py` — Home (hero AQI, 4 KPI panels, 90-day trend).
- `dashboard/pages/1_Dataset_Overview.py` — shape, dtypes, validation,
  stats, preview.
- `dashboard/pages/2_Exploratory_Analysis.py` — distribution, trend,
  correlation heatmap (with the collinearity warning surfaced directly in
  the UI, not just docs), seasonality, outlier scatter.
- `dashboard/pages/3_Pollutant_Analysis.py` — per-pollutant trend/
  distribution/monthly average, selector-driven, with the "estimated not
  measured" caveat shown prominently.
- `dashboard/pages/4_Forecast.py` — horizon selector (day/week/custom),
  calls `forecast_service.generate_future_forecast()`, hero prediction +
  chart + table with confidence labels.
- `dashboard/pages/5_Model_Performance.py` — 4-model comparison table,
  feature importance, production model details.
- `dashboard/pages/6_Health_Recommendations.py` — today's guidance,
  AQI-value slider lookup, all 6 categories.
- `dashboard/pages/7_Reports.py` — CSV (forecast, dataset summary) and
  PDF (model performance) export via `report_service`; verified the PDF
  generation logic actually executes and produces a valid file (checked
  `%PDF-` header), not just that the button renders.
- `dashboard/pages/8_About.py` — project/dataset/model overview, known
  limitations stated directly (2022 gap, forecast uncertainty).

### Testing approach note
Two risky, unverifiable Streamlit API calls (`st.line_chart(color=...)`,
`st.bar_chart(horizontal=...)`) were caught during self-review and
removed rather than shipped on faith — the mock harness's permissive
stubs would not have caught a real signature mismatch, so those were
flagged as a blind spot rather than trusted.

## Milestone 5 (Dashboard Development): COMPLETE
Dashboard ✅ · Interactive charts ✅ · Forecast page ✅ · Report download ✅

## Milestone 6 (Testing & QA): COMPLETE (with noted limitations)

### Added
- `tests/integration/test_full_pipeline.py` (3 tests): end-to-end pipeline and production-model reproducibility.
- `tests/functional/test_dashboard_pages.py` (10 tests): renders every dashboard page via Streamlit `AppTest`.
- Regression test for Season one-hot consistency in `tests/unit/test_model_matrix.py`.
- `docs/reports/TEST_REPORT.md`.

### Fixed
- `build_model_matrix()` Season encoding now uses a fixed category list, so columns are identical regardless of which seasons a split contains. No change to the trained model or its 24 features.

### Changed
- Code review pass: removed unused imports, added 17 missing docstrings, fixed whitespace style issues.

### Known issues
- Some lines exceed 120 characters; manual browser testing not yet done (see Test Report).
