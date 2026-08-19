"""
Time-series preparation for the AQI Forecast & Environmental Analytics
Platform (ML-TS-001, ML-TS-002).

The Delhi AQI dataset has a critical structural property, confirmed in EDA
(`03_exploratory_data_analysis.ipynb`, Chart 18) and re-investigated during
feature engineering: it is **not evenly spaced**. All of 2022 (365 days) and
one isolated day (2020-02-29) are simply absent -- not present with a
missing value, but entirely missing rows.

This matters enormously for lag/rolling features. `DataFrame.shift(n)` and
`.rolling(window)` operate on ROW POSITION, not calendar time. On a gapped
dataframe, `shift(7)` for the row dated 2023-01-01 would silently grab the
value from ~2021-12-25 (7 *rows* back) instead of a non-existent 2022-12-25
(7 *days* back) -- the same category of silent corruption as the date-parsing
bug found earlier in this project, just relocated to feature engineering.

`reindex_to_daily_calendar` exists specifically to make row position and
calendar time coincide again before any lag/rolling feature is computed.
"""

from typing import Tuple

import pandas as pd

from src.utils.logger import get_logger

logger = get_logger(__name__)


def reindex_to_daily_calendar(df: pd.DataFrame, date_column: str = "Date") -> pd.DataFrame:
    """
    Reindex `df` to a continuous daily calendar spanning its min/max date.

    Rows for genuinely missing calendar days are inserted with NaN in every
    other column. An `IsOriginalRecord` boolean column is added so it is
    always possible to tell real data apart from gap-filler rows -- nothing
    is silently fabricated.

    Parameters
    ----------
    df : pd.DataFrame
    date_column : str, default "Date"

    Returns
    -------
    pd.DataFrame
        Reindexed, chronologically sorted DataFrame with one row per
        calendar day, `IsOriginalRecord` marking which rows were real.
    """
    working = df.sort_values(date_column).reset_index(drop=True).copy()
    full_range = pd.date_range(
        working[date_column].min(), working[date_column].max(), freq="D"
    )

    working = working.set_index(date_column)
    n_before = len(working)
    reindexed = working.reindex(full_range)
    reindexed.index.name = date_column

    reindexed["IsOriginalRecord"] = reindexed.index.isin(working.index)
    n_gap_rows = int((~reindexed["IsOriginalRecord"]).sum())

    logger.info(
        "reindex_to_daily_calendar: %d original rows -> %d calendar rows "
        "(%d gap-filler rows inserted).",
        n_before,
        len(reindexed),
        n_gap_rows,
    )
    if n_gap_rows:
        logger.warning(
            "%d gap-filler rows were inserted with NaN values. These are "
            "NOT real observations -- do not train on them, and be aware "
            "lag/rolling features near a gap will be NaN by design.",
            n_gap_rows,
        )

    return reindexed.reset_index()


def chronological_train_val_test_split(
    df: pd.DataFrame,
    date_column: str = "Date",
    train_ratio: float = 0.70,
    val_ratio: float = 0.15,
    test_ratio: float = 0.15,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Split `df` chronologically into train/validation/test sets (ML-TS-002).

    Random shuffling is never used for time-series data -- splitting is a
    simple chronological cut after sorting by `date_column`, so no future
    information can leak into training (Handbook D.12, Data Leakage
    Detection).

    Parameters
    ----------
    df : pd.DataFrame
    date_column : str, default "Date"
    train_ratio, val_ratio, test_ratio : float
        Must sum to 1.0 (within floating-point tolerance).

    Returns
    -------
    (pd.DataFrame, pd.DataFrame, pd.DataFrame)
        train, validation, test -- each still sorted chronologically, with
        no overlap and no gaps between them.

    Raises
    ------
    ValueError
        If the ratios do not sum to 1.0.
    """
    total = train_ratio + val_ratio + test_ratio
    if abs(total - 1.0) > 1e-6:
        raise ValueError(
            f"train_ratio + val_ratio + test_ratio must sum to 1.0, got {total}"
        )

    working = df.sort_values(date_column).reset_index(drop=True)
    n = len(working)
    train_end = int(n * train_ratio)
    val_end = train_end + int(n * val_ratio)

    train = working.iloc[:train_end]
    val = working.iloc[train_end:val_end]
    test = working.iloc[val_end:]

    logger.info(
        "chronological_train_val_test_split: train=%d (%s to %s), "
        "val=%d (%s to %s), test=%d (%s to %s)",
        len(train), train[date_column].min(), train[date_column].max(),
        len(val), val[date_column].min(), val[date_column].max(),
        len(test), test[date_column].min(), test[date_column].max(),
    )
    return train, val, test
