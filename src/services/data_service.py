"""
Data and model loading services for the AQI Forecast & Environmental
Analytics Platform dashboard.

These are thin, deliberately dumb wrappers around the already-tested
`preprocessing`/`model_io` modules. Their only job is to give
`dashboard/` pages a single, simple import (per Handbook Section 5.6:
"dashboard should never retrain models" / "the dashboard calls a
forecasting service that performs prediction" -- not preprocessing code
directly). Streamlit's own `@st.cache_data`/`@st.cache_resource`
decorators belong in the dashboard layer, wrapped around these functions
-- not baked in here, since these functions have no Streamlit dependency
and are independently testable without it.
"""

from typing import Dict, Tuple

import pandas as pd

from config.paths import PROCESSED_DATA_DIR, TRAINED_MODELS_DIR
from src.models.model_io import load_model
from src.preprocessing.data_loader import load_dataset
from src.utils.logger import get_logger

logger = get_logger(__name__)

# The model selected in 06_model_evaluation.ipynb (test-set MAE winner).
# Centralized here so a future re-evaluation only needs to change one line,
# not every dashboard page that loads a model.
PRODUCTION_MODEL_FILENAME = "linear_regression_v1.joblib"


def load_cleaned_dataset() -> pd.DataFrame:
    """Load the cleaned dataset (Date, AQI, pollutants, City) for dashboard display."""
    return load_dataset(PROCESSED_DATA_DIR / "delhi_aqi_cleaned.csv")


def load_feature_dataset() -> pd.DataFrame:
    """Load the full feature-engineered dataset (for Model Performance page, etc.)."""
    df = pd.read_csv(PROCESSED_DATA_DIR / "delhi_aqi_features.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    return df


def load_production_model() -> Tuple[object, Dict]:
    """
    Load the current production model and its metadata.

    Returns
    -------
    (model, metadata)
    """
    return load_model(TRAINED_MODELS_DIR / PRODUCTION_MODEL_FILENAME)


def load_all_model_metadata() -> Dict[str, Dict]:
    """
    Load metadata (not the models themselves) for every trained model in
    `models/trained/` -- used by the Model Performance comparison page,
    which needs metrics for all 4 candidates without paying the cost of
    deserializing 4 full models just to show a comparison table.
    """
    import json

    metadata_by_model = {}
    for path in sorted(TRAINED_MODELS_DIR.glob("*.metadata.json")):
        model_name = path.name.replace(".metadata.json", "")
        with open(path) as f:
            metadata_by_model[model_name] = json.load(f)

    logger.info("load_all_model_metadata: loaded metadata for %d models.", len(metadata_by_model))
    return metadata_by_model
