# ui_components/simulation_ui.py
import streamlit as st
import pandas as pd
from utils.plotting import update_plot

def build_simulation_ui():
    model_params = {
        "SIR": {
            "Population": 1000,
            "Susceptible": 990,  # Default values for each compartment
            "Infected": 10,
            "Recovered": 0,
            "Infection Rate (beta)": 0.2,
            "Recovery Rate (gamma)": 0.1,
            "Natural Death Rate": 0.01,
            "Disease Death Rate": 0.05,
            "Time in Days":200
        },
        "SEIR": {
            "Population": 1000,
            "Susceptible": 990,
            "Exposed": 0,
            "Infected": 10,
            "Recovered": 0,
            "Recruitment Rate(Birth_rate)":0.0,
            "Infection Rate (beta)": 0.2,
            "Recovery Rate (gamma)": 0.1,
            "Incubation Rate (alpha)": 0.1,
            "Natural Death Rate": 0.01,
            "Disease Death Rate": 0.05,
            "Time in Days": 200
        },
        "SIS": {
            "Population": 1000,
            "Susceptible": 990,
            "Infected": 10,
            "Infection Rate (beta)": 0.3,
            "Recovery Rate (gamma)": 0.1,
            "Natural Death Rate": 0.01,
            "Time in Days":200
        },
    }

    # Sidebar for model selection
    st.sidebar.header("Model Selection")
    model_choice = st.sidebar.selectbox("Select Epidemic Model", list(model_params.keys()))
    
    # Set title for the selected model
    st.title(f"{model_choice} Model Simulation")

    # Set default parameters based on selected model
    params = model_params[model_choice]

    # Sidebar dropdown for adjusting compartment values
    st.sidebar.header("Compartment Values")
    compartments = [key for key in params.keys() if key in ["Susceptible", "Exposed", "Infected", "Recovered"]]
    selected_compartment = st.sidebar.selectbox("Select Compartment", compartments)
    params[selected_compartment] = st.sidebar.number_input(f"Initial {selected_compartment}", value=params[selected_compartment], min_value=0)

    # Sidebar for model parameters
    st.sidebar.header("Model Parameters")
    params["Population"] = st.sidebar.number_input("Population", value=params["Population"], min_value=1)
    params["Time in Days"] = st.sidebar.number_input("Time in Days",value=params["Time in Days"],min_value=1)
    params["Infection Rate (beta)"] = st.sidebar.slider("Infection Rate (beta)", 0.0, 1.0, params["Infection Rate (beta)"])
    params["Recovery Rate (gamma)"] = st.sidebar.slider("Recovery Rate (gamma)", 0.0, 1.0, params["Recovery Rate (gamma)"])
    

    # Show additional parameters based on model choice
    if model_choice == "SEIR":
        params["Incubation Rate (alpha)"] = st.sidebar.slider("Incubation Rate (alpha)", 0.0, 1.0, params["Incubation Rate (alpha)"])
        params["Recruitment Rate(Birth_rate)"] = st.sidebar.slider("Recruitment Rate(Birth_rate)",0.0,1.0,params["Recruitment Rate(Birth_rate)"])
    if "Natural Death Rate" in params:
        params["Natural Death Rate"] = st.sidebar.slider("Natural Death Rate", 0.0, 1.0, params["Natural Death Rate"])
    if "Disease Death Rate" in params:
        params["Disease Death Rate"] = st.sidebar.slider("Disease Death Rate", 0.0, 1.0, params["Disease Death Rate"],1/100)
    if "Recruitment Rate(Birth_rate)" in params:
        print(123)
    # Dsplay the graph
    st.subheader("Graph")
    update_plot(model_choice, params)

    # Display the summary table below the graph
    st.subheader("Summary Table")
    summary_df = pd.DataFrame(list(params.items()), columns=["Parameter", "Value"])
    st.dataframe(summary_df, height=300)

    return model_choice
