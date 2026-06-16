from pathlib import Path
import json

import pandas as pd
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data" / "processed"
MODEL_DIR = PROJECT_ROOT / "models"
RAW_EXPERIMENT_DIR = PROJECT_ROOT / "experiments" / "raw"
INJECTION_DIR = PROJECT_ROOT / "experiments" / "injection"


def initialise_session_state() -> None:
    defaults = {
        "selected_dataset_path": None,
        "selected_dataset_name": None,
        "selected_training_dataset_path": None,
        "selected_model_path": None,
        "selected_model_name": None,
        "selected_injection_data_path": None,
        "selected_evaluation_output_path": None,
        "selected_experiment_output_path": None,
        "last_action_message": None,
        "selected_pipeline_page": "Download Data",
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def list_csv_files(directory: Path) -> list[Path]:
    if not directory.exists():
        return []

    return sorted(directory.glob("*.csv"))


def list_model_files(directory: Path) -> list[Path]:
    if not directory.exists():
        return []

    return sorted(directory.glob("*.joblib"))


def list_jsonl_files(directory: Path) -> list[Path]:
    if not directory.exists():
        return []

    return sorted(directory.glob("*.jsonl"))


def load_jsonl(path: Path) -> pd.DataFrame:
    rows = []

    with path.open("r", encoding="utf-8") as file:
        for line in file:
            rows.append(json.loads(line))

    return pd.DataFrame(rows)


def show_sidebar() -> None:
    st.sidebar.subheader("Current Selection")

    st.sidebar.write(
        f"Dataset: `{st.session_state.selected_dataset_name or 'None'}`"
    )

    st.sidebar.write(
        f"Model: `{st.session_state.selected_model_name or 'None'}`"
    )

    injection_path = st.session_state.get("selected_injection_data_path")

    if injection_path:
        injection_name = Path(injection_path).name
    else:
        injection_name = "None"

    st.sidebar.write(
        f"Injection data: `{injection_name}`"
    )

    if st.session_state.last_action_message:
        st.sidebar.caption(
            f"Last action: {st.session_state.last_action_message}"
        )

def get_registry_path() -> Path:
    return MODEL_DIR / "registry.csv"


def load_model_registry() -> pd.DataFrame:
    registry_path = get_registry_path()

    if not registry_path.exists():
        return pd.DataFrame()

    return pd.read_csv(registry_path)


def save_model_registry(registry_data: pd.DataFrame) -> None:
    registry_path = get_registry_path()
    registry_path.parent.mkdir(parents=True, exist_ok=True)
    registry_data.to_csv(registry_path, index=False)


def delete_file_if_exists(path_text: str | None) -> bool:
    if path_text is None or pd.isna(path_text) or not str(path_text).strip():
        return False

    path = Path(str(path_text))

    if path.exists() and path.is_file():
        path.unlink()
        return True

    return False


def delete_model_registry_entry(model_name: str) -> dict:
    registry_data = load_model_registry()

    if registry_data.empty:
        raise ValueError("Model registry is empty.")

    if "model_name" not in registry_data.columns:
        raise ValueError("Model registry is missing the model_name column.")

    matching_rows = registry_data[registry_data["model_name"] == model_name]

    if matching_rows.empty:
        raise ValueError(f"No registry entry found for model: {model_name}")

    row = matching_rows.iloc[0]

    deleted_files = []

    for column in [
        "model_path",
        "training_rows_path",
        "injection_data_path",
    ]:
        if column in row and delete_file_if_exists(row[column]):
            deleted_files.append(str(row[column]))

    updated_registry = registry_data[
        registry_data["model_name"] != model_name
    ].copy()

    save_model_registry(updated_registry)

    return {
        "model_name": model_name,
        "deleted_files": deleted_files,
    }