"""Integration test: raw -> clean -> features -> model -> forecast (Handbook A.10.6)."""

import numpy as np
import pandas as pd
import pytest

from config.paths import RAW_DATA_DIR
from src.evaluation.metrics import calculate_regression_metrics
from src.feature_engineering.date_features import add_date_features
from src.feature_engineering.lag_features import add_lag_features
from src.feature_engineering.model_matrix import build_model_matrix
from src.feature_engineering.rolling_features import add_rolling_features
from src.feature_engineering.time_series_prep import (
    reindex_to_daily_calendar,
)
from src.models.model_trainer import train_model
from src.services.data_service import load_cleaned_dataset, load_production_model
from src.services.forecast_service import generate_future_forecast


@pytest.fixture(scope="module")
def pipeline():
    cleaned = load_cleaned_dataset()
    # Build features on the longest continuous run (the data has a 2022 gap).
    daily = reindex_to_daily_calendar(cleaned)
    featured = add_rolling_features(add_lag_features(add_date_features(daily)))
    featured = featured.dropna().reset_index(drop=True)
    return cleaned, featured


def test_raw_dataset_exists():
    assert any(RAW_DATA_DIR.glob("*.csv"))


def test_features_to_model_to_forecast(pipeline):
    cleaned, featured = pipeline
    X, y, names = build_model_matrix(featured)
    assert not X.isna().any().any()
    split_at = int(len(X) * 0.8)
    model = train_model("linear_regression", X.iloc[:split_at], y.iloc[:split_at])
    preds = model.predict(X.iloc[split_at:])
    metrics = calculate_regression_metrics(y.iloc[split_at:], preds)
    assert all(np.isfinite(list(metrics.to_dict().values())))

    recent = cleaned.sort_values("Date").tail(60)
    out = generate_future_forecast(model, recent, names, horizon_days=3)
    assert len(out) == 3
    assert out.select_dtypes("number").notna().all().all()


def test_production_model_forecast_is_reproducible(pipeline):
    cleaned, _ = pipeline
    model, meta = load_production_model()
    names = meta["feature_names"]
    recent = cleaned.sort_values("Date").tail(60)
    a = generate_future_forecast(model, recent, names, horizon_days=7)
    b = generate_future_forecast(model, recent, names, horizon_days=7)
    pd.testing.assert_frame_equal(a, b)
    assert len(names) == 24
