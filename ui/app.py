import streamlit as st

from common import initialise_session_state


st.set_page_config(
    page_title="Portfolio AI Dashboard",
    layout="wide",
)

initialise_session_state()

home_page = st.Page(
    "views/home.py",
    title="Home",
    icon="🏠",
)

download_data_page = st.Page(
    "views/create_dataset.py",
    title="Download Data",
    icon="📈",
)

train_model_page = st.Page(
    "views/train_model.py",
    title="Train Model",
    icon="🧠",
)

experiment_page = st.Page(
    "views/experiments.py",
    title="Experiments",
    icon="🧪",
)

results_page = st.Page(
    "views/results.py",
    title="Results",
    icon="📊",
)

model_registry_page = st.Page(
    "views/model_registry.py",
    title="Model Registry",
    icon="🗂️",
)

navigation = st.navigation(
    {
        "Main": [home_page],
        "Pipeline": [
            download_data_page,
            train_model_page,
            experiment_page,
        ],
        "Management": [
            model_registry_page,
        ],
        "Results": [results_page],
    }
)

navigation.run()