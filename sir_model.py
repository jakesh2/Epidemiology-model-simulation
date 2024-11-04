# models/sir_model.py
import numpy as np

def sir_model(population, initial_infected, beta, gamma, natural_death=0, disease_death=0, days=160):
    susceptible = population - initial_infected
    infected = initial_infected
    recovered = 0

    S, I, R = [susceptible], [infected], [recovered]

    for _ in range(days):
        new_infected = beta * susceptible * infected / population
        new_recovered = gamma * infected
        natural_deaths = natural_death * susceptible
        disease_deaths = disease_death * infected

        susceptible -= new_infected + natural_deaths
        infected += new_infected - new_recovered - disease_deaths
        recovered += new_recovered

        S.append(susceptible)
        I.append(infected)
        R.append(recovered)

    return np.array(S), np.array(I), np.array(R)
