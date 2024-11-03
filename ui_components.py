# ui_components.py
import streamlit as st
import pandas as pd
from plotting import update_plot
from seir_model import seir_model
from sir_model import sir_model
from sis_model import sis_model

def build_ui():
    model_params = {
        "SIR": {
            "Population": 1000,
            "Susceptible": 990,  # Default values for each compartment
            "Infected": 10,
            "Recovered": 0,
            "Infection Rate (beta)": 0.2,
            "Recovery Rate (gamma)": 0.1,
            "Natural Death Rate": 0.01,
            "Disease Death Rate": 0.05
        },
        "SEIR": {
            "Population": 1000,
            "Susceptible": 990,
            "Exposed": 0,
            "Infected": 10,
            "Recovered": 0,
            "Infection Rate (beta)": 0.2,
            "Recovery Rate (gamma)": 0.1,
            "Incubation Rate (alpha)": 0.1,
            "Natural Death Rate": 0.01,
            "Disease Death Rate": 0.05
        },
        "SIS": {
            "Population": 1000,
            "Susceptible": 990,
            "Infected": 10,
            "Infection Rate (beta)": 0.3,
            "Recovery Rate (gamma)": 0.1,
            "Natural Death Rate": 0.01,
        },
    }
    
    st.sidebar.header("Model Selection")
    model_choice = st.sidebar.selectbox("Select Epidemic Model", list(model_params.keys()))

    #set title
    st.title(f"{model_choice} MODEL")
    
    # Set default parameters based on selected model
    params = model_params[model_choice]

    # Dropdown for compartments based on selected model
    st.sidebar.header("Compartment Values")
    compartments = [key for key in params.keys() if key in ["Susceptible", "Exposed", "Infected", "Recovered"]]
    selected_compartment = st.sidebar.selectbox("Select Compartment", compartments)
    params[selected_compartment] = st.sidebar.number_input(f"Initial {selected_compartment}", value=params[selected_compartment], min_value=0)

    # Display other model-specific parameters
    st.sidebar.header("Model Parameters")
    params["Population"] = st.sidebar.number_input("Population", value=params["Population"], min_value=1)
    params["Infection Rate (beta)"] = st.sidebar.slider("Infection Rate (beta)", 0.0, 1.0, params["Infection Rate (beta)"])
    params["Recovery Rate (gamma)"] = st.sidebar.slider("Recovery Rate (gamma)", 0.0, 1.0, params["Recovery Rate (gamma)"])

    # Show additional parameters based on model choice
    if model_choice == "SEIR":
        params["Incubation Rate (alpha)"] = st.sidebar.slider("Incubation Rate (alpha)", 0.0, 1.0, params["Incubation Rate (alpha)"])
    if "Natural Death Rate" in params:
        params["Natural Death Rate"] = st.sidebar.slider("Natural Death Rate", 0.0, 0.1, params["Natural Death Rate"])
    if "Disease Death Rate" in params:
        params["Disease Death Rate"] = st.sidebar.slider("Disease Death Rate", 0.0, 0.1, params["Disease Death Rate"])

    # Summary table and plot
    col1, col2 = st.columns([1, 1.5])

    with col1:
        st.subheader("Summary Table")
        summary_df = pd.DataFrame(list(params.items()), columns=["Parameter", "Value"])
        st.dataframe(summary_df, height=300)

    with col2:
        st.subheader("Graph")
        update_plot(model_choice, params)
