# utils/plotting.py
import streamlit as st
import plotly.graph_objects as go
from models.sir_model import solve_model as sir_model
from models.seir_model import solve_model as seir_model
from models.sis_model import sis_model

def update_plot(model_choice, params, return_results=False):
    if model_choice == "SIR":
        S, I, R, r0, r_eff = sir_model(
            S=params["Susceptible"],
            I=params["Infected"],
            R=params["Recovered"],
            beta=params["Infection Rate (beta)"],
            gamma=params["Recovery Rate (gamma)"],
            natural_death_rate=params.get("Natural Death Rate", 0),
            disease_death_rate=params.get("Disease Death Rate", 0),
            birth_rate=params.get("Recruitment Rate(Birth_rate)", 0),
            v=params.get("Vaccination Rate (v)", 0),
            tau=params.get("Treatment Rate (tau)", 0),
            days=params["Time in Days"]
        )
        compartments = {"Susceptible": S, "Infected": I, "Recovered": R}
        incidence = params["Infection Rate (beta)"] * S * I

    elif model_choice == "SEIR":
        S, E, I, R, r0, r_eff = seir_model(
            S=params["Susceptible"],
            E=params["Exposed"],
            I=params["Infected"],
            R=params["Recovered"],
            beta=params["Infection Rate (beta)"],
            gamma=params["Recovery Rate (gamma)"],
            alpha=params["Incubation Rate (alpha)"],
            natural_death_rate=params.get("Natural Death Rate", 0),
            disease_death_rate=params.get("Disease Death Rate", 0),
            birth_rate=params["Recruitment Rate(Birth_rate)"],
            v=params.get("Vaccination Rate (v)", 0),
            tau=params.get("Treatment Rate (tau)", 0),
            days=params["Time in Days"]
        )
        compartments = {"Susceptible": S, "Exposed": E, "Infected": I, "Recovered": R}
        incidence = params["Infection Rate (beta)"] * S * I

    elif model_choice == "SIS":
        S, I = sis_model(
            population=params["Population"],
            initial_infected=params["Infected"],
            beta=params["Infection Rate (beta)"],
            gamma=params["Recovery Rate (gamma)"],
            natural_death=params.get("Natural Death Rate", 0),
            days=params["Time in Days"]
        )
        compartments = {"Susceptible": S, "Infected": I}
        incidence = params["Infection Rate (beta)"] * S * I

    days = list(range(len(next(iter(compartments.values())))))

    # If return_results is True, return the simulation results
    if return_results:
        if model_choice == "SEIR":
            return S, E, I, R, r0, r_eff
        elif model_choice == "SIR":
            return S, I, R, r0, r_eff
        elif model_choice == "SIS":
            return S, I

    # Otherwise, proceed with plotting
    plot_options = ["Compartment Dynamics", "Specific Compartment", "Incidence", "R₀ and R_eff"]
    plot_choice = st.selectbox("Choose what to plot", plot_options)

    fig = go.Figure()

    if plot_choice == "Compartment Dynamics":
        for name, data in compartments.items():
            fig.add_trace(go.Scatter(x=days, y=data, mode='lines', name=name))
        fig.update_layout(
            title=f"{model_choice} Model Simulation",
            xaxis_title="Days",
            yaxis_title="Population"
        )

    elif plot_choice == "Specific Compartment":
        selected_compartment = st.selectbox("Select Compartment to Plot", list(compartments.keys()))
        fig.add_trace(go.Scatter(x=days, y=compartments[selected_compartment], mode='lines', name=selected_compartment))
        fig.update_layout(
            title=f"{selected_compartment} Over Time",
            xaxis_title="Days",
            yaxis_title="Population"
        )

    elif plot_choice == "Incidence":
        fig.add_trace(go.Scatter(x=days, y=incidence, mode='lines', name='Incidence'))
        fig.update_layout(
            title="Incidence Over Time",
            xaxis_title="Days",
            yaxis_title="New Infections"
        )

    elif plot_choice == "R₀ and R_eff" and model_choice in ["SIR", "SEIR"]:
        # Plot R₀ (constant) and R_eff (time-varying)
        fig.add_trace(go.Scatter(x=days, y=[r0]*len(days), mode='lines', name='R₀', line=dict(dash='dash')))
        fig.add_trace(go.Scatter(x=days, y=r_eff, mode='lines', name='R_eff'))
        fig.update_layout(
            title="Basic and Effective Reproduction Numbers",
            xaxis_title="Days",
            yaxis_title="Reproduction Number",
            hovermode="x",
            legend_title="Metrics"
        )
        st.write(f"Initial R₀ value: {r0:.2f}")

    fig.update_layout(hovermode="x", legend_title="Compartments")
    st.plotly_chart(fig, use_container_width=True)