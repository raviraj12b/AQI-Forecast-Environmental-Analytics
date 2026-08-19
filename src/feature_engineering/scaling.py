"""
Feature scaling for the AQI Forecast & Environmental Analytics Platform
(FR-FE-004 / ML-FE-004).

Per Handbook Section 6.7 (Feature Scaling Policy) and D.23: "Scaling shall
never be applied automatically." This module provides the capability;
whether/how to use it is a Milestone 4 decision made per-model (tree-based
models like Random Forest generally don't need it; Linear Regression
typically benefits from StandardScaler). It is deliberately NOT called from
`04_feature_engineering.ipynb`'s main pipeline.
"""

from typing import Sequence, Tuple

import pandas as pd
from sklearn.preprocessing import MinMaxScaler, RobustScaler, StandardScaler

from src.utils.logger import get_logger

logger = get_logger(__name__)

APPROVED_SCALERS = {
    "standard": StandardScaler,
    "minmax": MinMaxScaler,
    "robust": RobustScaler,
}


def scale_features(
    df: pd.DataFrame, columns: Sequence[str], method: str = "standard"
) -> Tuple[pd.DataFrame, object]:
    """
    Scale `columns` in `df` using the specified method.

    Parameters
    ----------
    df : pd.DataFrame
    columns : sequence of str
        Numeric columns to scale.
    method : str, default "standard"
        One of "standard" (StandardScaler -- recommended for Linear
        Regression), "minmax" (MinMaxScaler), or "robust" (RobustScaler --
        recommended when outliers are present; not needed here per the
        EDA finding of zero outliers, but available).

    Returns
    -------
    (pd.DataFrame, scaler)
        A NEW DataFrame with `columns` scaled, and the FITTED scaler object
        -- callers must keep this to inverse-transform predictions or to
        apply the identical transform to validation/test data (never
        re-fit on val/test, which would leak information).

    Raises
    ------
    ValueError
        If `method` is not one of `APPROVED_SCALERS`.
    """
    if method not in APPROVED_SCALERS:
        raise ValueError(
            f"Unknown scaling method '{method}'. Approved: {list(APPROVED_SCALERS)}"
        )

    scaler = APPROVED_SCALERS[method]()
    out = df.copy()
    out[list(columns)] = scaler.fit_transform(out[list(columns)])

    logger.info("scale_features: scaled %d columns using %s.", len(columns), method)
    return out, scaler
