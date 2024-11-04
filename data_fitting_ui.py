# ui_components/data_fitting_ui.py
import streamlit as st
#from  matplotlib.pyplot import plot as plt
import pandas as pd
import plotly.graph_objects as go
from sir_model import sir_model
from seir_model import seir_model
from sis_model import sis_model
from generate_data import generate_synthetic_data, recommend_model
#from plotting import update_plot
import plotly.graph_objects as go
import streamlit as st

def update_plot(model_choice, params, return_data=False):
    """
    Updates the plot based on the selected epidemic model and parameters.
    Optionally returns compartment data without rendering the plot.

    Args:
        model_choice (str): The selected epidemic model (SIR, SEIR, SIS).
        params (dict): Parameters for the selected model.
        return_data (bool): If True, returns compartment data instead of rendering the plot.
    
    Returns:
        dict: Compartment data if return_data is True.
    """
    # Default parameter values
    print(params)
    population = params.get("Population", 1000)
    initial_infected = params.get("Initial Infected", 10)
    beta = params.get("beta", 0.3)
    gamma = params.get("gamma", 0.1)
    natural_death = params.get("Natural Death Rate", 0)
    disease_death = params.get("Disease Death Rate", 0)
    alpha = params.get("alpha", 0.1)

    # Initialize the model compartments based on the selected model
    if model_choice == "SIR":
        S, I, R = sir_model(
            population=population,
            initial_infected=initial_infected,
            beta=beta,
            gamma=gamma,
            natural_death=natural_death,
            disease_death=disease_death
        )
        compartments = {"Susceptible": S, "Infected": I, "Recovered": R}
    
    elif model_choice == "SEIR":
        S, E, I, R = seir_model(
            population=population,
            initial_infected=initial_infected,
            beta=beta,
            gamma=gamma,
            alpha=alpha,
            natural_death=natural_death,
            disease_death=disease_death
        )
        compartments = {"Susceptible": S, "Exposed": E, "Infected": I, "Recovered": R}
    
    elif model_choice == "SIS":
        S, I = sis_model(
            population=population,
            initial_infected=initial_infected,
            beta=beta,
            gamma=gamma,
            natural_death=natural_death
        )
        compartments = {"Susceptible": S, "Infected": I}
    
    # Return compartment data if requested
    if return_data:
        return compartments

    # Create and display the plot if return_data is False
    fig = go.Figure()
    days = list(range(len(next(iter(compartments.values())))))

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


def build_data_fitting_ui():
    st.sidebar.header("Data Selection")

    # Button to generate synthetic data
    if st.sidebar.button("Generate Synthetic Data"):
        synthetic_data, selected_model, true_values = generate_synthetic_data()
        st.session_state["synthetic_data"] = synthetic_data
        st.write(f"Synthetic data generated using {selected_model} model with parameters: {true_values}")
        st.dataframe(synthetic_data.head())

    # Download button for generated synthetic data
    if "synthetic_data" in st.session_state:
        st.sidebar.download_button(
            label="Download Synthetic Data",
            data=st.session_state["synthetic_data"].to_csv(index=False),
            file_name="synthetic_epidemic_data.csv",
            mime="text/csv"
        )

    # Choose between generated or uploaded data
    data_option = st.sidebar.radio("Data Source", ["Generated Data", "Upload Data"])
    if data_option == "Upload Data":
        uploaded_file = st.sidebar.file_uploader("Upload CSV file", type=["csv"])
        if uploaded_file:
            data = pd.read_csv(uploaded_file)
            st.write("Uploaded Data:")
            st.dataframe(data.head())
    else:
        if "synthetic_data" in st.session_state:
            data = st.session_state["synthetic_data"]
            st.write("Using generated data:")
            st.dataframe(data.head())
        else:
            st.write("No synthetic data. Please click 'Generate Synthetic Data'.")

    # Generate synthetic data
    data = generate_synthetic_data()[0]
    data, model_used, params = generate_synthetic_data()
    #print("Synthetic Data Generated:\n", data)
    print("True Model Used:", model_used)
    #print("True Parameters:", params)
    #print("\nRecommendation Results:")
    #print(recommend_model(data))

    # Perform model fitting and recommendation if data is available
    try:
        if data is not None:
            recommended_model, errors, params = recommend_model(data)

            # Display the recommended model
            st.subheader(f"Recommended Model: {recommended_model}")
            print(f"{recommended_model}")
            sir_beta,seir_beta,sis_beta=[params[model].get("beta", "N/A") for model  in errors.keys()]
            sir_gamma,seir_gamma,sis_gamma=[params[model].get("gamma", "N/A") for model in errors.keys()]
            sir_alpha,seir_gamma,sis_gamma=[params[model].get("alpha", "N/A") for model in errors.keys()]
            print(f'{sir_beta}')
            # Create a DataFrame to display errors and parameter
            results_data = {
                "Model": list(errors.keys()),
                "Mean Squared Error": list(errors.values()),
                "Beta": [params[model].get("beta", "N/A") for model in errors.keys()],
                "Gamma": [params[model].get("gamma", "N/A") for model in errors.keys()],
                "Alpha": [params[model].get("alpha", "N/A") for model in errors.keys()]
            }
            results_df = pd.DataFrame(results_data)
            st.table(results_df)

            # Use the recommended model to update the plot
            update_plot(recommended_model, params[recommended_model])

            # Plot each compartment with real data
            st.subheader("Compartment-Specific Comparisons")

            # Extract model results for each compartment
            compartments = update_plot(recommended_model, params[recommended_model], return_data=True)
            #print(model_data)
            days = list(range(len(next(iter(compartments.values())))))  # Days for x-axis

            # Iterate over each compartment and plot it with real data
            #model_data = model_data["Susceptible","Infected","Recovered"]
            for compartment, model_data in compartments.items():
                fig = go.Figure()

                # Plot the model-predicted data
                fig.add_trace(go.Scatter(x=days, y=model_data, mode='lines', name=f"Model {compartment}"))

                # Plot the real data if available
                
                #plt(x=days,y=)
                datab =pd.DataFrame({f"Model {compartment}":model_data})
                datab[f"actual {compartment}"] = data[compartment]
                #plt(datab)
                #plt.shoW()
                #print(datab.head(20))
                #print(compartment)
                #print(data[compartment])
                
                if compartment in data.columns:
                    fig.add_trace(go.Scatter(x=days, y=data[compartment], mode='markers', name=f"Real {compartment}"))

                # Update layout and display plot
                fig.update_layout(
                    title=f"{compartment} Comparison: Model vs Real Data",
                    xaxis_title="Days",
                    yaxis_title="Population",
                    hovermode="x",
                    legend_title="Data Source",
                )

                st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error("An error occurred while generating the recommendation.")
        st.write("Error details:", e)


