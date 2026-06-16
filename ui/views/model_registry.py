from pathlib import Path

import pandas as pd
import streamlit as st

from common import (
    delete_model_registry_entry,
    load_model_registry,
    show_sidebar,
)


show_sidebar()

st.title("Model Registry")

st.write(
    "View, select, and delete trained models and their associated training "
    "and injection data."
)

registry_data = load_model_registry()

if registry_data.empty:
    st.info("No models have been registered yet.")
    st.stop()


display_columns = [
    "model_name",
    "model_type",
    "test_accuracy",
    "source_dataset_path",
    "training_rows_path",
    "injection_data_path",
    "model_path",
]

existing_display_columns = [
    column for column in display_columns
    if column in registry_data.columns
]

display_data = registry_data[existing_display_columns].copy()

if "test_accuracy" in display_data.columns:
    display_data["test_accuracy"] = display_data["test_accuracy"].round(3)

for column in [
    "source_dataset_path",
    "training_rows_path",
    "injection_data_path",
    "model_path",
]:
    if column in display_data.columns:
        display_data[column] = display_data[column].apply(
            lambda value: Path(str(value)).name
            if pd.notna(value)
            else value
        )

st.subheader("Registered Models")

st.dataframe(
    display_data,
    use_container_width=True,
    hide_index=True,
)

st.divider()

st.subheader("Use a registered model")

model_names = registry_data["model_name"].tolist()

selected_model_name = st.selectbox(
    "Select model",
    model_names,
    key="registry_model_selector",
)

selected_row = registry_data[
    registry_data["model_name"] == selected_model_name
].iloc[0]

if st.button("Use this model for experiments", type="primary"):
    st.session_state.selected_model_path = selected_row["model_path"]
    st.session_state.selected_model_name = selected_row["model_name"]
    st.session_state.selected_injection_data_path = selected_row[
        "injection_data_path"
    ]

    st.success(f"Selected `{selected_model_name}` for experiments.")

st.write("Selected model details:")

details = {
    "Model name": selected_row.get("model_name", "Unknown"),
    "Model type": selected_row.get("model_type", "Unknown"),
    "Test accuracy": selected_row.get("test_accuracy", "Unknown"),
    "Source dataset": Path(str(selected_row.get("source_dataset_path", ""))).name,
    "Training rows": Path(str(selected_row.get("training_rows_path", ""))).name,
    "Injection data": Path(str(selected_row.get("injection_data_path", ""))).name,
    "Model file": Path(str(selected_row.get("model_path", ""))).name,
}

st.json(details)

st.divider()

st.subheader("Delete model")

st.warning(
    "Deleting a model will remove the registry entry, saved model file, "
    "training rows file, and injection data file."
)

confirm_delete = st.checkbox(
    f"I understand that `{selected_model_name}` and its associated files will be deleted."
)

if st.button(
    "Delete selected model",
    disabled=not confirm_delete,
):
    try:
        deletion_result = delete_model_registry_entry(
            selected_model_name
        )

        if st.session_state.get("selected_model_name") == selected_model_name:
            st.session_state.selected_model_path = None
            st.session_state.selected_model_name = None
            st.session_state.selected_injection_data_path = None

        st.success(
            f"Deleted registry entry for `{deletion_result['model_name']}`."
        )

        if deletion_result["deleted_files"]:
            st.write("Deleted files:")
            for deleted_file in deletion_result["deleted_files"]:
                st.write(f"- `{deleted_file}`")
        else:
            st.write("No associated files were found to delete.")

        st.rerun()

    except Exception as error:
        st.error(str(error))