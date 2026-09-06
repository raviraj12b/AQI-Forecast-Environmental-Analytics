import numpy as np
import pandas as pd
import pytest
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression

from src.models.hyperparameter_tuning import tune_with_grid_search
from src.models.model_io import load_model, save_model
from src.models.model_trainer import MODEL_REGISTRY, get_feature_importance, train_model

@pytest.fixture
def toy_regression_data():
    rng = np.random.default_rng(42)
    X = pd.DataFrame({"f1": rng.uniform(0,100,200), "f2": rng.uniform(0,50,200)})
    y = 2*X["f1"] + 0.5*X["f2"] + rng.normal(0,1,200)
    return X, y

def test_train_model_linear_regression_returns_fitted_estimator(toy_regression_data):
    X, y = toy_regression_data
    assert isinstance(train_model("linear_regression", X, y), LinearRegression)

def test_train_model_random_forest_returns_fitted_estimator(toy_regression_data):
    X, y = toy_regression_data
    assert isinstance(train_model("random_forest", X, y), RandomForestRegressor)

def test_train_model_rejects_unknown_model_name(toy_regression_data):
    X, y = toy_regression_data
    with pytest.raises(ValueError):
        train_model("not_a_real_model", X, y)

def test_train_model_accepts_kwargs_override(toy_regression_data):
    X, y = toy_regression_data
    model = train_model("random_forest", X, y, n_estimators=10)
    assert model.n_estimators == 10

def test_model_registry_has_mandatory_and_optional_models():
    assert {"linear_regression","random_forest","gradient_boosting"}.issubset(MODEL_REGISTRY)

def test_get_feature_importance_random_forest(toy_regression_data):
    X, y = toy_regression_data
    model = train_model("random_forest", X, y)
    imp = get_feature_importance(model, list(X.columns))
    assert imp["f1"] > imp["f2"]

def test_get_feature_importance_linear_regression_uses_coefficients(toy_regression_data):
    X, y = toy_regression_data
    model = train_model("linear_regression", X, y)
    imp = get_feature_importance(model, list(X.columns))
    assert imp["f1"] > imp["f2"]

def test_tune_with_grid_search_returns_best_estimator_and_params(toy_regression_data):
    X, y = toy_regression_data
    best_model, best_params, best_score = tune_with_grid_search(
        RandomForestRegressor(random_state=42), {"n_estimators":[10,20],"max_depth":[3,5]}, X, y, n_splits=3
    )
    assert best_params["n_estimators"] in (10,20) and best_params["max_depth"] in (3,5)
    assert best_score >= 0

def test_save_and_load_model_roundtrip(toy_regression_data, tmp_path):
    X, y = toy_regression_data
    model = train_model("linear_regression", X, y)
    save_path = tmp_path / "test_model.joblib"
    save_model(model, save_path, metadata={"algorithm":"linear_regression","test":True})
    loaded_model, metadata = load_model(save_path)
    assert np.allclose(model.predict(X), loaded_model.predict(X))
    assert metadata["algorithm"]=="linear_regression" and "saved_at" in metadata

def test_load_model_raises_if_file_missing(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_model(tmp_path / "does_not_exist.joblib")

def test_save_model_creates_metadata_sidecar(toy_regression_data, tmp_path):
    X, y = toy_regression_data
    model = train_model("linear_regression", X, y)
    save_path = tmp_path / "sub" / "test_model.joblib"
    save_model(model, save_path, metadata={"algorithm":"linear_regression"})
    assert save_path.exists() and save_path.with_suffix(".metadata.json").exists()
