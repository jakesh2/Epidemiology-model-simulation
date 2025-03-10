# generate_data.py
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
from sklearn.metrics import mean_squared_error
import random
from models.sir_model import sir_model
from models.seir_model import solve_model as seir_model
from models.sis_model import sis_model

def generate_synthetic_data():
    """
    Generates synthetic epidemic data using a randomly chosen model (SIR, SEIR, or SIS) 
    with random parameter values.
    
    Returns:
        data (DataFrame): The generated synthetic data as a DataFrame.
        selected_model (str): The model that was used to generate the data.
        true_params (dict): The actual parameters used for data generation.
    """
    # Randomly select a model
    selected_model = random.choice(["SIR", "SEIR", "SIS"])

    # Randomize model parameters
    beta = round(random.uniform(0.1, 0.5), 2)    # Infection rate
    gamma = round(random.uniform(0.05, 0.2), 2)  # Recovery rate
    alpha = round(random.uniform(0.1, 0.3), 2)   # Incubation rate for SEIR model
    population = 1000
    initial_infected = 10
    days = 50

    # Print statements for debugging
    print("Debugging Info: Synthetic Data Generation")
    print(f"Selected Model: {selected_model}")
    print(f"Parameters - beta: {beta}, gamma: {gamma}, alpha: {alpha if selected_model == 'SEIR' else 'N/A'}")
    print(f"Population: {population}, Initial Infected: {initial_infected}, Days: {days}\n")


    # Generate data based on the selected model
    if selected_model == "SIR":
        susceptible, infected, recovered = population - initial_infected, initial_infected, 0
        S, I, R = [susceptible], [infected], [recovered]
        
        for _ in range(days):
            new_infected = beta * susceptible * infected / population
            new_recovered = gamma * infected
            susceptible -= new_infected
            infected += new_infected - new_recovered
            recovered += new_recovered
            S.append(susceptible)
            I.append(infected)
            R.append(recovered)
        
        data = pd.DataFrame({"Days": range(days + 1), "Susceptible": S, "Infected": I, "Recovered": R})

    elif selected_model == "SEIR":
        susceptible, exposed, infected, recovered = population - initial_infected, 0, initial_infected, 0
        S, E, I, R = [susceptible], [exposed], [infected], [recovered]
        
        for _ in range(days):
            new_exposed = beta * susceptible * infected / population
            new_infected = alpha * exposed
            new_recovered = gamma * infected
            susceptible -= new_exposed
            exposed += new_exposed - new_infected
            infected += new_infected - new_recovered
            recovered += new_recovered
            S.append(susceptible)
            E.append(exposed)
            I.append(infected)
            R.append(recovered)
        
        data = pd.DataFrame({"Days": range(days + 1), "Susceptible": S, "Exposed": E, "Infected": I, "Recovered": R})

    elif selected_model == "SIS":
        susceptible, infected = population - initial_infected, initial_infected
        S, I = [susceptible], [infected]
        
        for _ in range(days):
            new_infected = beta * susceptible * infected / population
            new_recovered = gamma * infected
            susceptible += new_recovered - new_infected
            infected += new_infected - new_recovered
            S.append(susceptible)
            I.append(infected)
        
        data = pd.DataFrame({"Days": range(days + 1), "Susceptible": S, "Infected": I})

    # Round values for realism and return
    data = data.round(2)
    true_params = {"beta": beta, "gamma": gamma, "alpha": alpha if selected_model == "SEIR" else None}
    print(data)
    return data, selected_model, true_params

def recommend_model(data):
    """
    Fits SIR, SEIR, and SIS models to the given data, calculates the mean squared error for each,
    and recommends the best-fitting model based on the lowest error.
    
    Args:
        data (DataFrame): The epidemic data to fit models on, with 'Days' and 'Infected' columns.

    Returns:
        recommended_model (str): The name of the model with the best fit.
        errors (dict): Mean squared errors for each model.
        fitted_params (dict): Best-fit parameters for each model.
    """
    days = data["Days"].values
    infected_data = data["Infected"].values
    errors = {}
    fitted_params = {}

    # SIR Model Fitting
    def sir_equations(t, beta, gamma):
        _, I, _ = sir_model(1000, 10, beta, gamma, days=len(t))
        return I
    sir_popt, _ = curve_fit(sir_equations, days, infected_data, p0=[0.3, 0.1])
    sir_predictions = sir_equations(days, *sir_popt)
    errors["SIR"] = mean_squared_error(infected_data, sir_predictions)
    fitted_params["SIR"] = {"beta": sir_popt[0], "gamma": sir_popt[1]}

    # SEIR Model Fitting
    def seir_equations(t, beta, gamma, alpha):
        _, _, I, _ = seir_model(1000, 10, beta, gamma, alpha, days=len(t))
        return I
    seir_popt, _ = curve_fit(seir_equations, days, infected_data, p0=[0.3, 0.1, 0.2])
    seir_predictions = seir_equations(days, *seir_popt)
    errors["SEIR"] = mean_squared_error(infected_data, seir_predictions)
    fitted_params["SEIR"] = {"beta": seir_popt[0], "gamma": seir_popt[1], "alpha": seir_popt[2]}

    # SIS Model Fitting
    def sis_equations(t, beta, gamma):
        _, I = sis_model(1000, 10, beta, gamma, days=len(t))
        return I
    sis_popt, _ = curve_fit(sis_equations, days, infected_data, p0=[0.3, 0.1])
    sis_predictions = sis_equations(days, *sis_popt)
    errors["SIS"] = mean_squared_error(infected_data, sis_predictions)
    fitted_params["SIS"] = {"beta": sis_popt[0], "gamma": sis_popt[1]}

    # Recommend the model with the lowest mean squared error
    recommended_model = min(errors, key=errors.get)
    return recommended_model, errors, fitted_params
#generate_synthetic_data()