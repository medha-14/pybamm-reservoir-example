"""
Copyright (c) 2025 medha-14. All rights reserved.

pybamm-reservoir-example: A battery modelling project to demonstrate the pybamm.Model() API for external models and parameter sets.
"""
from importlib.metadata import version

__version__ = version("pybamm-reservoir-example")

import pybamm
from pybamm_reservoir_example.entry_point import Model, parameter_sets, models

__all__ = [
    "__version__",
    "pybamm",
    "parameter_sets",
    "Model",
    "models",
]
