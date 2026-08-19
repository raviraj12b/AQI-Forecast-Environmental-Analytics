"""
Rolling statistics for the AQI Forecast & Environmental Analytics Platform
(FR-FE-003 / ML-FE-003).
"""

from typing import Sequence

import pandas as pd

from src.feature_engineering.lag_features import _assert_continuous_daily
from src.utils.logger import get_logger

logger = get_logger(__name__)

DEFAULT_WINDOWS = (7, 14, 30)
DEFAULT_STATS = ("mean", "median", "std")


def add_rolling_features(
    df: pd.DataFrame,
    target_column: str = "AQI",
    date_column: str = "Date",
    windows: Sequence[int] = DEFAULT_WINDOWS,
    stats: Sequence[str] = DEFAULT_STATS,
) -> pd.DataFrame:
    """
    Add rolling-window statistics of `target_column` (ML-FE-003).

    For each window size in `windows`, adds `Rolling_<Stat>_<window>` for
    each requested statistic. Rolling windows look strictly at *past* values
    only (`min_periods` requires a full window, no forward-looking data),
    consistent with time-series forecasting requirements.

    Parameters
    ----------
    df : pd.DataFrame
        Must be a continuous daily calendar -- see
        `time_series_prep.reindex_to_daily_calendar`; enforced via the same
        guard as `add_lag_features` since rolling windows have identical
        row-position-vs-calendar-time exposure.
    target_column : str, default "AQI"
    date_column : str, default "Date"
    windows : sequence of int, default (7, 14, 30)
    stats : sequence of str, default ("mean", "median", "std")
        Any of "mean", "median", "std", "min", "max".

    Returns
    -------
    pd.DataFrame
        A NEW DataFrame with the added rolling columns. Rows before a full
        window is available (or within a window of a calendar gap) will be
        NaN, by design -- not filled here.

    Raises
    ------
    ValueError
        If `df` is not a continuous daily calendar, or an unsupported stat
        is requested.
    """
    _assert_continuous_daily(df, date_column)

    supported = {"mean", "median", "std", "min", "max"}
    unsupported = set(stats) - supported
    if unsupported:
        raise ValueError(f"Unsupported rolling stat(s): {unsupported}. Supported: {supported}")

    out = df.sort_values(date_column).reset_index(drop=True).copy()
    added_columns = []
    for window in windows:
        rolling = out[target_column].rolling(window=window, min_periods=window)
        for stat in stats:
            col_name = f"Rolling_{stat.capitalize()}_{window}"
            out[col_name] = getattr(rolling, stat)()
            added_columns.append(col_name)

    logger.info("add_rolling_features: added %d columns: %s", len(added_columns), added_columns)
    return out
