# ui_components.py
import streamlit as st
import pandas as pd
from plotting import update_plot
from seir_model import seir_model  # Ensure you have imported the relevant model functions
from sir_model import sir_model

def build_ui():
    # Dictionary of parameter configurations for each model
    model_params = {
        "SIR": {
            "Population": 1000,
            "Initial Infected": 10,
            "Infection Rate (beta)": 0.2,
            "Recovery Rate (gamma)": 0.1,
            "Natural Death Rate": 0.01,
            "Disease Death Rate": 0.05
        },
        "SEIR": {
            "Population": 1000,
            "Initial Infected": 10,
            "Infection Rate (beta)": 0.2,
            "Recovery Rate (gamma)": 0.1,
            "Incubation Rate (alpha)": 0.1,
            "Natural Death Rate": 0.01,
            "Disease Death Rate": 0.05
        },
        # Add configurations for other models here as needed
        "SIS": {
            "Population": 1000,
            "Initial Infected": 10,
            "Infection Rate (beta)": 0.3,
            "Recovery Rate (gamma)": 0.1,
            "Natural Death Rate": 0.01,
        },
    }
    
    # Sidebar for model selection
    st.sidebar.header("Model Selection")
    model_choice = st.sidebar.selectbox("Select Epidemic Model", list(model_params.keys()))

    # Set default parameters based on selected model
    params = model_params[model_choice]

    # Display parameters dynamically based on the selected model
    st.sidebar.header("Parameters")
    params["Population"] = st.sidebar.number_input("Population", value=params["Population"], min_value=1)
    params["Initial Infected"] = st.sidebar.number_input("Initial Infected", value=params["Initial Infected"], min_value=0)
    params["Infection Rate (beta)"] = st.sidebar.slider("Infection Rate (beta)", 0.0, 1.0, params["Infection Rate (beta)"])
    params["Recovery Rate (gamma)"] = st.sidebar.slider("Recovery Rate (gamma)", 0.0, 1.0, params["Recovery Rate (gamma)"])
    
    if "Incubation Rate (alpha)" in params:
        params["Incubation Rate (alpha)"] = st.sidebar.slider("Incubation Rate (alpha)", 0.0, 1.0, params["Incubation Rate (alpha)"])
    if "Natural Death Rate" in params:
        params["Natural Death Rate"] = st.sidebar.slider("Natural Death Rate", 0.0, 0.1, params["Natural Death Rate"])
    if "Disease Death Rate" in params:
        params["Disease Death Rate"] = st.sidebar.slider("Disease Death Rate", 0.0, 0.1, params["Disease Death Rate"])

    col1, col2 = st.columns([1, 1.5])

    with col1:
        st.subheader("Summary Table")
        summary_df = pd.DataFrame(list(params.items()), columns=["Parameter", "Value"])
        st.dataframe(summary_df, height=300)

    with col2:
        st.subheader("Graph")
        # Pass the selected model and parameters to the plot
        update_plot(model_choice, params)
