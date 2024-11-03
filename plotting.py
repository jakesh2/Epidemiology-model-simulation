# plotting.py
from seir_model import seir_model
from sir_model import sir_model
from sis_model import sis_model
import plotly.graph_objects as go
import streamlit as st

def update_plot(model_choice, params):
    # Check the selected model and handle parameters accordingly
    if model_choice == "SIR":
        # Ensure "Initial Infected" and other necessary parameters are in params
        S, I, R = sir_model(
            params["Population"],
            params.get("Initial Infected", 1),  # Set a default of 1 if "Initial Infected" is missing
            params["Infection Rate (beta)"],
            params["Recovery Rate (gamma)"],
            params.get("Natural Death Rate", 0),
            params.get("Disease Death Rate", 0)
        )
        compartments = {"Susceptible": S, "Infected": I, "Recovered": R}

    elif model_choice == "SEIR":
        # Ensure required parameters for SEIR model
        S, E, I, R = seir_model(
            params["Population"],
            params.get("Initial Infected", 1),
            params["Infection Rate (beta)"],
            params["Recovery Rate (gamma)"],
            params.get("Incubation Rate (alpha)", 0.1),
            params.get("Natural Death Rate", 0),
            params.get("Disease Death Rate", 0)
        )
        compartments = {"Susceptible": S, "Exposed": E, "Infected": I, "Recovered": R}

    elif model_choice == "SIS":
        # Ensure required parameters for SIS model
        S, I = sis_model(
            params["Population"],
            params.get("Initial Infected", 1),
            params["Infection Rate (beta)"],
            params["Recovery Rate (gamma)"],
            params.get("Natural Death Rate", 0)
        )
        compartments = {"Susceptible": S, "Infected": I}

    # Default line chart for visualization
    fig = go.Figure()
    days = list(range(len(next(iter(compartments.values())))))  # Get the number of days

    for name, data in compartments.items():
        fig.add_trace(go.Scatter(x=days, y=data, mode='lines', name=name))

    fig.update_layout(
        title=f"{model_choice} Model Simulation",
        xaxis_title="Days",
        yaxis_title="Population",
        hovermode="x",
        legend_title="Compartments",
    )

    st.plotly_chart(fig, use_container_width=True)
