# app.py
import streamlit as st
from ui_components.simulation_ui import build_simulation_ui
from ui_components.data_fitting_ui import build_data_fitting_ui

# Mode selection toggle
def main():
    mode = st.sidebar.radio("Select Mode", ["Simulation", "Data Fitting"])
    
    if mode == "Simulation":
        st.title("Epidemic Model Simulation")
        build_simulation_ui()
    elif mode == "Data Fitting":
        st.title("Epidemic Model Data Fitting")
        build_data_fitting_ui()

if __name__ == "__main__":
    main()
