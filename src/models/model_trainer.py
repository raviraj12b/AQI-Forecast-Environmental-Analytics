"""Model training (FR-ML-002 / ML-MODEL-001..004)."""

from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import LinearRegression

from config.constants import DEFAULT_RANDOM_SEED
from src.utils.logger import get_logger

logger = get_logger(__name__)

MODEL_REGISTRY = {
    "linear_regression": lambda: LinearRegression(),
    "random_forest": lambda: RandomForestRegressor(n_estimators=200, random_state=DEFAULT_RANDOM_SEED, n_jobs=-1),
    "gradient_boosting": lambda: GradientBoostingRegressor(random_state=DEFAULT_RANDOM_SEED),
}


def train_model(model_name: str, X_train, y_train, **model_kwargs):
    if model_name not in MODEL_REGISTRY:
        raise ValueError(f"Unknown model '{model_name}'. Available: {list(MODEL_REGISTRY)}")
    model = MODEL_REGISTRY[model_name]()
    if model_kwargs:
        model.set_params(**model_kwargs)
    model.fit(X_train, y_train)
    logger.info("train_model: trained '%s' on %d rows, %d features.", model_name, len(X_train), X_train.shape[1])
    return model


def get_feature_importance(model, feature_names) -> dict:
    if hasattr(model, "feature_importances_"):
        importances = model.feature_importances_
    elif hasattr(model, "coef_"):
        importances = abs(model.coef_)
    else:
        raise AttributeError(f"{type(model).__name__} exposes neither feature_importances_ nor coef_.")
    return dict(sorted(zip(feature_names, importances), key=lambda kv: -kv[1]))
