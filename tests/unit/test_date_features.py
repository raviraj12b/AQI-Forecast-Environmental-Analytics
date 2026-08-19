"""Unit tests for src.feature_engineering.date_features (FR-FE-001)."""

import pandas as pd
import pytest

from src.feature_engineering.date_features import add_date_features


@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "Date": pd.to_datetime(["2023-01-02", "2023-07-15", "2023-12-25"]),  # Mon, Sat, Mon
        "AQI": [200, 80, 300],
    })


def test_add_date_features_adds_expected_columns(sample_df):
    out = add_date_features(sample_df)
    expected = {"Year", "Month", "Quarter", "Week", "Day", "DayOfWeek",
                "IsWeekend", "DayOfYear", "Season"}
    assert expected.issubset(out.columns)


def test_add_date_features_values_correct(sample_df):
    out = add_date_features(sample_df)
    assert out.loc[0, "Year"] == 2023
    assert out.loc[0, "Month"] == 1
    assert out.loc[0, "DayOfWeek"] == 0  # Monday
    assert out.loc[1, "DayOfWeek"] == 5  # Saturday
    assert out.loc[0, "IsWeekend"] == False
    assert out.loc[1, "IsWeekend"] == True


def test_add_date_features_season_mapping(sample_df):
    out = add_date_features(sample_df)
    assert out.loc[0, "Season"] == "Winter"    # January
    assert out.loc[1, "Season"] == "Monsoon"   # July
    assert out.loc[2, "Season"] == "Winter"    # December


def test_add_date_features_does_not_mutate_input(sample_df):
    original_columns = list(sample_df.columns)
    add_date_features(sample_df)
    assert list(sample_df.columns) == original_columns


def test_add_date_features_rejects_non_datetime_column():
    bad_df = pd.DataFrame({"Date": ["2023-01-01", "2023-01-02"], "AQI": [100, 200]})
    with pytest.raises(TypeError):
        add_date_features(bad_df)
