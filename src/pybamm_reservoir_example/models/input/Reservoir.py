import pybamm


class Reservoir(pybamm.BaseModel):
    def __init__(self):
        super().__init__(name="Reservoir model")

        x_n = pybamm.Variable("Negative electrode stoichiometry")
        x_p = pybamm.Variable("Positive electrode stoichiometry")

        i = pybamm.FunctionParameter("Current function [A]", {"Time [s]": pybamm.t})
        x_n_0 = pybamm.Parameter("Initial negative electrode stoichiometry")
        x_p_0 = pybamm.Parameter("Initial positive electrode stoichiometry")
        U_p = pybamm.FunctionParameter("Positive electrode OCV", {"x_p": x_p})
        U_n = pybamm.FunctionParameter("Negative electrode OCV", {"x_n": x_n})
        Q_n = pybamm.Parameter("Negative electrode capacity [A.h]")
        Q_p = pybamm.Parameter("Positive electrode capacity [A.h]")
        R = pybamm.Parameter("Electrode resistance [Ohm]")
        
        self.rhs = {
            x_n: -i / Q_n,
            x_p: i / Q_p,
        }

        self.initial_conditions = {
            x_n: x_n_0,
            x_p: x_p_0,
        }

        self.variables = {
            "Negative electrode stoichiometry": x_n,
            "Positive electrode stoichiometry": x_p,
            "Voltage [V]": U_p - U_n - i * R,
        }

        self.events = [
            pybamm.Event("x_n ≤ 0", x_n - 0),
            pybamm.Event("x_n ≥ 1", 1 - x_n),
            pybamm.Event("x_p ≤ 0", x_p - 0),
            pybamm.Event("x_p ≥ 1", 1 - x_p),
        ]