from pathlib import Path
import json

import streamlit as st

from common import (
    RAW_EXPERIMENT_DIR,
    initialise_session_state,
    show_sidebar,
)


initialise_session_state()
show_sidebar()

st.title("3. Experiment")

st.write(
    "Configure and run local experiments. Later, these same settings can "
    "map to CloudLab architecture experiments."
)

architecture_id = st.selectbox(
    "Architecture",
    [
        "A0-local",
        "A1-bare-metal-monolith",
        "A2-kubernetes-monolith",
        "A3-kubernetes-microservices",
        "A4-event-driven",
    ],
)

workload_mode = st.selectbox(
    "Workload mode",
    [
        "RF_FIXED",
        "RF_PERIODIC_20",
        "RULE_BASED",
    ],
)

event_rate = st.number_input(
    "Event rate per second",
    min_value=1,
    value=5,
)

experiment_id = st.text_input(
    "Experiment ID",
    value=f"EXP-{architecture_id}-UI-001",
)

st.subheader("Selected inputs")

st.write(f"Dataset: `{st.session_state.selected_dataset_name or 'None'}`")
st.write(f"Model: `{st.session_state.selected_model_name or 'None'}`")

if st.button("Save experiment config", type="primary"):
    RAW_EXPERIMENT_DIR.mkdir(parents=True, exist_ok=True)

    config = {
        "experiment_id": experiment_id,
        "architecture_id": architecture_id,
        "workload_mode": workload_mode,
        "event_rate_per_second": event_rate,
        "dataset_path": st.session_state.selected_dataset_path,
        "model_path": st.session_state.selected_model_path,
    }

    config_path = RAW_EXPERIMENT_DIR / f"{experiment_id}-config.json"

    with config_path.open("w", encoding="utf-8") as file:
        json.dump(config, file, indent=2)

    st.success(f"Saved experiment config: `{config_path.name}`")
    st.session_state.selected_experiment_output_path = str(config_path)

    st.toast("Experiment config saved.")

st.divider()

if st.session_state.selected_experiment_output_path:
    if st.button("View results"):
        st.switch_page("pages/5_Results.py")