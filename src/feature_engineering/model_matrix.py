"""Model matrix construction -- centralizes leakage-safe feature selection."""

from typing import List, Tuple

import pandas as pd

from src.utils.logger import get_logger

logger = get_logger(__name__)

DATE_FEATURE_COLUMNS = ["Month", "Quarter", "Week", "Day", "DayOfWeek", "IsWeekend", "DayOfYear", "Season"]
LAG_FEATURE_COLUMNS = ["Lag_1", "Lag_3", "Lag_7", "Lag_14", "Lag_30"]
ROLLING_FEATURE_COLUMNS = [
    "Rolling_Mean_7", "Rolling_Mean_14", "Rolling_Mean_30",
    "Rolling_Median_7", "Rolling_Median_14", "Rolling_Median_30",
    "Rolling_Std_7", "Rolling_Std_14", "Rolling_Std_30",
]
EXCLUDED_LEAKAGE_COLUMNS = ["PM2.5", "PM10", "NO2", "SO2", "CO", "O3"]
EXCLUDED_OTHER_COLUMNS = ["City", "Year", "Date"]


def build_model_matrix(df: pd.DataFrame, target_column: str = "AQI") -> Tuple[pd.DataFrame, pd.Series, List[str]]:
    required = DATE_FEATURE_COLUMNS + LAG_FEATURE_COLUMNS + ROLLING_FEATURE_COLUMNS
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise KeyError(f"Missing required feature columns: {missing}")

    feature_df = df[required].copy()
    feature_df = pd.get_dummies(feature_df, columns=["Season"], drop_first=True)

    y = df[target_column]
    feature_names = list(feature_df.columns)

    logger.info("build_model_matrix: %d rows, %d features.", len(feature_df), len(feature_names))
    return feature_df, y, feature_names
