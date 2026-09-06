# Model Evaluation Report — Delhi AQI Forecasting

**Milestone:** MS-004 (Machine Learning Development) · Produced by `notebooks/05_model_training.ipynb` + `06_model_evaluation.ipynb`

## Models trained

| Model | Type | Tuned? |
|---|---|---|
| Linear Regression | Baseline (mandatory, ML-MODEL-001) | No |
| Random Forest | Mandatory (ML-MODEL-002) | No (default params) |
| Random Forest (tuned) | Mandatory | Yes — GridSearchCV + TimeSeriesSplit(5) |
| Gradient Boosting | Optional (ML-MODEL-003) | No |

## Test-set results (final, evaluated once, after all tuning was finished on train/val)

| Model | MAE | MSE | RMSE | R² |
|---|---|---|---|---|
| **Linear Regression** | **26.06** | 1204.55 | 34.71 | **0.8784** |
| Random Forest (tuned) | 26.25 | 1207.58 | 34.75 | 0.8781 |
| Random Forest (default) | 27.00 | 1308.76 | 36.18 | 0.8679 |
| Gradient Boosting | 27.98 | 1480.89 | 38.48 | 0.8505 |

**Selected production model: Linear Regression.** This was not the expected
outcome going in — but it's the honest result on this feature set,
consistent between validation (05) and test (06).

## Methodology notes

- **No data leakage:** pollutant columns and `Year` excluded from every
  model's input features — see `FEATURE_DOCUMENTATION.md`.
- **No temporal leakage in tuning:** hyperparameter search used
  `TimeSeriesSplit`, never shuffled K-Fold.
- **No leakage in model selection:** the test set was touched exactly once.
- **Chronological split preserved throughout.**

## Why the simplest model won

The dominant predictive signal is short-horizon AQI autocorrelation —
`Lag_1`, `Lag_3`, and the 7-day rolling statistics. Day-to-day AQI change
is largely smooth and close to linear in its own recent history, which is
exactly the regime where Linear Regression is competitive with tree
ensembles. A legitimate, explainable result, not a modeling mistake.

## Visualizations produced (ML-EVAL-002, minimum 4 required — 6 delivered)

1. Model comparison bar chart
2. Actual vs. Predicted scatter
3. Residual plot
4. Prediction error distribution histogram
5. Feature importance (top 10)
6. Predicted vs. Actual over the full test time period

## Outputs

- `models/trained/` — all 4 models saved (`.joblib` + `.metadata.json` sidecar each).
- `outputs/forecasts/test_set_forecast.csv` — Date, Actual_AQI, Predicted_AQI, Predicted_AQI_Category, Model.

## What this is *not* yet

Genuine forward-looking forecasting (beyond 2024-12-31) requires a
recursive forecasting service — Milestone 5's dashboard-facing forecasting
engine, not this evaluation notebook.

## MS-004 Definition of Done

Best model selected ✅ · Metrics documented ✅ · Model saved successfully ✅ · Forecast output generated ✅
