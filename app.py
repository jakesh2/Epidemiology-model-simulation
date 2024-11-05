# app.py
import streamlit as st
import streamlit.components.v1 as components
from simulation_ui import build_simulation_ui
from data_fitting_ui import build_data_fitting_ui

# Mode selection toggle
def main():
    mode = st.sidebar.radio("Select Mode", ["Simulation", "Data Fitting"])
    components.html("""
    <head>
    <meta name="google-site-verification"
    content="uEdoedTxFYR7r8POe7yYULtC7y97ghmJjwew6XbpiUw" />
    </head>
    """,height=0)
    if mode == "Simulation":
        st.title("Epidemic Model Simulation")
        build_simulation_ui()
    elif mode == "Data Fitting":
        st.title("Epidemic Model Data Fitting")
        build_data_fitting_ui()

if __name__ == "__main__":
    main()
