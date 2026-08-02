# data/

Single source of truth for all project datasets (Handbook Appendix A.3).

| Folder | Purpose |
|---|---|
| `raw/` | Original, unmodified datasets exactly as obtained. Never edited by hand or overwritten by pipeline code. |
| `processed/` | Cleaned, feature-engineered, training-ready datasets. Always reproducible from `raw/`. |
| `interim/` | Temporary intermediate outputs produced while preprocessing runs. |
| `external/` | Third-party or supplementary datasets (e.g. weather data) not from the primary source. |
| `samples/` | Small representative datasets used for tests and demos. |
| `metadata/` | Dataset schemas, source descriptions, and data dictionaries. |

**Rule:** no notebook, script, or dashboard page writes into `raw/`. See ML-DATA-001..005 in the PRD for validation/quality requirements.
