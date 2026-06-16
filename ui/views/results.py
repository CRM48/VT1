from pathlib import Path

import streamlit as st

from common import (
    RAW_EXPERIMENT_DIR,
    initialise_session_state,
    list_jsonl_files,
    load_jsonl,
    show_sidebar,
)


initialise_session_state()
show_sidebar()

st.title("Results")

result_files = list_jsonl_files(RAW_EXPERIMENT_DIR)

if not result_files:
    st.warning("No JSONL result files found.")
    st.stop()

default_index = 0

if st.session_state.selected_evaluation_output_path:
    selected_output_path = Path(
        st.session_state.selected_evaluation_output_path
    )

    if selected_output_path in result_files:
        default_index = result_files.index(selected_output_path)

selected_file = st.selectbox(
    "Result file",
    result_files,
    index=default_index,
    format_func=lambda path: path.name,
)

data = load_jsonl(selected_file)

st.write(f"Rows: {len(data)}")

if "correct" in data.columns:
    accuracy = data["correct"].mean()
    st.metric("Accuracy", f"{accuracy:.3f}")

if "actual_label" in data.columns:
    st.subheader("Actual label distribution")
    st.bar_chart(data["actual_label"].value_counts())

if "predicted_label" in data.columns:
    st.subheader("Predicted label distribution")
    st.bar_chart(data["predicted_label"].value_counts())

if "timestamp" in data.columns:
    st.subheader("Time range")
    st.write(f"Start: `{data['timestamp'].min()}`")
    st.write(f"End: `{data['timestamp'].max()}`")

st.subheader("Raw results")
st.dataframe(data)

st.divider()

if st.button("Start another dataset"):
    st.switch_page("pages/1_Create_Dataset.py")