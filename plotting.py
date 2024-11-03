import plotly.graph_objects as go
from sir_model import sir_model
import streamlit as st

def update_plot(population, initial_infected, beta, gamma, natural_death, disease_death, graph_type):
    # Generate SIR model data
    S, I, R = sir_model(population, initial_infected, beta, gamma, natural_death, disease_death)
    days = list(range(len(S)))

    # Create an interactive plot with Plotly
    fig = go.Figure()

    # Add traces based on selected graph type
    if graph_type == "Line Chart":
        # Lines only, with markers shown only on hover
        fig.add_trace(go.Scatter(x=days, y=S, mode='lines', name='Susceptible', hoverinfo="x+y", line=dict(color='blue')))
        fig.add_trace(go.Scatter(x=days, y=I, mode='lines', name='Infected', hoverinfo="x+y", line=dict(color='red')))
        fig.add_trace(go.Scatter(x=days, y=R, mode='lines', name='Recovered', hoverinfo="x+y", line=dict(color='green')))
    elif graph_type == "Bar Chart":
        fig.add_trace(go.Bar(x=days, y=S, name='Susceptible', hoverinfo="x+y"))
        fig.add_trace(go.Bar(x=days, y=I, name='Infected', hoverinfo="x+y"))
        fig.add_trace(go.Bar(x=days, y=R, name='Recovered', hoverinfo="x+y"))
    elif graph_type == "Scatter Plot":
        fig.add_trace(go.Scatter(x=days, y=S, mode='markers', name='Susceptible', hoverinfo="x+y", marker=dict(color='blue')))
        fig.add_trace(go.Scatter(x=days, y=I, mode='markers', name='Infected', hoverinfo="x+y", marker=dict(color='red')))
        fig.add_trace(go.Scatter(x=days, y=R, mode='markers', name='Recovered', hoverinfo="x+y", marker=dict(color='green')))

    # Customize layout to make it responsive
    fig.update_layout(
        title="SIR Model with Death Rates",
        xaxis_title="Days",
        yaxis_title="Population",
        hovermode="x",  # Ensure hover shows values for all series at the same x value
        legend_title="Categories",
    )

    # Display the Plotly chart in Streamlit
    st.plotly_chart(fig, use_container_width=True)
