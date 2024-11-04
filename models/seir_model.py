# models/seir_model.py
import numpy as np

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
