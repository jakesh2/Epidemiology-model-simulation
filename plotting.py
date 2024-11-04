# plotting.py
import streamlit as st
import plotly.graph_objects as go
from sir_model import sir_model
from seir_model import seir_model
from sis_model import sis_model

def update_plot(model_choice, params):
    """
    Updates the plot based on the selected epidemic model and parameters.

    Args:
        model_choice (str): The selected epidemic model (SIR, SEIR, SIS).
        params (dict): Parameters for the selected model.
    """
    # Set initial_infected with a default fallback if not provided
    initial_infected = params.get("Initial Infected", 10)

    # Initialize the plot based on the model choice
    if model_choice == "SIR":
        S, I, R = sir_model(
            population=params["Population"],
            initial_infected=initial_infected,
            beta=params["Infection Rate (beta)"],
            gamma=params["Recovery Rate (gamma)"],
            natural_death=params.get("Natural Death Rate", 0),
            disease_death=params.get("Disease Death Rate", 0)
        )
        compartments = {"Susceptible": S, "Infected": I, "Recovered": R}
    
    elif model_choice == "SEIR":
        S, E, I, R = seir_model(
            population=params["Population"],
            initial_infected=initial_infected,
            beta=params["Infection Rate (beta)"],
            gamma=params["Recovery Rate (gamma)"],
            alpha=params["Incubation Rate (alpha)"],
            natural_death=params.get("Natural Death Rate", 0),
            disease_death=params.get("Disease Death Rate", 0)
        )
        compartments = {"Susceptible": S, "Exposed": E, "Infected": I, "Recovered": R}
    
    elif model_choice == "SIS":
        S, I = sis_model(
            population=params["Population"],
            initial_infected=initial_infected,
            beta=params["Infection Rate (beta)"],
            gamma=params["Recovery Rate (gamma)"],
            natural_death=params.get("Natural Death Rate", 0)
        )
        compartments = {"Susceptible": S, "Infected": I}
    
    # Create a Plotly figure
    fig = go.Figure()
    days = list(range(len(next(iter(compartments.values())))))  # Get the number of days from the length of the data

    # Add traces for each compartment
    for name, data in compartments.items():
        fig.add_trace(go.Scatter(x=days, y=data, mode='lines', name=name))

    # Update layout for the plot
    fig.update_layout(
        title=f"{model_choice} Model Simulation",
        xaxis_title="Days",
        yaxis_title="Population",
        hovermode="x",
        legend_title="Compartments",
    )

    # Display the plot in the Streamlit app
    st.plotly_chart(fig, use_container_width=True)
