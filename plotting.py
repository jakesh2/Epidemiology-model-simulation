# plotting.py
from seir_model import seir_model  # Import SEIR model function
from sir_model import sir_model
import plotly.graph_objects as go
import streamlit as st

def update_plot(model_choice, params):
    # Choose the model function
    if model_choice == "SIR":
        S, I, R = sir_model(params["Population"], params["Initial Infected"], params["Infection Rate (beta)"],
                            params["Recovery Rate (gamma)"], params["Natural Death Rate"], params["Disease Death Rate"])
        compartments = {"Susceptible": S, "Infected": I, "Recovered": R}
    
    elif model_choice == "SEIR":
        S, E, I, R = seir_model(params["Population"], params["Initial Infected"], params["Infection Rate (beta)"],
                                params["Recovery Rate (gamma)"], params["Incubation Rate (alpha)"],
                                params["Natural Death Rate"], params["Disease Death Rate"])
        compartments = {"Susceptible": S, "Exposed": E, "Infected": I, "Recovered": R}

    # Plot with a default line chart
    fig = go.Figure()
    days = list(range(len(next(iter(compartments.values())))))  # Get the length of days

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
