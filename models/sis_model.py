# models/sis_model.py
import numpy as np

def sis_model(population, initial_infected, beta, gamma, natural_death=0, days=160):
    susceptible = population - initial_infected
    infected = initial_infected

    S, I = [susceptible], [infected]

    for _ in range(days):
        new_infected = beta * susceptible * infected / population
        new_recovered = gamma * infected
        natural_deaths = natural_death * susceptible

        susceptible += new_recovered - new_infected - natural_deaths
        infected += new_infected - new_recovered

        S.append(susceptible)
        I.append(infected)

    return np.array(S), np.array(I)
