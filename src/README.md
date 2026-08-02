# src/

All application/business logic lives here (Handbook Appendix A.4). Dashboard
pages and notebooks call into `src/` — they never contain business logic
themselves.

| Package | Responsibility |
|---|---|
| `preprocessing/` | Dataset loading, validation, cleaning, missing-value/duplicate/outlier handling. |
| `feature_engineering/` | Date features, lag features, rolling statistics, scaling. |
| `models/` | Training, saving, loading trained models. |
| `forecasting/` | Prediction / future-value generation logic. |
| `evaluation/` | Metric calculation (MAE/MSE/RMSE/R²), residual analysis, model comparison. |
| `visualization/` | Reusable chart-building functions (no preprocessing here). |
| `services/` | Workflow orchestration — the layer the dashboard actually calls. |
| `utils/` | Generic, stateless helper functions (no business logic). |
| `pipelines/` | End-to-end training/prediction pipeline orchestration. |

**Import direction:** `dashboard → services → {forecasting, models} → {feature_engineering, preprocessing} → utils`. Reverse imports are not allowed (Handbook Section 5.6 / Appendix A.6).
