"""Regression evaluation metrics (FR-ML-004 / ML-EVAL-001)."""

from dataclasses import dataclass

import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from src.utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class RegressionMetrics:
    mae: float
    mse: float
    rmse: float
    r2: float

    def summary(self) -> str:
        return f"MAE={self.mae:.2f}  MSE={self.mse:.2f}  RMSE={self.rmse:.2f}  R2={self.r2:.4f}"

    def to_dict(self) -> dict:
        return {"MAE": self.mae, "MSE": self.mse, "RMSE": self.rmse, "R2": self.r2}


def calculate_regression_metrics(y_true, y_pred) -> RegressionMetrics:
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    if y_true.shape != y_pred.shape:
        raise ValueError(f"y_true and y_pred must have the same shape, got {y_true.shape} vs {y_pred.shape}")
    if y_true.size == 0:
        raise ValueError("y_true/y_pred must not be empty.")

    mae = float(mean_absolute_error(y_true, y_pred))
    mse = float(mean_squared_error(y_true, y_pred))
    rmse = float(np.sqrt(mse))
    r2 = float(r2_score(y_true, y_pred))

    metrics = RegressionMetrics(mae=mae, mse=mse, rmse=rmse, r2=r2)
    logger.info("calculate_regression_metrics: %s", metrics.summary())
    return metrics
