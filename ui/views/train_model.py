from pathlib import Path
import re

import streamlit as st

from common import (
    DATA_DIR,
    MODEL_DIR,
    PROJECT_ROOT,
    initialise_session_state,
    list_csv_files,
    show_sidebar,
)
from portfolio_system.ml.training_pipeline import run_training_pipeline


INJECTION_DIR = PROJECT_ROOT / "experiments" / "injection"
REGISTRY_PATH = MODEL_DIR / "registry.csv"
TRAINING_ROWS_DIR = DATA_DIR / "training_rows"


initialise_session_state()
show_sidebar()

st.title("2. Train Model")

st.write(
    "Train a model using the first part of a dataset and reserve the later "
    "part as injection data for experiments."
)

# ------------------------------------------------------------
# Dataset selection
# ------------------------------------------------------------

price_files = [
    path for path in list_csv_files(DATA_DIR)
    if path.name.endswith("_prices.csv")
]

if not price_files:
    st.warning("No price datasets found.")

    if st.button("Create dataset"):
        st.switch_page("pages/1_Create_Dataset.py")

    st.stop()


default_index = 0

if st.session_state.get("selected_dataset_path"):
    selected_path = Path(st.session_state.selected_dataset_path)

    if selected_path in price_files:
        default_index = price_files.index(selected_path)


selected_dataset = st.selectbox(
    "Dataset",
    price_files,
    index=default_index,
    format_func=lambda path: path.name,
)

st.session_state.selected_dataset_path = str(selected_dataset)
st.session_state.selected_dataset_name = selected_dataset.name


# ------------------------------------------------------------
# Data split
# ------------------------------------------------------------

st.subheader("Data split")

development_ratio = st.slider(
    "Model-development data",
    min_value=0.3,
    max_value=0.8,
    value=0.5,
    step=0.05,
)

injection_ratio = 1 - development_ratio

st.write(
    f"{development_ratio:.0%} of the dataset will be used to train/test "
    f"the model. {injection_ratio:.0%} will be reserved as injection data "
    "for experiments."
)

st.caption(
    "The split is chronological: the earlier part is used for model "
    "development, and the later part becomes future incoming data."
)


# ------------------------------------------------------------
# Train/test split
# ------------------------------------------------------------

st.subheader("Train/test split")

train_ratio = st.slider(
    "Train split within model-development data",
    min_value=0.6,
    max_value=0.9,
    value=0.8,
    step=0.05,
)

test_ratio = 1 - train_ratio

st.write(f"Test split within model-development data: {test_ratio:.0%}")

st.caption(
    "The model is first trained on the train split and evaluated on the "
    "test split. After the test accuracy is recorded, the final saved model "
    "is trained on all labelled rows from the model-development section."
)


# ------------------------------------------------------------
# Label settings
# ------------------------------------------------------------

st.subheader("Prediction target")

label_horizon = st.number_input(
    "Prediction horizon",
    min_value=1,
    value=5,
    step=1,
    help=(
        "How many rows ahead the model should predict. "
        "For daily data, 5 means roughly one trading week ahead."
    ),
)

label_threshold = st.number_input(
    "Label threshold",
    min_value=0.0,
    value=0.02,
    step=0.005,
    format="%.3f",
    help=(
        "Minimum future return needed for BUY or SELL. "
        "For example, 0.02 means +2% is BUY and -2% is SELL."
    ),
)

st.write(
    f"Labels will be created using a {label_horizon}-step future price "
    f"movement and a {label_threshold:.1%} threshold."
)


# ------------------------------------------------------------
# Model settings
# ------------------------------------------------------------

st.subheader("Model")

model_type = st.selectbox(
    "Model type",
    ["Random Forest"],
)

default_model_name = selected_dataset.stem.replace(
    "_prices",
    "",
)

default_model_name = f"{default_model_name}-rf-v1"

model_name = st.text_input(
    "Model name",
    value=default_model_name,
)

model_name = model_name.strip().replace(" ", "-")

model_name = re.sub(
    r"[^A-Za-z0-9_-]",
    "",
    model_name,
)

if not model_name:
    st.error("Model name must not be empty.")

model_path = MODEL_DIR / f"{model_name}.joblib"

st.write("Model file:")
st.code(model_path.name)

if model_path.exists():
    st.warning("A model with this name already exists. Choose another name.")


# ------------------------------------------------------------
# Train button
# ------------------------------------------------------------

can_train = (
    bool(model_name)
    and not model_path.exists()
)

if st.button(
    "Train model",
    type="primary",
    disabled=not can_train,
):
    try:
        with st.spinner("Training model and creating injection data..."):
            summary = run_training_pipeline(
                source_dataset_path=selected_dataset,
                model_name=model_name,
                model_output_dir=MODEL_DIR,
                training_rows_output_dir=TRAINING_ROWS_DIR,
                injection_output_dir=INJECTION_DIR,
                registry_path=REGISTRY_PATH,
                development_ratio=development_ratio,
                train_ratio=train_ratio,
                label_horizon=label_horizon,
                label_threshold=label_threshold,
            )

        st.session_state.selected_model_path = str(summary.model_path)
        st.session_state.selected_model_name = summary.model_path.name
        st.session_state.selected_injection_data_path = str(
            summary.injection_data_path
        )

        st.success("Model trained successfully.")

        col1, col2 = st.columns(2)

        col1.metric(
            "Train accuracy",
            f"{summary.train_accuracy:.3f}",
        )

        col2.metric(
            "Test accuracy",
            f"{summary.test_accuracy:.3f}",
        )

        st.subheader("Saved artifacts")

        st.write(f"Model saved to: `{summary.model_path}`")
        st.write(f"Training rows saved to: `{summary.training_rows_path}`")
        st.write(f"Injection data saved to: `{summary.injection_data_path}`")

        st.subheader("Split summary")

        st.write(f"Train rows: `{summary.train_rows}`")
        st.write(f"Test rows: `{summary.test_rows}`")
        st.write(f"Final training rows: `{summary.final_training_rows}`")
        st.write(f"Injection rows: `{summary.injection_rows}`")

        st.subheader("Prediction target")

        st.write(f"Prediction horizon: `{summary.label_horizon}`")
        st.write(f"Label threshold: `{summary.label_threshold}`")

        st.subheader("Time ranges")

        st.write(f"Model-development start: `{summary.train_start_timestamp}`")
        st.write(f"Model-development end: `{summary.train_end_timestamp}`")
        st.write(f"Injection start: `{summary.injection_start_timestamp}`")
        st.write(f"Injection end: `{summary.injection_end_timestamp}`")

        st.toast("Training complete.")

    except Exception as error:
        st.error(str(error))


# ------------------------------------------------------------
# Next step
# ------------------------------------------------------------

st.divider()

if st.session_state.get("selected_injection_data_path"):
    st.subheader("Next step")

    st.write(
        "The model has been trained and injection data has been created."
    )

    if st.button("Use injection data in experiment"):
        st.switch_page("pages/4_Experiment.py")