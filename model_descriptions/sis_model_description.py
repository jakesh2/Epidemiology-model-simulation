# model_descriptions/sis_model_description.py

def sis_model_description():
    """
    Returns the description of the SIS model as a Streamlit-compatible markdown and LaTeX.
    """
    description = """
    ### SIS Model Description
    The SIS model divides the population into two compartments:
    - **Susceptible (S)**: Individuals who can catch the disease.
    - **Infected (I)**: Individuals currently infected and capable of spreading the disease.

    ### Differential Equations:
    """
    equations = r"""
    \begin{align*}
    \frac{dS}{dt} &= \lambda \times N - \beta \frac{S I}{N} - \mu S + \gamma I \\
    \frac{dI}{dt} &= \beta \frac{S I}{N} - (\gamma + \mu + \delta) I
    \end{align*}
    """
    parameters = """
    ### Parameters:
    - $N$: Total population
    - $\\beta$: Transmission rate
    - $\gamma$: Recovery rate
    - $\mu$: Natural death rate
    - $\delta$: Disease-induced death rate
    """
    reproduction_numbers = """
    ### Reproduction Numbers:
    - **$R_0$**: Basic reproduction number, representing the average number of secondary infections produced by a single infected individual in a fully susceptible population.
    - **$R_{\text{eff}}$**: Effective reproduction number, representing the average number of secondary infections produced by a single infected individual in a population that is not fully susceptible.
    """
    return description, equations, parameters, reproduction_numbers