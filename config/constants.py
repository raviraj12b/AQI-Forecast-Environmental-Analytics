"""
Global constants for the AQI Forecast & Environmental Analytics Platform.

Centralizing constants here avoids magic numbers scattered throughout the
codebase, per Master Development Handbook Section 8.13
(Constants & Configuration).
"""

# Reproducibility (ML-MODEL training standard, Handbook Section 6.10 / D.42)
DEFAULT_RANDOM_SEED = 42

# Forecasting (FR-FORECAST-001 / ML-FOR-001)
DEFAULT_FORECAST_HORIZON_DAYS = 7
SUPPORTED_FORECAST_HORIZONS = ("next_day", "next_week", "next_month")

# Chronological data splitting (ML-TS-002 — no random shuffling for
# time-series data)
TRAIN_SPLIT_RATIO = 0.70
VALIDATION_SPLIT_RATIO = 0.15
TEST_SPLIT_RATIO = 0.15

# Mandatory pollutant columns (ML-DATA-002)
REQUIRED_POLLUTANT_COLUMNS = ("PM2.5", "PM10", "NO2", "SO2", "CO", "O3")

# Mandatory dataset columns (ML-DATA-002)
REQUIRED_DATASET_COLUMNS = ("Date", "AQI") + REQUIRED_POLLUTANT_COLUMNS

# AQI category breakpoints, used by the Health Recommendations page
# (UI-HEALTH-001). Each entry is inclusive of `min` and `max`.
AQI_CATEGORIES = (
    {"label": "Good", "min": 0, "max": 50},
    {"label": "Moderate", "min": 51, "max": 100},
    {"label": "Unhealthy for Sensitive Groups", "min": 101, "max": 150},
    {"label": "Unhealthy", "min": 151, "max": 200},
    {"label": "Very Unhealthy", "min": 201, "max": 300},
    {"label": "Hazardous", "min": 301, "max": 500},
)

# Mandatory evaluation metrics (ML-EVAL-001)
EVALUATION_METRICS = ("MAE", "MSE", "RMSE", "R2")
