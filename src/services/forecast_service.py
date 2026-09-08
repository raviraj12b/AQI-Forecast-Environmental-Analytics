"""
Forecast generation service for the AQI Forecast & Environmental Analytics
Platform (FR-FORECAST-001/002).

This is the piece explicitly deferred at the end of Milestone 4: predicting
AQI for dates *beyond* the dataset's last known date (2024-12-31), where no
real lag/rolling inputs exist yet.

The core problem: `Lag_1` for tomorrow needs today's AQI, but "today" may
itself be a day this function already predicted. The only way to forecast
more than one day ahead with a lag-feature model is recursively -- predict
day 1, treat that prediction as if it were real to compute day 2's lag
features, and so on. This is standard practice for lag-feature time-series
models, but it has a real, honestly-documented consequence: **uncertainty
compounds with horizon** -- a 7-day-ahead forecast is built partly on the
model's own earlier guesses, not on independent measurements. This module
does not fabricate a false sense of precision about that; see
`ForecastResult.confidence_label`.
"""

from dataclasses import dataclass
from typing import List, Sequence

import pandas as pd

from config.constants import AQI_CATEGORIES
from src.feature_engineering.date_features import _month_to_season
from src.feature_engineering.lag_features import DEFAULT_LAGS
from src.feature_engineering.rolling_features import DEFAULT_STATS, DEFAULT_WINDOWS
from src.feature_engineering.time_series_prep import reindex_to_daily_calendar
from src.utils.logger import get_logger

logger = get_logger(__name__)

MIN_SEED_HISTORY_DAYS = max(max(DEFAULT_LAGS), max(DEFAULT_WINDOWS))  # 30


def _categorize_aqi(aqi: float) -> str:
    for cat in AQI_CATEGORIES:
        if cat["min"] <= aqi <= cat["max"]:
            return cat["label"]
    return "Beyond scale"


def _confidence_label(days_ahead: int) -> str:
    """
    A simple, honestly-labeled heuristic (not a statistical confidence
    interval -- FR-FORECAST-002 marks confidence score as optional, and a
    real prediction interval is out of scope here). Recursive forecasts
    compound uncertainty with horizon, so this at least prevents the
    dashboard from presenting day-7 with the same implied confidence as
    day-1.
    """
    if days_ahead <= 1:
        return "High"
    if days_ahead <= 3:
        return "Medium"
    return "Low"


def _build_date_features_row(date: pd.Timestamp) -> dict:
    return {
        "Month": date.month,
        "Quarter": date.quarter,
        "Week": int(date.isocalendar().week),
        "Day": date.day,
        "DayOfWeek": date.dayofweek,
        "IsWeekend": date.dayofweek in (5, 6),
        "DayOfYear": date.dayofyear,
        "Season": _month_to_season(date.month),
    }


def _build_feature_row(
    date: pd.Timestamp, working_series: pd.Series, feature_names: Sequence[str]
) -> pd.DataFrame:
    date_feats = _build_date_features_row(date)
    season = date_feats.pop("Season")

    row = dict(date_feats)
    for lag in DEFAULT_LAGS:
        row[f"Lag_{lag}"] = working_series.loc[date - pd.Timedelta(days=lag)]
    for window in DEFAULT_WINDOWS:
        window_values = working_series.loc[
            date - pd.Timedelta(days=window) : date - pd.Timedelta(days=1)
        ]
        for stat in DEFAULT_STATS:
            row[f"Rolling_{stat.capitalize()}_{window}"] = getattr(window_values, stat)()

    # One-hot Season, matching training's pd.get_dummies(drop_first=True) encoding
    for name in feature_names:
        if name.startswith("Season_"):
            row[name] = 1 if name == f"Season_{season}" else 0

    aligned = {name: row[name] for name in feature_names}
    return pd.DataFrame([aligned])


@dataclass
class ForecastDay:
    date: pd.Timestamp
    predicted_aqi: float
    predicted_category: str
    days_ahead: int
    confidence_label: str


def generate_future_forecast(
    model,
    historical_df: pd.DataFrame,
    feature_names: Sequence[str],
    horizon_days: int = 7,
    target_column: str = "AQI",
    date_column: str = "Date",
) -> pd.DataFrame:
    """
    Recursively forecast `horizon_days` days beyond the last date in
    `historical_df` (FR-FORECAST-001: supports next-day / next-week /
    arbitrary horizon by varying `horizon_days`).

    Parameters
    ----------
    model : a fitted scikit-learn estimator (trained on `feature_names`, in
        that exact column order -- e.g. the model loaded from
        `models/trained/`).
    historical_df : pd.DataFrame
        Real historical data, must include at least the last
        `MIN_SEED_HISTORY_DAYS` (30) CONSECUTIVE calendar days -- checked
        and enforced, not assumed. Only `date_column` and `target_column`
        are used from it.
    feature_names : sequence of str
        Must exactly match the column order the model was trained on
        (`build_model_matrix`'s third return value / the model's saved
        metadata `feature_names`).
    horizon_days : int, default 7
    target_column : str, default "AQI"
    date_column : str, default "Date"

    Returns
    -------
    pd.DataFrame
        Columns: Date, Predicted_AQI, Predicted_AQI_Category, DaysAhead,
        ConfidenceLabel. One row per forecast day, in chronological order.

    Raises
    ------
    ValueError
        If fewer than `MIN_SEED_HISTORY_DAYS` consecutive days of real
        history are available, or `horizon_days` < 1.
    """
    if horizon_days < 1:
        raise ValueError(f"horizon_days must be >= 1, got {horizon_days}")

    seed = historical_df[[date_column, target_column]].sort_values(date_column).tail(
        MIN_SEED_HISTORY_DAYS
    )
    if len(seed) < MIN_SEED_HISTORY_DAYS:
        raise ValueError(
            f"Need at least {MIN_SEED_HISTORY_DAYS} days of history to seed "
            f"lag/rolling features, got {len(seed)}."
        )

    diffs = seed[date_column].diff().dropna().unique()
    if len(diffs) != 1 or diffs[0] != pd.Timedelta(days=1):
        raise ValueError(
            "The last MIN_SEED_HISTORY_DAYS of historical_df must be a "
            "continuous daily calendar (no gaps) -- lag/rolling features "
            "would otherwise silently reach across a gap. See "
            "time_series_prep.reindex_to_daily_calendar."
        )

    working_series = seed.set_index(date_column)[target_column].copy()
    last_real_date = working_series.index.max()

    results: List[ForecastDay] = []
    for day_offset in range(1, horizon_days + 1):
        next_date = last_real_date + pd.Timedelta(days=day_offset)
        X_next = _build_feature_row(next_date, working_series, feature_names)
        predicted_aqi = float(model.predict(X_next)[0])

        working_series.loc[next_date] = predicted_aqi  # feed forward for next iteration

        results.append(
            ForecastDay(
                date=next_date,
                predicted_aqi=round(predicted_aqi, 1),
                predicted_category=_categorize_aqi(predicted_aqi),
                days_ahead=day_offset,
                confidence_label=_confidence_label(day_offset),
            )
        )

    forecast_df = pd.DataFrame([r.__dict__ for r in results]).rename(
        columns={
            "date": "Date",
            "predicted_aqi": "Predicted_AQI",
            "predicted_category": "Predicted_AQI_Category",
            "days_ahead": "DaysAhead",
            "confidence_label": "ConfidenceLabel",
        }
    )
    logger.info(
        "generate_future_forecast: %d-day forecast from %s to %s.",
        horizon_days, forecast_df["Date"].min().date(), forecast_df["Date"].max().date(),
    )
    return forecast_df
