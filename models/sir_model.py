# models/sir_model.py
import numpy as np
from scipy.integrate import odeint

def sir_model(variables, t, params):
    '''
    SIR model definition with vaccination and treatment.
    '''
    S, I, R = variables
    birth_rate, beta, gamma, mu, delta, v, tau = params
    N = S + I + R  # Total population
    
    # Force of infection
    lamda = beta * I / N  # The rate at which susceptible individuals become infected
    
    # Differential equations
    dS_dt = birth_rate * N - lamda * S - mu * S - v * S  # Births, infection, natural deaths, and vaccination
    dI_dt = lamda * S - (gamma + tau + mu + delta) * I  # Movement from infectious to recovered or disease-induced deaths, with treatment
    dR_dt = (gamma + tau) * I - mu * R + v * S  # Recovery, treatment, natural deaths, and vaccination
    
    return [dS_dt, dI_dt, dR_dt]

def calculate_r0(beta, gamma, mu, delta,tau):
    """Calculate the basic reproduction number (R₀)"""
    return beta / (gamma + mu + delta + tau)

def solve_model(S, I, R, beta, gamma, natural_death_rate=0, disease_death_rate=0, days=160, birth_rate=0.01, v=0, tau=0):
    '''
    Solving Model using dsolve and returning the population size at every point evaluated.
    '''
    mu = natural_death_rate
    delta = disease_death_rate
    t = np.linspace(0, days, days)
    y0 = [S, I, R]
    params = [birth_rate, beta, gamma, mu, delta, v, tau]
    
    # Solve the ODE
    y = odeint(sir_model, y0, t, args=(params,))
    S_values = y[:, 0]
    I_values = y[:, 1]
    R_values = y[:, 2]
    
    # Calculate R₀
    r0 = calculate_r0(beta, gamma, mu, delta,tau)
    
    # Calculate R_eff over time (R₀ * S/N)
    N = S_values + I_values + R_values
    r_eff = r0 * (S_values / N)
    
    return S_values, I_values, R_values, r0, r_eff