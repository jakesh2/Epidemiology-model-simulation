import streamlit as st
from plotting import update_plot
import pandas as pd

def update_summary_table(values):
    summary_df = pd.DataFrame(list(values.items()), columns=["Parameter", "Value"])
    return summary_df

def build_ui():
    params = {
        "Population": 1000,
        "Initial Infected": 10,
        "Infection Rate (beta)": 0.2,
        "Recovery Rate (gamma)": 0.1,
        "Natural Death Rate": 0.01,
        "Disease Death Rate": 0.05
    }

    st.sidebar.header("Parameters")
    params["Population"] = st.sidebar.number_input("Population", value=params["Population"], min_value=1)
    params["Initial Infected"] = st.sidebar.number_input("Initial Infected", value=params["Initial Infected"], min_value=0)
    params["Infection Rate (beta)"] = st.sidebar.slider("Infection Rate (beta)", 0.0, 1.0, params["Infection Rate (beta)"])
    params["Recovery Rate (gamma)"] = st.sidebar.slider("Recovery Rate (gamma)", 0.0, 1.0, params["Recovery Rate (gamma)"])
    params["Natural Death Rate"] = st.sidebar.slider("Natural Death Rate", 0.0, 0.1, params["Natural Death Rate"])
    params["Disease Death Rate"] = st.sidebar.slider("Disease Death Rate", 0.0, 0.1, params["Disease Death Rate"])

    col1, col2 = st.columns([1, 1.5])

    with col1:
        st.subheader("Summary Table")
        summary_df = update_summary_table(params)
        st.dataframe(summary_df, height=300)

    with col2:
        st.subheader("Graph")
        graph_type = st.selectbox("Select Graph Type", ["Line Chart", "Bar Chart", "Scatter Plot"])
        update_plot(
            params["Population"],
            params["Initial Infected"],
            params["Infection Rate (beta)"],
            params["Recovery Rate (gamma)"],
            params["Natural Death Rate"],
            params["Disease Death Rate"],
            graph_type
        )
