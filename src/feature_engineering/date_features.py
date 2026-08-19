"""
Date feature extraction for the AQI Forecast & Environmental Analytics
Platform (FR-FE-001 / ML-FE-001).
"""

from typing import Union

import pandas as pd

from src.utils.logger import get_logger

logger = get_logger(__name__)


def add_date_features(df: pd.DataFrame, date_column: str = "Date") -> pd.DataFrame:
    """
    Add calendar-derived features from `date_column` (ML-FE-001).

    Adds: Year, Month, Quarter, Week, Day, DayOfWeek (0=Monday), IsWeekend,
    DayOfYear, Season (Winter/Summer/Monsoon/Post-Monsoon, per the seasonal
    pattern confirmed in `03_exploratory_data_analysis.ipynb` -- the
    strongest signal found in EDA).

    Parameters
    ----------
    df : pd.DataFrame
    date_column : str, default "Date"
        Must already be a proper datetime dtype (e.g. via `load_dataset`).

    Returns
    -------
    pd.DataFrame
        A NEW DataFrame (input is never mutated) with the added columns.

    Raises
    ------
    TypeError
        If `date_column` is not a datetime dtype.
    """
    if not pd.api.types.is_datetime64_any_dtype(df[date_column]):
        raise TypeError(
            f"'{date_column}' must be a datetime column. "
            f"Got dtype {df[date_column].dtype}. Parse it first (e.g. via "
            f"data_loader.load_dataset)."
        )

    out = df.copy()
    dt = out[date_column].dt

    out["Year"] = dt.year
    out["Month"] = dt.month
    out["Quarter"] = dt.quarter
    out["Week"] = dt.isocalendar().week.astype(int)
    out["Day"] = dt.day
    out["DayOfWeek"] = dt.dayofweek  # 0=Monday .. 6=Sunday
    out["IsWeekend"] = out["DayOfWeek"].isin([5, 6])
    out["DayOfYear"] = dt.dayofyear
    out["Season"] = out["Month"].map(_month_to_season)

    logger.info("add_date_features: added 9 date-derived columns.")
    return out


def _month_to_season(month: int) -> str:
    """
    Map a calendar month to an Indian seasonal category, matching the
    categorization used in `03_exploratory_data_analysis.ipynb` (Chart 13),
    which found this to be the strongest EDA signal.
    """
    if month in (12, 1, 2):
        return "Winter"
    if month in (3, 4, 5):
        return "Summer"
    if month in (6, 7, 8, 9):
        return "Monsoon"
    return "Post-Monsoon"
