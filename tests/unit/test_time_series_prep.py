"""Unit tests for src.feature_engineering.time_series_prep (ML-TS-001/002)."""

import pandas as pd
import pytest

from src.feature_engineering.time_series_prep import (
    chronological_train_val_test_split,
    reindex_to_daily_calendar,
)


@pytest.fixture
def gapped_df():
    """
    10 real days, then a 5-day gap, then 5 more real days -- a small analog
    of the real dataset's 2022 gap, built by hand so exact behavior is
    verifiable.
    """
    early = pd.date_range("2023-01-01", periods=10, freq="D")
    late = pd.date_range("2023-01-21", periods=5, freq="D")  # gap: Jan 11-20
    dates = list(early) + list(late)
    return pd.DataFrame({"Date": dates, "AQI": range(100, 100 + len(dates))})


def test_reindex_fills_the_correct_number_of_gap_days(gapped_df):
    out = reindex_to_daily_calendar(gapped_df)
    assert len(out) == 25  # Jan 1 to Jan 25 inclusive = 25 days
    assert (~out["IsOriginalRecord"]).sum() == 10  # Jan 11-20 gap = 10 days


def test_reindex_marks_real_vs_gap_rows_correctly(gapped_df):
    out = reindex_to_daily_calendar(gapped_df)
    real_dates = set(gapped_df["Date"])
    for _, row in out.iterrows():
        expected = row["Date"] in real_dates
        assert row["IsOriginalRecord"] == expected


def test_reindex_gap_rows_have_nan_aqi(gapped_df):
    out = reindex_to_daily_calendar(gapped_df)
    gap_rows = out[~out["IsOriginalRecord"]]
    assert gap_rows["AQI"].isna().all()


def test_reindex_preserves_real_values_unchanged(gapped_df):
    out = reindex_to_daily_calendar(gapped_df)
    merged = gapped_df.merge(out, on="Date", suffixes=("_orig", "_reindexed"))
    assert (merged["AQI_orig"] == merged["AQI_reindexed"]).all()


def test_reindex_output_is_continuous_daily(gapped_df):
    out = reindex_to_daily_calendar(gapped_df)
    diffs = out["Date"].diff().dropna().unique()
    assert len(diffs) == 1
    assert diffs[0] == pd.Timedelta(days=1)


# --- chronological_train_val_test_split ---

@pytest.fixture
def ordered_df():
    dates = pd.date_range("2023-01-01", periods=100, freq="D")
    return pd.DataFrame({"Date": dates, "AQI": range(100)})


def test_split_ratios_produce_expected_sizes(ordered_df):
    train, val, test = chronological_train_val_test_split(ordered_df, train_ratio=0.7, val_ratio=0.15, test_ratio=0.15)
    assert len(train) == 70
    assert len(val) == 15
    assert len(test) == 15


def test_split_preserves_chronological_order_with_no_overlap(ordered_df):
    train, val, test = chronological_train_val_test_split(ordered_df)
    assert train["Date"].max() < val["Date"].min()
    assert val["Date"].max() < test["Date"].min()


def test_split_covers_every_row_exactly_once(ordered_df):
    train, val, test = chronological_train_val_test_split(ordered_df)
    assert len(train) + len(val) + len(test) == len(ordered_df)
    combined = pd.concat([train, val, test])
    assert set(combined["AQI"]) == set(ordered_df["AQI"])


def test_split_rejects_ratios_not_summing_to_one(ordered_df):
    with pytest.raises(ValueError):
        chronological_train_val_test_split(ordered_df, train_ratio=0.5, val_ratio=0.3, test_ratio=0.3)
