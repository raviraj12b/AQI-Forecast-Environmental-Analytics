"""Unit tests for src.feature_engineering.scaling (FR-FE-004)."""

import numpy as np
import pandas as pd
import pytest

from src.feature_engineering.scaling import scale_features


@pytest.fixture
def sample_df():
    return pd.DataFrame({"A": [1.0, 2.0, 3.0, 4.0, 5.0], "B": [10.0, 20.0, 30.0, 40.0, 50.0]})


def test_scale_features_standard_zero_mean_unit_variance(sample_df):
    out, scaler = scale_features(sample_df, columns=["A", "B"], method="standard")
    assert out["A"].mean() == pytest.approx(0.0, abs=1e-9)
    assert out["A"].std(ddof=0) == pytest.approx(1.0, abs=1e-9)


def test_scale_features_minmax_bounds_zero_one(sample_df):
    out, scaler = scale_features(sample_df, columns=["A", "B"], method="minmax")
    assert out["A"].min() == pytest.approx(0.0)
    assert out["A"].max() == pytest.approx(1.0)


def test_scale_features_returns_fitted_scaler_usable_for_transform(sample_df):
    out, scaler = scale_features(sample_df, columns=["A"], method="standard")
    new_data = pd.DataFrame({"A": [3.0]})
    transformed = scaler.transform(new_data)
    assert transformed.shape == (1, 1)


def test_scale_features_rejects_unknown_method(sample_df):
    with pytest.raises(ValueError):
        scale_features(sample_df, columns=["A"], method="not_a_real_method")


def test_scale_features_does_not_mutate_input(sample_df):
    original = sample_df.copy(deep=True)
    scale_features(sample_df, columns=["A", "B"], method="standard")
    pd.testing.assert_frame_equal(sample_df, original)
