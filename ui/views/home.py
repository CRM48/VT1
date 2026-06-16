import streamlit as st

from common import show_sidebar


show_sidebar()

st.title("Portfolio AI Experiment Dashboard")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📈 Download Data")
    st.write("Create reusable historical stock-price datasets from yfinance.")

    if st.button("Open Download Data", use_container_width=True):
        st.switch_page("views/create_dataset.py")

with col2:
    st.markdown("### 🧠 Train Model")
    st.write("Train a model, record accuracy, and create injection data.")

    if st.button("Open Train Model", use_container_width=True):
        st.switch_page("views/train_model.py")

col3, col4 = st.columns(2)

with col3:
    st.markdown("### 🧪 Experiments")
    st.write("Run local or CloudLab-style architecture experiments.")

    if st.button("Open Experiments", use_container_width=True):
        st.switch_page("views/experiment.py")

with col4:
    st.markdown("### 🗂️ Model Registry")
    st.write("View, select, and delete trained models.")
    if st.button("Open Model Registry", use_container_width=True):
        st.switch_page("views/model_registry.py")

st.markdown("### 📊 Results")
st.write("Inspect saved prediction files, metrics, and experiment outputs.")
if st.button("Open Results", use_container_width=True):
    st.switch_page("views/results.py")

st.divider()