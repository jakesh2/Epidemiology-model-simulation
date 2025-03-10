# model_descriptions/seir_model_description.py

def seir_model_description():
    """
    Returns the description of the SEIR model as a Streamlit-compatible markdown and LaTeX.
    """
    description = """
    ### SEIR Model Description
    The SEIR model divides the population into four compartments:
    - **Susceptible (S)**: Individuals who can catch the disease.
    - **Exposed (E)**: Individuals who are infected but not yet infectious.
    - **Infected (I)**: Individuals who are currently infectious.
    - **Recovered (R)**: Individuals who have recovered and gained immunity.

    """
    equations = r"""
    \begin{align*}
    \frac{dS}{dt} &= \lambda N - \beta \frac{S I}{N} - \mu S - v S \\
    \frac{dE}{dt} &= \beta \frac{S I}{N} - (\alpha + \mu) E \\
    \frac{dI}{dt} &= \alpha E - (\gamma + \tau + \mu + \delta) I \\
    \frac{dR}{dt} &= (\gamma + \tau) I - \mu R + v S
    \end{align*}
    """
    parameters = """
    ### Parameters:
    - $N$: Total population
    - $\\beta$: Transmission rate
    - $\\alpha$: Incubation rate
    - $\gamma$: Recovery rate
    - $\mu$: Natural death rate
    - $\delta$: Disease-induced death rate
    - $v$: Vaccination rate
    - $\\tau$: Treatment rate
    """
    assumptions = r"""
    ### Assumptions:
    - The population is closed (no migration).
    - The disease confers lifelong immunity upon recovery.
    - The incubation period is finite (exposed individuals eventually become infectious).
    - The population is well-mixed (no spatial structure).
    - The transmission rate ($\beta$), incubation rate ($\alpha$), recovery rate ($\gamma$), and death rates ($\mu$, $\delta$) are constant over time.
    - Vaccination ($v$) and treatment ($\tau$) are applied uniformly across the population.
    - Exposed individuals ($E$) are not infectious.
    
    ### Differential Equations:
    """
    reproduction_numbers = """
    ### Reproduction Numbers:
    - **$R_0$**: Basic reproduction number, representing the average number of secondary infections produced by a single infected individual in a fully susceptible population.
    - **$R_{\\text{eff}}$**: Effective reproduction number, representing the average number of secondary infections produced by a single infected individual in a population that is not fully susceptible.
    """
    return description, equations, parameters,assumptions, reproduction_numbers