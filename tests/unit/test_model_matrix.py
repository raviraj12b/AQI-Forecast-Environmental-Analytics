import pandas as pd
import pytest
from src.feature_engineering.model_matrix import EXCLUDED_LEAKAGE_COLUMNS, build_model_matrix

@pytest.fixture
def featured_df():
    n = 40
    return pd.DataFrame({
        "Date": pd.date_range("2023-01-01", periods=n, freq="D"), "City": ["Delhi"]*n,
        "AQI": range(100,140), "PM2.5":[x*0.55 for x in range(100,140)], "PM10":[x*0.9 for x in range(100,140)],
        "NO2":[x*0.3 for x in range(100,140)], "SO2":[x*0.1 for x in range(100,140)],
        "CO":[x*0.01 for x in range(100,140)], "O3":[x*0.2 for x in range(100,140)],
        "Year":[2023]*n, "Month":[1]*n, "Quarter":[1]*n, "Week":[1]*n, "Day":list(range(1,41)),
        "DayOfWeek":[i%7 for i in range(n)], "IsWeekend":[i%7 in (5,6) for i in range(n)],
        "DayOfYear":list(range(1,41)), "Season":["Winter"]*20+["Summer"]*20,
        "Lag_1":range(99,139), "Lag_3":range(97,137), "Lag_7":range(93,133), "Lag_14":range(86,126), "Lag_30":range(70,110),
        "Rolling_Mean_7":[100.0]*n, "Rolling_Mean_14":[100.0]*n, "Rolling_Mean_30":[100.0]*n,
        "Rolling_Median_7":[100.0]*n, "Rolling_Median_14":[100.0]*n, "Rolling_Median_30":[100.0]*n,
        "Rolling_Std_7":[5.0]*n, "Rolling_Std_14":[5.0]*n, "Rolling_Std_30":[5.0]*n,
    })

def test_build_model_matrix_excludes_leakage_columns(featured_df):
    X, y, names = build_model_matrix(featured_df)
    for col in EXCLUDED_LEAKAGE_COLUMNS:
        assert col not in X.columns and col not in names

def test_build_model_matrix_excludes_year(featured_df):
    X, y, names = build_model_matrix(featured_df)
    assert "Year" not in X.columns

def test_build_model_matrix_excludes_city_and_date(featured_df):
    X, y, names = build_model_matrix(featured_df)
    assert "City" not in X.columns and "Date" not in X.columns

def test_build_model_matrix_one_hot_encodes_season(featured_df):
    X, y, names = build_model_matrix(featured_df)
    assert any(c.startswith("Season_") for c in X.columns)
    assert "Season" not in X.columns

def test_build_model_matrix_y_matches_target(featured_df):
    X, y, names = build_model_matrix(featured_df)
    assert list(y) == list(featured_df["AQI"])

def test_build_model_matrix_raises_on_missing_required_column(featured_df):
    with pytest.raises(KeyError):
        build_model_matrix(featured_df.drop(columns=["Lag_7"]))
