# ui_components/data_fitting_ui.py
import streamlit as st
import pandas as pd
from utils.generate_data import generate_synthetic_data, recommend_model

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
        # Use generated data if available
        if "synthetic_data" in st.session_state:
            data = st.session_state["synthetic_data"]
            st.write("Using generated data:")
            st.dataframe(data.head())
        else:
            st.write("No synthetic data. Please click 'Generate Synthetic Data'.")
            

    # Perform model fitting and recommendation if data is available
    try:
        if "data" in locals():
            recommended_model, errors, params = recommend_model(data)
            st.write(f"Recommended Model: {recommended_model}")
            st.write("Fit Errors (Mean Squared Error):", errors)
            st.write("Estimated Parameters:", params[recommended_model])
    except:
        st.write("Recommended Model")
        st.write("Please take Note that i haven't completed the logic on this part yet")
        
