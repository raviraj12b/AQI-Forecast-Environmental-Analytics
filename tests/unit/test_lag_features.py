"""Unit tests for src.feature_engineering.lag_features (FR-FE-002)."""

import numpy as np
import pandas as pd
import pytest

from src.feature_engineering.lag_features import add_lag_features
from src.feature_engineering.time_series_prep import reindex_to_daily_calendar


@pytest.fixture
def continuous_df():
    dates = pd.date_range("2023-01-01", periods=40, freq="D")
    return pd.DataFrame({"Date": dates, "AQI": range(100, 140)})


def test_add_lag_features_adds_expected_columns(continuous_df):
    out = add_lag_features(continuous_df, lags=(1, 7))
    assert "Lag_1" in out.columns
    assert "Lag_7" in out.columns


def test_lag_1_is_previous_days_value(continuous_df):
    out = add_lag_features(continuous_df, lags=(1,))
    # AQI is 100, 101, 102, ... so Lag_1 at row i should equal AQI at row i-1
    assert out.loc[5, "Lag_1"] == out.loc[4, "AQI"]
    assert out.loc[10, "Lag_7"] if "Lag_7" in out.columns else True


def test_lag_7_is_seven_days_back_exactly(continuous_df):
    out = add_lag_features(continuous_df, lags=(7,))
    assert out.loc[10, "Lag_7"] == out.loc[3, "AQI"]


def test_first_n_rows_have_nan_lag(continuous_df):
    out = add_lag_features(continuous_df, lags=(7,))
    assert out.loc[:5, "Lag_7"].isna().all()
    assert out.loc[7:, "Lag_7"].notna().all()


def test_add_lag_features_rejects_gapped_dataframe():
    """The critical test: a gapped dataframe must be rejected, not silently
    produce wrong lag values."""
    early = pd.date_range("2023-01-01", periods=10, freq="D")
    late = pd.date_range("2023-02-01", periods=10, freq="D")  # big gap
    gapped = pd.DataFrame({"Date": list(early) + list(late), "AQI": range(20)})
    with pytest.raises(ValueError):
        add_lag_features(gapped)


def test_add_lag_features_accepts_reindexed_gapped_dataframe():
    """Once reindexed, the same gapped source should work -- and correctly
    produce NaN lags right after the gap, rather than reaching across it."""
    early = pd.date_range("2023-01-01", periods=10, freq="D")
    late = pd.date_range("2023-02-01", periods=10, freq="D")
    gapped = pd.DataFrame({"Date": list(early) + list(late), "AQI": range(20)})

    reindexed = reindex_to_daily_calendar(gapped)
    out = add_lag_features(reindexed, lags=(1,))

    # The first real row after the gap (2023-02-01) must have NaN Lag_1 --
    # NOT the last pre-gap value. This is the exact bug this module prevents.
    first_post_gap_row = out[out["Date"] == pd.Timestamp("2023-02-01")].iloc[0]
    assert pd.isna(first_post_gap_row["Lag_1"])


def test_add_lag_features_does_not_mutate_input(continuous_df):
    original = continuous_df.copy(deep=True)
    add_lag_features(continuous_df, lags=(1, 7))
    pd.testing.assert_frame_equal(continuous_df, original)
