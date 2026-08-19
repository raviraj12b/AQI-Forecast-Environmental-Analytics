"""Unit tests for src.feature_engineering.rolling_features (FR-FE-003)."""

import numpy as np
import pandas as pd
import pytest

from src.feature_engineering.rolling_features import add_rolling_features


@pytest.fixture
def continuous_df():
    dates = pd.date_range("2023-01-01", periods=40, freq="D")
    return pd.DataFrame({"Date": dates, "AQI": [float(i) for i in range(100, 140)]})


def test_add_rolling_features_adds_expected_columns(continuous_df):
    out = add_rolling_features(continuous_df, windows=(7,), stats=("mean", "std"))
    assert "Rolling_Mean_7" in out.columns
    assert "Rolling_Std_7" in out.columns


def test_rolling_mean_correct_value(continuous_df):
    out = add_rolling_features(continuous_df, windows=(7,), stats=("mean",))
    # Row 10 (0-indexed): mean of AQI rows 4..10 inclusive (7 values)
    expected = continuous_df["AQI"].iloc[4:11].mean()
    assert out.loc[10, "Rolling_Mean_7"] == pytest.approx(expected)


def test_rolling_window_requires_full_window_before_producing_value(continuous_df):
    out = add_rolling_features(continuous_df, windows=(7,), stats=("mean",))
    assert out.loc[:5, "Rolling_Mean_7"].isna().all()  # rows 0-5: fewer than 7 values available
    assert out.loc[6:, "Rolling_Mean_7"].notna().all()


def test_add_rolling_features_rejects_gapped_dataframe():
    early = pd.date_range("2023-01-01", periods=10, freq="D")
    late = pd.date_range("2023-02-01", periods=10, freq="D")
    gapped = pd.DataFrame({"Date": list(early) + list(late), "AQI": range(20)})
    with pytest.raises(ValueError):
        add_rolling_features(gapped)


def test_add_rolling_features_rejects_unsupported_stat(continuous_df):
    with pytest.raises(ValueError):
        add_rolling_features(continuous_df, stats=("not_a_real_stat",))


def test_add_rolling_features_does_not_mutate_input(continuous_df):
    original = continuous_df.copy(deep=True)
    add_rolling_features(continuous_df, windows=(7, 14))
    pd.testing.assert_frame_equal(continuous_df, original)
