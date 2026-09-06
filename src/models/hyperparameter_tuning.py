"""Hyperparameter tuning with time-series-aware CV (FR-ML-003 / ML-OPT-001)."""

from typing import Dict, Tuple

from sklearn.model_selection import GridSearchCV, TimeSeriesSplit

from src.utils.logger import get_logger

logger = get_logger(__name__)


def tune_with_grid_search(estimator, param_grid: Dict, X_train, y_train, n_splits: int = 5, scoring: str = "neg_mean_absolute_error") -> Tuple[object, Dict, float]:
    tscv = TimeSeriesSplit(n_splits=n_splits)
    search = GridSearchCV(estimator, param_grid, cv=tscv, scoring=scoring, n_jobs=-1)
    search.fit(X_train, y_train)
    best_score = -search.best_score_ if scoring.startswith("neg_") else search.best_score_
    logger.info("tune_with_grid_search: best_params=%s, best_score=%.3f", search.best_params_, best_score)
    return search.best_estimator_, search.best_params_, best_score
