# models/seir_model.py
import numpy as np
from scipy.integrate import odeint

def seir_model(population, initial_infected, beta, gamma, alpha, natural_death=0, disease_death=0, days=160):
    susceptible = population - initial_infected
    exposed = 0
    infected = initial_infected
    recovered = 0

    S, E, I, R = [susceptible], [exposed], [infected], [recovered]

    for _ in range(days):
        new_exposed = beta * susceptible * infected / population
        new_infected = alpha * exposed
        new_recovered = gamma * infected
        natural_deaths = natural_death * susceptible
        disease_deaths = disease_death * infected

        susceptible -= new_exposed + natural_deaths
        exposed += new_exposed - new_infected
        infected += new_infected - new_recovered - disease_deaths
        recovered += new_recovered

        S.append(susceptible)
        E.append(exposed)
        I.append(infected)
        R.append(recovered)

    return np.array(S), np.array(E), np.array(I), np.array(R)

# SEIR differential equations
def seir_model2(variables:list, t:list, params:list):
    '''
    SEIR model definition
    These include all the differential equations and returns the List of Population size
    in each compartment
    
    parameter
    
    variables : List - all variables in the model in this case [S,E,I,R] defined at inital time point
    t: List -time points to be evaluated
    params: -all the values of the parameters defined in the differential equations'''
    S, E, I, R = variables
    birth_rate, beta, alpha, gamma, mu, delta = params
    N = S + E + I + R  # Total population
    
    # Force of infection
    lamda = beta * I / N  # The rate at which susceptible individuals become infected
    
    # Differential equations
    dS_dt = birth_rate * N - lamda * S - mu * S  # Births, infection, and natural deaths
    dE_dt = lamda * S - (alpha + mu) * E  # Movement from exposed to infectious, and natural deaths
    dI_dt = alpha * E - (gamma + mu + delta) * I  # Movement from infectious to recovered or disease-induced deaths
    dR_dt = gamma * I - mu * R  # Recovery and natural deaths
    
    return [dS_dt, dE_dt, dI_dt, dR_dt]

"""def solve_R0():
    '''
    Returns R0 of the Model'''
    return (beta*birth_rate*alpha)/(mu*(alpha+mu)*(gamma+mu+delta))"""



def solve_model(S,E,I,R,beta, gamma, alpha, natural_death_rate=0, disease_death_rate=0, days=160,birth_rate=0.01):
    '''
    Solving Model using dsolve and returning the population size at every point evaluated
    
    parameters
    
    model :  the SIER model to be solved
    y0    :  inital conditions of population
    t     :  time points to be evaluated
    params:  parameters of the model
    birth_rate = 1/10000  # Birth rate: 1 new individual per 10,000 people per day
    beta = 6/10  # Infection rate: 60% of contacts between susceptible and infected lead to infection
    alpha = 1/3  # Incubation rate: 1/3 means an incubation period of 3 days
    gamma = 1/15  # Recovery rate: 1/15 means the infectious period lasts for 15 days on average
    mu = 1/(66*365)  # Natural death rate: Based on an average lifespan of 66 years
    delta = 1/100  # Disease-induced death rate: 1% of infected people die from the disease per day
    initial conditions: S= Susceptible, E = Exposed, I = Infectious, R = Recovered
    
    
    S  # Initial susceptible population
    E  # Initial exposed population (already infected but not yet infectious)
    I   # Initial infectious population
    R  # Initial recovered population'''
    mu = natural_death_rate
    delta = disease_death_rate
    t = np.linspace(0, days, days)
    #t = days
    y0 = [S, E, I, R]
    params = [birth_rate, beta, alpha, gamma, mu, delta]

    
    # Solve the ODE
    y = odeint(seir_model2, y0, t, args=(params,))
    #y : results from a solved SEIR model
    S_values = y[:,0]
    E_values = y[:,1]
    I_values = y[:,2]
    R_values = y[:,3]
    return S_values,E_values,I_values,R_values
#s,e,i,r = solve_model(1000,1,2,0,0.1,0.2,0.1,0,0,20,0)
#print(type(s))