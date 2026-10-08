# Test Report — Milestone 6 (Testing & QA)

**Project:** AQI Forecast & Environmental Analytics Platform
**Date executed:** 2026-10-08 · **Python:** 3.12 · **Runner:** pytest
**Result:** 116 passed, 0 failed (~6 s total)

## 1. Scope and results

| Suite | Location | Tests | Result |
|---|---|---|---|
| Unit | `tests/unit/` | 103 | Pass |
| Integration | `tests/integration/test_full_pipeline.py` | 3 | Pass |
| Functional (dashboard) | `tests/functional/test_dashboard_pages.py` | 10 | Pass |

**Unit** covers loader, validator, date/lag/rolling features, scaling, time-series split, model matrix, models, metrics, data/forecast/health/report services.
**Integration** chains cleaned data -> daily reindex -> features -> model matrix -> training -> metrics -> recursive forecast, and checks the production model forecast is reproducible (NFR-REL-002) with 24 features.
**Functional** renders `app.py` and all 8 pages with Streamlit's `AppTest` and asserts no exceptions.

## 2. Defects found and fixed

| ID | Severity | Description | Fix | Verification |
|---|---|---|---|---|
| D-01 | Medium | `build_model_matrix()` one-hot encoded Season with `get_dummies` on the data present, so a split lacking a season produced different columns and broke prediction. | Fixed category list (`SEASON_CATEGORIES`); same dropped baseline (Monsoon). | New regression test; production model still has the same 24 features and unchanged forecast behaviour (integration test). |

## 3. Code review (Handbook checklist)

- Unused imports removed (6 across `src/`, `dashboard/`, `tests/`).
- Missing docstrings added to 17 public functions/classes in `src/` and `dashboard/components/`.
- PEP 8 whitespace issues auto-fixed in dashboard pages and tests.
- No `TODO`/`FIXME`/`print()` in production code.
- **Remaining (Low, not fixed):** E501 lines over 120 chars in `health_service.py`, `hyperparameter_tuning.py`, `data_cleaner.py`, `theme.py`; E203 in one slice in `forecast_service.py`; E712 in two test assertions. The Handbook recommends 88-100 chars, so the line-length target is **not fully met**.

## 4. Known limitations (not verified)

- `AppTest` checks pages execute without exceptions. It does **not** verify visual layout, responsiveness, keyboard navigation, theme switching, or PDF/CSV downloads through a real browser. Those need manual checks.
- Dashboard load-time targets (NFR-PERF-002, < 3 s) were not formally benchmarked; page script runs took roughly 0.3-1.4 s each in this environment, which is indicative only.
- Integration and functional tests, and 2 unit tests, need `data/processed/*.csv`, which is git-ignored. Regenerate by running notebooks 02 and 04 before testing on a fresh clone.
- Forecast accuracy (R² target > 0.80, SM-001) is documented in `data/metadata/MODEL_EVALUATION_REPORT.md`, not re-evaluated here.

## 5. Sign-off checklist

- [x] Unit / integration / functional suites pass
- [x] Regression baseline stable after changes
- [x] Defect D-01 fixed with a regression test
- [ ] Manual browser check (navigation, themes, downloads)
- [ ] Line-length cleanup to Handbook target
