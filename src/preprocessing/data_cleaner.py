"""
Dataset cleaning for the AQI Forecast & Environmental Analytics Platform.
"""

from dataclasses import dataclass
from typing import Optional, Sequence

import numpy as np
import pandas as pd

from src.utils.logger import get_logger

logger = get_logger(__name__)

APPROVED_MISSING_VALUE_STRATEGIES = (
    "drop_rows", "mean", "median", "mode", "forward_fill", "backward_fill",
)


def handle_missing_values(df: pd.DataFrame, strategy: str = "median", columns: Optional[Sequence[str]] = None) -> tuple:
    if strategy not in APPROVED_MISSING_VALUE_STRATEGIES:
        raise ValueError(
            f"Unknown missing-value strategy '{strategy}'. "
            f"Approved strategies: {APPROVED_MISSING_VALUE_STRATEGIES}"
        )

    cleaned = df.copy()
    target_columns = list(columns) if columns is not None else list(cleaned.select_dtypes(include="number").columns)
    report = {}
    rows_before = len(cleaned)

    if strategy == "drop_rows":
        affected = int(cleaned[target_columns].isna().any(axis=1).sum())
        cleaned = cleaned.dropna(subset=target_columns).reset_index(drop=True)
        report["rows_dropped"] = affected
    else:
        for col in target_columns:
            n_missing = int(cleaned[col].isna().sum())
            if n_missing == 0:
                continue
            if strategy == "mean":
                cleaned[col] = cleaned[col].fillna(cleaned[col].mean())
            elif strategy == "median":
                cleaned[col] = cleaned[col].fillna(cleaned[col].median())
            elif strategy == "mode":
                mode_values = cleaned[col].mode(dropna=True)
                fill_value = mode_values.iloc[0] if not mode_values.empty else np.nan
                cleaned[col] = cleaned[col].fillna(fill_value)
            elif strategy == "forward_fill":
                cleaned[col] = cleaned[col].ffill()
            elif strategy == "backward_fill":
                cleaned[col] = cleaned[col].bfill()
            report[col] = n_missing

    logger.info("handle_missing_values(strategy=%s): %d rows before, %d after. Report: %s", strategy, rows_before, len(cleaned), report)
    return cleaned, report


def remove_duplicate_rows(df: pd.DataFrame, subset: Optional[Sequence[str]] = None) -> tuple:
    n_before = len(df)
    cleaned = df.drop_duplicates(subset=subset, keep="first").reset_index(drop=True)
    n_removed = n_before - len(cleaned)
    logger.info("remove_duplicate_rows: removed %d duplicate row(s).", n_removed)
    return cleaned, n_removed


@dataclass
class OutlierResult:
    column: str
    method: str
    count: int
    indices: list
    lower_bound: float
    upper_bound: float


def detect_outliers_iqr(df: pd.DataFrame, columns: Sequence[str], multiplier: float = 1.5) -> dict:
    results = {}
    for col in columns:
        series = df[col].dropna()
        q1, q3 = series.quantile(0.25), series.quantile(0.75)
        iqr = q3 - q1
        lower = q1 - multiplier * iqr
        upper = q3 + multiplier * iqr
        mask = (df[col] < lower) | (df[col] > upper)
        results[col] = OutlierResult(col, "IQR", int(mask.sum()), df.index[mask].tolist(), float(lower), float(upper))
    logger.info("detect_outliers_iqr: %s", {c: r.count for c, r in results.items()})
    return results


def detect_outliers_zscore(df: pd.DataFrame, columns: Sequence[str], threshold: float = 3.0) -> dict:
    results = {}
    for col in columns:
        series = df[col]
        mean, std = series.mean(), series.std()
        if not std or pd.isna(std):
            z_scores = pd.Series(0.0, index=series.index)
        else:
            z_scores = (series - mean) / std
        mask = z_scores.abs() > threshold
        lower = float(mean - threshold * std) if std else float("nan")
        upper = float(mean + threshold * std) if std else float("nan")
        results[col] = OutlierResult(col, "Z-score", int(mask.sum()), df.index[mask].tolist(), lower, upper)
    logger.info("detect_outliers_zscore: %s", {c: r.count for c, r in results.items()})
    return results
