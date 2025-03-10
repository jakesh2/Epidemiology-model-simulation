# models/seir_model.py
import numpy as np
from scipy.integrate import odeint

def seir_model2(variables: list, t: list, params: list):
    '''
    SEIR model definition with vaccination and treatment.
    '''
    S, E, I, R = variables
    birth_rate, beta, alpha, gamma, mu, delta, v, tau = params
    N = S + E + I + R  # Total population
    
    # Force of infection
    lamda = beta * I / N  # The rate at which susceptible individuals become infected
    
    # Differential equations
    dS_dt = birth_rate * N - lamda * S - mu * S - v * S  # Births, infection, natural deaths, and vaccination
    dE_dt = lamda * S - (alpha + mu) * E  # Movement from exposed to infectious, and natural deaths
    dI_dt = alpha * E - (gamma + tau + mu + delta) * I  # Movement from infectious to recovered or disease-induced deaths, with treatment
    dR_dt = (gamma + tau) * I - mu * R + v * S  # Recovery, treatment, natural deaths, and vaccination
    
    return [dS_dt, dE_dt, dI_dt, dR_dt]

def calculate_r0(beta, alpha, gamma, mu, delta):
    """Calculate the basic reproduction number (R₀)"""
    return (beta * alpha) / ((alpha + mu) * (gamma + mu + delta))

def solve_model(S, E, I, R, beta, gamma, alpha, natural_death_rate=0, disease_death_rate=0, days=160, birth_rate=0.01, v=0, tau=0):
    '''
    Solving Model using dsolve and returning the population size at every point evaluated.
    '''
    mu = natural_death_rate
    delta = disease_death_rate
    t = np.linspace(0, days, days)
    y0 = [S, E, I, R]
    params = [birth_rate, beta, alpha, gamma, mu, delta, v, tau]
    
    # Solve the ODE
    y = odeint(seir_model2, y0, t, args=(params,))
    S_values = y[:, 0]
    E_values = y[:, 1]
    I_values = y[:, 2]
    R_values = y[:, 3]
    
    # Calculate R₀
    r0 = calculate_r0(beta, alpha, gamma, mu, delta)
    
    # Calculate R_eff over time (R₀ * S/N)
    N = S_values + E_values + I_values + R_values
    r_eff = r0 * (S_values / N)
    
    return S_values, E_values, I_values, R_values, r0, r_eff