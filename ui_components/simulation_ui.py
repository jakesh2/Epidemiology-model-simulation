import streamlit as st
import pandas as pd
import numpy as np
from utils.plotting import update_plot
from model_descriptions.seir_description import seir_model_description
from model_descriptions.sir_model_description import sir_model_description
from model_descriptions.sis_model_description import sis_model_description
from models.sir_model import solve_model as sir_model
from models.seir_model import solve_model as seir_model
from models.sis_model import sis_model


def build_simulation_ui():
    model_params = {
        "SIR": {
            "Population": 1000,
            "Susceptible": 990,
            "Infected": 1,
            "Recovered": 0,
            "Infection Rate (beta)": 0.00001,
            "Recovery Rate (gamma)": 0.00001,
            "Natural Death Rate": 0.00001,
            "Disease Death Rate": 0.00005,
            "Vaccination Rate (v)": 0.00000,
            "Treatment Rate (tau)": 0.0,
            "Time in Days": 200
        },
        "SEIR": {
            "Population": 1000,
            "Susceptible": 990,
            "Exposed": 0,
            "Infected": 10,
            "Recovered": 0,
            "Recruitment Rate(Birth_rate)": 0.0,
            "Infection Rate (beta)": 0.00002,
            "Recovery Rate (gamma)": 0.00001,
            "Incubation Rate (alpha)": 0.00001,
            "Natural Death Rate": 0.00001,
            "Disease Death Rate": 0.00005,
            "Vaccination Rate (v)": 0.0,
            "Treatment Rate (tau)": 0.0,
            "Time in Days": 200
        },
        "SIS": {
            "Population": 1000,
            "Susceptible": 990,
            "Infected": 10,
            "Infection Rate (beta)": 0.00003,
            "Recovery Rate (gamma)": 0.00001,
            "Natural Death Rate": 0.00001,
            "Disease Death Rate": 0.00005,
            "Time in Days": 200
        },
    }

    # Sidebar for model selection
    st.sidebar.header("Model Selection")
    model_choice = st.sidebar.selectbox("Select Epidemic Model", list(model_params.keys()))
    
    # Set title for the selected model
    st.title(f"{model_choice} Model Simulation")

    # Radio button to switch between description and simulation
    view_option = st.radio("Choose View", ["Model Description", "Simulation & Plots"])

    if view_option == "Model Description":
        st.header("Model Description")
        if model_choice == "SEIR":
            # Import and display the SEIR model description
            description, equations, parameters, assumptions, reproduction_numbers = seir_model_description()
            st.markdown(description)
            st.markdown(assumptions)
            st.latex(equations)  # Render the aligned equations
            st.markdown(parameters)
            st.markdown(reproduction_numbers)

        elif model_choice == "SIR":
            # Import and display the SIR model description
            description, equations, parameters, reproduction_numbers,assumptions = sir_model_description()
            st.markdown(description)
            st.markdown(assumptions)
            st.latex(equations)  # Render the aligned equations
            st.markdown(parameters)
            st.markdown(reproduction_numbers)

        elif model_choice == "SIS":
            # Import and display the SIS model description
            description, equations, parameters, reproduction_numbers,assumptions = sis_model_description()
            st.markdown(description)
            st.markdown(assumptions)
            st.latex(equations)  # Render the aligned equations
            st.markdown(parameters)
            st.markdown(reproduction_numbers)

    else:
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
        params["Time in Days"] = st.sidebar.number_input("Time in Days", value=params["Time in Days"], min_value=1)

        # Dynamic Slider Settings for Infection and Recovery Rates
        def dynamic_slider(label, default_value, min_value=0.0, max_value=1.0, step_value=0.01):
            # Use session_state to store min, max, and step values
            if f"min_{label}" not in st.session_state:
                st.session_state[f"min_{label}"] = min_value
            if f"max_{label}" not in st.session_state:
                st.session_state[f"max_{label}"] = max_value
            if f"step_{label}" not in st.session_state:
                st.session_state[f"step_{label}"] = step_value

            # Display the slider with the current min, max, and step values
            slider_value = st.sidebar.slider(
                label,
                st.session_state[f"min_{label}"],
                st.session_state[f"max_{label}"],
                default_value,
                st.session_state[f"step_{label}"],
                key=f"slider_{label}"
            )

            # Use an expander for min, max, and step settings (collapsed by default)
            with st.sidebar.expander(f"⚙️ {label} Settings", expanded=False):
                col1, col2, col3 = st.columns(3)
                min_slider = col1.number_input(f"Min {label}", value=st.session_state[f"min_{label}"], format="%.6f", key=f"min_input_{label}")
                max_slider = col2.number_input(f"Max {label}", value=st.session_state[f"max_{label}"], format="%.6f", key=f"max_input_{label}")
                step_slider = col3.number_input(f"Step {label}", value=st.session_state[f"step_{label}"], min_value=0.0, format="%.6f", key=f"step_input_{label}")

                if min_slider >= max_slider:
                    st.warning(f"⚠️ Max value for {label} must be greater than min value")
                elif step_slider <= 0:
                    st.warning(f"⚠️ Step size for {label} must be greater than 0")
                else:
                    # Update session_state with new min, max, and step values
                    st.session_state[f"min_{label}"] = min_slider
                    st.session_state[f"max_{label}"] = max_slider
                    st.session_state[f"step_{label}"] = step_slider

            return slider_value

        # Apply dynamic sliders for parameters
        params["Infection Rate (beta)"] = dynamic_slider("Infection Rate (beta)", params["Infection Rate (beta)"])
        params["Recovery Rate (gamma)"] = dynamic_slider("Recovery Rate (gamma)", params["Recovery Rate (gamma)"])

        # Show additional parameters based on model choice
        if model_choice == "SEIR":
            params["Incubation Rate (alpha)"] = dynamic_slider("Incubation Rate (alpha)", params["Incubation Rate (alpha)"])
            params["Recruitment Rate(Birth_rate)"] = dynamic_slider("Recruitment Rate(Birth_rate)", params["Recruitment Rate(Birth_rate)"])
            params["Vaccination Rate (v)"] = dynamic_slider("Vaccination Rate (v)", params["Vaccination Rate (v)"])
            params["Treatment Rate (tau)"] = dynamic_slider("Treatment Rate (tau)", params["Treatment Rate (tau)"])

        if model_choice == "SIR":
            params["Vaccination Rate (v)"] = dynamic_slider("Vaccination Rate (v)", params["Vaccination Rate (v)"])
            params["Treatment Rate (tau)"] = dynamic_slider("Treatment Rate (tau)", params["Treatment Rate (tau)"])

        if "Natural Death Rate" in params:
            params["Natural Death Rate"] = dynamic_slider("Natural Death Rate", params["Natural Death Rate"])

        if "Disease Death Rate" in params:
            params["Disease Death Rate"] = dynamic_slider("Disease Death Rate", params["Disease Death Rate"], 0.0, 1.0, 1/100)
        
        # Display the graph
        st.subheader("Graph")
        update_plot(model_choice, params)

        # Display the summary table below the graph
        st.subheader("Summary Table")
        summary_df = pd.DataFrame(list(params.items()), columns=["Parameter", "Value"])
        st.dataframe(summary_df, height=300)

        # Sensitivity Analysis
        # Inside simulation_ui.py

        # Inside simulation_ui.py

        # Sensitivity Analysis
        st.sidebar.header("Sensitivity Analysis")
        param_to_vary = st.sidebar.selectbox("Select Parameter to Vary", list(params.keys()))
        param_range = st.sidebar.slider(f"Range for {param_to_vary}", 0.0, 1.0, (0.1, 0.9))

        # Run simulations for the selected parameter range
        sensitivity_results = []
        for value in np.linspace(param_range[0], param_range[1], 10):
            # Update the parameter value
            params[param_to_vary] = value

            # Call update_plot to simulate the model and get the results
            if model_choice == "SEIR":
                S, E, I, R, r0, r_eff = update_plot(model_choice, params, return_results=True)
                sensitivity_results.append((value, S[-1], I[-1], R[-1]))
            elif model_choice == "SIR":
                S, I, R, r0, r_eff = update_plot(model_choice, params, return_results=True)
                sensitivity_results.append((value, S[-1], I[-1], R[-1]))
            elif model_choice == "SIS":
                S, I = update_plot(model_choice, params, return_results=True)
                sensitivity_results.append((value, S[-1], I[-1]))

        # Display sensitivity results
        st.subheader("Sensitivity Analysis")
        sensitivity_df = pd.DataFrame(sensitivity_results, columns=["Parameter Value", "Final S", "Final I", "Final R"])
        st.dataframe(sensitivity_df)
    return model_choice