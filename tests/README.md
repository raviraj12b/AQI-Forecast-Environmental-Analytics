# tests/

Automated tests for the platform (Handbook Appendix A.10).

| Folder | Purpose |
|---|---|
| `unit/` | Tests for individual functions (preprocessing, feature engineering, metrics). |
| `integration/` | Tests verifying interaction between modules (e.g. preprocessing → feature engineering). |
| `functional/` | End-to-end user-facing workflow tests (dashboard loads, forecast runs). |
| `regression/` | Confirms existing functionality isn't broken by new changes. |
| `test_data/` | Small representative datasets used only by the test suite. |
| `fixtures/` | Reusable pytest fixtures/test objects. |

Run with `pytest` from the project root. `conftest.py` adds the project root
to `sys.path` so tests can import `config` and `src` directly.
