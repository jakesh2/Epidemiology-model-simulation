# model_descriptions/sir_model_description.py

def sir_model_description():
    """
    Returns the description of the SIR model as a Streamlit-compatible markdown and LaTeX.
    """
    description = """
    ### SIR Model Description
    The SIR model divides the population into three compartments:
    - **Susceptible (S)**: Individuals who can catch the disease.
    - **Infected (I)**: Individuals currently infected and capable of spreading the disease.
    - **Recovered (R)**: Individuals who have recovered and gained lifelong immunity.

    ### Differential Equations:
    """
    equations = r"""
    \begin{align*}
    \frac{dS}{dt} &= \lambda N - \beta \frac{S I}{N} - \mu S - v S \\
    \frac{dI}{dt} &= \beta \frac{S I}{N} - (\gamma + \tau + \mu + \delta) I \\
    \frac{dR}{dt} &= (\gamma + \tau) I - \mu R + v S
    \end{align*}
    """
    parameters = """
    ### Parameters:
    - $N$: Total population
    - $\\beta$: Transmission rate
    - $\gamma$: Recovery rate
    - $\mu$: Natural death rate
    - $\delta$: Disease-induced death rate
    - $v$: Vaccination rate
    - $\\tau$: Treatment rate
    """
    reproduction_numbers = """
    ### Reproduction Numbers:
    - **$R_0$**: Basic reproduction number, representing the average number of secondary infections produced by a single infected individual in a fully susceptible population.
    - **$R_{\text{eff}}$**: Effective reproduction number, representing the average number of secondary infections produced by a single infected individual in a population that is not fully susceptible.
    """
    return description, equations, parameters, reproduction_numbers