import joblib
from pathlib import Path


def load_model(model_path: Path):
    loaded_object = joblib.load(model_path)

    if isinstance(loaded_object, dict) and "model" in loaded_object:
        return loaded_object["model"]

    return loaded_object


def load_model_package(model_path: Path) -> dict:
    loaded_object = joblib.load(model_path)

    if isinstance(loaded_object, dict) and "model" in loaded_object:
        return loaded_object

    return {
        "model": loaded_object,
        "feature_columns": None,
        "model_type": "unknown",
    }