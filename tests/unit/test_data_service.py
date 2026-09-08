"""Unit tests for src.services.data_service."""

import pandas as pd

from src.services.data_service import (
    PRODUCTION_MODEL_FILENAME,
    load_all_model_metadata,
    load_cleaned_dataset,
    load_feature_dataset,
    load_production_model,
)


def test_load_cleaned_dataset_returns_real_data():
    df = load_cleaned_dataset()
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (2191, 9)
    assert "AQI" in df.columns


def test_load_feature_dataset_returns_real_data():
    df = load_feature_dataset()
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2101  # per FEATURE_DOCUMENTATION.md
    assert pd.api.types.is_datetime64_any_dtype(df["Date"])


def test_load_production_model_returns_model_and_metadata():
    model, metadata = load_production_model()
    assert hasattr(model, "predict")
    assert "feature_names" in metadata
    assert "validation_metrics" in metadata


def test_production_model_filename_exists_on_disk():
    from config.paths import TRAINED_MODELS_DIR
    assert (TRAINED_MODELS_DIR / PRODUCTION_MODEL_FILENAME).exists()


def test_load_all_model_metadata_finds_all_four_models():
    metadata_by_model = load_all_model_metadata()
    assert len(metadata_by_model) == 4
    assert "linear_regression_v1" in metadata_by_model
    assert "random_forest_v1" in metadata_by_model
    assert "random_forest_tuned_v1" in metadata_by_model
    assert "gradient_boosting_v1" in metadata_by_model


def test_load_all_model_metadata_each_has_validation_metrics():
    metadata_by_model = load_all_model_metadata()
    for name, metadata in metadata_by_model.items():
        assert "validation_metrics" in metadata, f"{name} missing validation_metrics"
        assert "MAE" in metadata["validation_metrics"]
