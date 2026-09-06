"""Model serialization (ML-REG-001)."""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Tuple, Union

import joblib

from src.utils.logger import get_logger

logger = get_logger(__name__)


def save_model(model, path: Union[str, Path], metadata: Dict) -> Path:
    model_path = Path(path)
    model_path.parent.mkdir(parents=True, exist_ok=True)
    metadata = dict(metadata)
    metadata.setdefault("saved_at", datetime.now(timezone.utc).isoformat())
    metadata.setdefault("model_class", type(model).__name__)
    joblib.dump(model, model_path)
    metadata_path = model_path.with_suffix(".metadata.json")
    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=2)
    logger.info("save_model: saved '%s' with metadata '%s'.", model_path, metadata_path)
    return model_path


def load_model(path: Union[str, Path]) -> Tuple[object, Dict]:
    model_path = Path(path)
    metadata_path = model_path.with_suffix(".metadata.json")
    if not model_path.exists():
        raise FileNotFoundError(f"Model file not found: '{model_path}'")
    if not metadata_path.exists():
        raise FileNotFoundError(f"Metadata sidecar not found: '{metadata_path}'")
    model = joblib.load(model_path)
    with open(metadata_path) as f:
        metadata = json.load(f)
    logger.info("load_model: loaded '%s' (%s).", model_path, metadata.get("model_class"))
    return model, metadata
