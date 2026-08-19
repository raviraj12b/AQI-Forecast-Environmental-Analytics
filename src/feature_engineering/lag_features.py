"""
Lag feature creation for the AQI Forecast & Environmental Analytics
Platform (FR-FE-002 / ML-FE-002).
"""

from typing import Sequence

import pandas as pd

from src.utils.logger import get_logger

logger = get_logger(__name__)

DEFAULT_LAGS = (1, 3, 7, 14, 30)


def _assert_continuous_daily(df: pd.DataFrame, date_column: str) -> None:
    """
    Guard against the exact bug class this module exists to prevent:
    computing `.shift()` on a dataframe with calendar gaps, which silently
    reaches back further in *time* than intended. Raises loudly instead of
    producing quietly-wrong lag values.
    """
    diffs = df[date_column].sort_values().diff().dropna().unique()
    if len(diffs) != 1 or diffs[0] != pd.Timedelta(days=1):
        raise ValueError(
            "add_lag_features requires a continuous daily calendar with no "
            "gaps (row position must equal calendar time), otherwise "
            "shift(n) silently means 'n rows back', not 'n days back'. "
            "Call time_series_prep.reindex_to_daily_calendar() first."
        )


def add_lag_features(
    df: pd.DataFrame,
    target_column: str = "AQI",
    date_column: str = "Date",
    lags: Sequence[int] = DEFAULT_LAGS,
) -> pd.DataFrame:
    """
    Add lag features Lag_<n> = target_column shifted n days back (ML-FE-002).

    Parameters
    ----------
    df : pd.DataFrame
        Must be a continuous daily calendar (see module docstring and
        `time_series_prep.reindex_to_daily_calendar`) -- checked and
        enforced, not assumed.
    target_column : str, default "AQI"
    date_column : str, default "Date"
    lags : sequence of int, default (1, 3, 7, 14, 30)

    Returns
    -------
    pd.DataFrame
        A NEW DataFrame (input is never mutated) with one `Lag_<n>` column
        per requested lag. The first `max(lags)` rows (and any rows within
        `max(lags)` days of a calendar gap) will have NaN in some lag
        columns -- this is expected and must be handled by the caller
        (typically by dropping rows before model training), not silently
        filled here.

    Raises
    ------
    ValueError
        If `df` is not a continuous daily calendar.
    """
    _assert_continuous_daily(df, date_column)

    out = df.sort_values(date_column).reset_index(drop=True).copy()
    for lag in lags:
        out[f"Lag_{lag}"] = out[target_column].shift(lag)

    n_incomplete = out[[f"Lag_{lag}" for lag in lags]].isna().any(axis=1).sum()
    logger.info(
        "add_lag_features: added lags %s. %d/%d rows have at least one NaN lag.",
        list(lags), int(n_incomplete), len(out),
    )
    return out
