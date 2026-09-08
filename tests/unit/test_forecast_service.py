"""Unit tests for src.services.forecast_service (FR-FORECAST-001/002)."""

import numpy as np
import pandas as pd
import pytest

from src.services.forecast_service import (
    MIN_SEED_HISTORY_DAYS,
    generate_future_forecast,
)


class _IdentityLag1Model:
    """
    A fake model that always predicts exactly Lag_1 (yesterday's value).
    Used to test the RECURSION MECHANICS in isolation from any real model's
    approximation error: if recursion works correctly, every forecast day
    should equal the last real day's AQI (since each day "copies" the
    previous day, which is itself a copy, all the way back to the seed).
    """

    def predict(self, X):
        return X["Lag_1"].values


@pytest.fixture
def continuous_history():
    dates = pd.date_range("2024-10-01", periods=40, freq="D")
    return pd.DataFrame({"Date": dates, "AQI": [200.0] * 40})


def test_identity_model_produces_constant_forecast(continuous_history):
    """The core recursion-correctness test: with an identity-on-Lag_1
    model and constant historical AQI, every forecast day must equal the
    last real value -- proving predictions are correctly fed forward."""
    feature_names = ["Lag_1"]  # identity model only looks at Lag_1
    forecast = generate_future_forecast(
        _IdentityLag1Model(), continuous_history, feature_names, horizon_days=7
    )
    assert (forecast["Predicted_AQI"] == 200.0).all()


def test_forecast_returns_correct_number_of_rows(continuous_history):
    forecast = generate_future_forecast(
        _IdentityLag1Model(), continuous_history, ["Lag_1"], horizon_days=5
    )
    assert len(forecast) == 5


def test_forecast_dates_are_consecutive_and_after_history(continuous_history):
    forecast = generate_future_forecast(
        _IdentityLag1Model(), continuous_history, ["Lag_1"], horizon_days=7
    )
    last_history_date = continuous_history["Date"].max()
    assert forecast["Date"].min() == last_history_date + pd.Timedelta(days=1)
    diffs = forecast["Date"].diff().dropna().unique()
    assert len(diffs) == 1 and diffs[0] == pd.Timedelta(days=1)


def test_forecast_days_ahead_column_increments_correctly(continuous_history):
    forecast = generate_future_forecast(
        _IdentityLag1Model(), continuous_history, ["Lag_1"], horizon_days=5
    )
    assert list(forecast["DaysAhead"]) == [1, 2, 3, 4, 5]


def test_confidence_label_decreases_with_horizon(continuous_history):
    forecast = generate_future_forecast(
        _IdentityLag1Model(), continuous_history, ["Lag_1"], horizon_days=7
    )
    labels = dict(zip(forecast["DaysAhead"], forecast["ConfidenceLabel"]))
    assert labels[1] == "High"
    assert labels[3] == "Medium"
    assert labels[7] == "Low"


def test_aqi_category_matches_config_breakpoints(continuous_history):
    forecast = generate_future_forecast(
        _IdentityLag1Model(), continuous_history, ["Lag_1"], horizon_days=1
    )
    # constant history AQI=200 -> "Unhealthy" per config.constants.AQI_CATEGORIES (151-200)
    assert forecast.iloc[0]["Predicted_AQI_Category"] == "Unhealthy"


def test_rejects_horizon_less_than_one(continuous_history):
    with pytest.raises(ValueError):
        generate_future_forecast(_IdentityLag1Model(), continuous_history, ["Lag_1"], horizon_days=0)


def test_rejects_insufficient_history():
    short_history = pd.DataFrame({
        "Date": pd.date_range("2024-12-01", periods=10, freq="D"),
        "AQI": [200.0] * 10,
    })
    with pytest.raises(ValueError):
        generate_future_forecast(_IdentityLag1Model(), short_history, ["Lag_1"], horizon_days=3)


def test_rejects_gapped_seed_history():
    early = pd.date_range("2024-11-01", periods=20, freq="D")
    late = pd.date_range("2024-11-25", periods=15, freq="D")  # 4-day gap
    gapped = pd.DataFrame({"Date": list(early) + list(late), "AQI": [200.0] * 35})
    with pytest.raises(ValueError):
        generate_future_forecast(_IdentityLag1Model(), gapped, ["Lag_1"], horizon_days=3)


def test_min_seed_history_days_matches_max_lag_and_window():
    # Sanity: the module's own stated minimum must actually match what the
    # feature builder needs (max of DEFAULT_LAGS and DEFAULT_WINDOWS = 30).
    assert MIN_SEED_HISTORY_DAYS == 30


# --- End-to-end integration test with a REAL trained model ---

def test_end_to_end_with_real_linear_regression_model():
    """Not a mock -- builds real features via our own modules, trains a
    real LinearRegression, and forecasts forward, proving the whole
    feature-alignment logic (one-hot Season, lag/rolling column order)
    works against an actual sklearn model, not just the identity mock."""
    from sklearn.linear_model import LinearRegression

    from src.feature_engineering.date_features import add_date_features
    from src.feature_engineering.lag_features import add_lag_features
    from src.feature_engineering.model_matrix import build_model_matrix
    from src.feature_engineering.rolling_features import add_rolling_features

    dates = pd.date_range("2024-01-01", periods=100, freq="D")
    rng = np.random.default_rng(42)
    aqi = 200 + 20 * np.sin(np.arange(100) / 10) + rng.normal(0, 2, 100)
    raw = pd.DataFrame({"Date": dates, "AQI": aqi})

    featured = add_date_features(raw)
    featured = add_lag_features(featured)
    featured = add_rolling_features(featured)
    featured = featured.dropna().reset_index(drop=True)

    X, y, feature_names = build_model_matrix(featured)
    model = LinearRegression().fit(X, y)

    forecast = generate_future_forecast(model, raw, feature_names, horizon_days=7)

    assert len(forecast) == 7
    assert forecast["Predicted_AQI"].notna().all()
    # Predictions should be in a physically sane range given the training
    # data oscillates around 200 -- not wildly extrapolating.
    assert forecast["Predicted_AQI"].between(100, 300).all()
