# Changelog

All notable changes to the AQI Forecast & Environmental Analytics Platform
are documented in this file.

## [Unreleased]

### Added (Milestone 4 — Machine Learning Development)
- `src/feature_engineering/model_matrix.py`: centralized, leakage-safe
  feature selection (Group A only) + Season one-hot encoding.
- `src/evaluation/metrics.py` (ML-EVAL-001): MAE/MSE/RMSE/R² with input
  validation.
- `src/models/model_trainer.py` (ML-MODEL-001..004): Linear Regression
  (mandatory baseline), Random Forest (mandatory), Gradient Boosting
  (optional, zero extra dependencies), + feature importance extraction.
- `src/models/hyperparameter_tuning.py` (ML-OPT-001): GridSearchCV with
  `TimeSeriesSplit` (never shuffled K-Fold, per Handbook D.38).
- `src/models/model_io.py` (ML-REG-001): model save/load with metadata
  sidecar JSON (algorithm, features, metrics, dataset version, timestamp).
- 30 new unit tests across the 4 new/completed modules.
- `notebooks/05_model_training.ipynb`: trains + tunes all 4 models on
  `train.csv`, ranks on `val.csv`, saves all 4 (not just the winner).
- `notebooks/06_model_evaluation.ipynb`: final test-set evaluation
  (touched exactly once), 6 required visualizations (ML-EVAL-002 minimum
  is 4), forecast CSV output (FR-FORECAST-002).
- `data/metadata/MODEL_EVALUATION_REPORT.md` — MS-004 deliverable.
- `models/trained/*.joblib` + metadata — all 4 trained models.
- `outputs/forecasts/test_set_forecast.csv`.

### Key finding
- **Linear Regression outperformed both Random Forest (tuned and
  untuned) and Gradient Boosting** on the held-out test set (MAE 26.06 vs
  26.25/27.00/27.98). Consistent between validation and test — not
  overfitting-driven. Explained by short-horizon AQI autocorrelation being
  the dominant signal, a regime where linear models are competitive.
  Selected as the production model on this evidence.
