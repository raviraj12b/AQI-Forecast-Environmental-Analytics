# dashboard/

Streamlit presentation layer only (Handbook Appendix A.6). No model
training, preprocessing, or business logic may live here — pages call
`src/services/` and render the result.

| Folder | Purpose |
|---|---|
| `pages/` | One file per dashboard page (home, dataset overview, EDA, pollutant analysis, forecast, model performance, health recommendations, reports, about — FR-DASH-001). |
| `components/` | Reusable UI elements (navbar, KPI cards, download buttons). |
| `styles/` | Shared CSS/theme configuration. |
| `assets/` | Dashboard-specific images/icons (distinct from project-level `assets/`). |
| `utils/` | Presentation-only helpers (formatting, layout helpers). |

Entry point `app.py` will be added in Milestone 5 (Dashboard Development).
