import numpy as np
import pybamm

# OCV functions from Chen2020 (as in your original code)
def graphite_LGM50_ocp_Chen2020(sto):
    return (
        1.9793 * np.exp(-39.3631 * sto)
        + 0.2482
        - 0.0909 * np.tanh(29.8538 * (sto - 0.1234))
        - 0.04478 * np.tanh(14.9159 * (sto - 0.2769))
        - 0.0205 * np.tanh(30.4444 * (sto - 0.6103))
    )

def nmc_LGM50_ocp_Chen2020(sto):
    return (
        -0.8090 * sto
        + 4.4875
        - 0.0428 * np.tanh(18.5138 * (sto - 0.5542))
        - 17.7326 * np.tanh(15.7890 * (sto - 0.3117))
        + 17.5842 * np.tanh(15.9308 * (sto - 0.3120))
    )

# Reservoir-model parameter set, using dictionary-style get_parameter_values
def get_parameter_values():
    return {
        "chemistry": "lithium_ion",
        # Function parameters
        "Current function [A]": lambda t: 1 + 0.5 * pybamm.sin(100 * t),
        "Positive electrode OCV": nmc_LGM50_ocp_Chen2020,
        "Negative electrode OCV": graphite_LGM50_ocp_Chen2020,
        # Initial conditions for x_n and x_p
        "Initial negative electrode stoichiometry": 0.9,
        "Initial positive electrode stoichiometry": 0.1,
        # Capacities and resistance
        "Negative electrode capacity [A.h]": 1.0,
        "Positive electrode capacity [A.h]": 1.0,
        "Electrode resistance [Ohm]": 0.1,
 
      "notcite": ["ReservoirParameters"],  
      }