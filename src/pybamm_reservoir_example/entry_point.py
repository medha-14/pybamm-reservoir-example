"""
This code is adopted from the PyBaMM project under the BSD-3-Clause

Copyright (c) 2018-2024, the PyBaMM team.
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of the copyright holder nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""


import importlib.metadata
import sys
import textwrap
from collections.abc import Mapping
from typing import Callable

class EntryPoint(Mapping):
    """
    Dict-like interface for accessing parameter sets and models through entry points in copier template.
    Access via :py:data:`pybamm_reservoir_example.parameter_sets` for parameter_sets
    Access via :py:data:`pybamm_reservoir_example.Model` for Models

    Examples
    --------
    Listing available parameter sets:
        >>> import pybamm_reservoir_example
        >>> list(pybamm_reservoir_example.parameter_sets)
        ['Chen2020', ...]
        >>> list(pybamm_reservoir_example.models)
        ['SPM', ...]

    Get the docstring for a parameter set/model:


        >>> print(pybamm_reservoir_example.parameter_sets.get_docstring("Ai2020"))
        <BLANKLINE>
        Parameters for the Enertech cell (Ai2020), from the papers :footcite:t:`Ai2019`,
        :footcite:t:`rieger2016new` and references therein.
        ...

        >>> print(pybamm_reservoir_example.models.get_docstring("SPM"))
        <BLANKLINE>
        Single Particle Model (SPM) model of a lithium-ion battery, from :footcite:t:`Marquis2019`. This class differs from the :class:`pybamm.lithium_ion.SPM` model class in that it shows the whole model in a single class. This comes at the cost of flexibility in combining different physical effects, and in general the main SPM class should be used instead.
        ...
        See also: :ref:`adding-parameter-sets`
    """

    _instances = 0
    def __init__(self, group):
        """Dict of entry points for parameter sets or models, lazily load entry points as"""
        if not hasattr(self, 'initialized'):    # Ensure __init__ is called once per instance
            self.initialized = True
            EntryPoint._instances += 1
            self._all_entries = dict()
            self.group = group
            for entry_point in self.get_entries(self.group):
                self._all_entries[entry_point.name] = entry_point

    @staticmethod
    def get_entries(group_name):
        """Wrapper for the importlib version logic"""
        if sys.version_info < (3, 10):  # pragma: no cover
            return importlib.metadata.entry_points()[group_name]
        else:
            return importlib.metadata.entry_points(group=group_name)

    def __new__(cls, group):
        """Ensure only two instances of entry points exist, one for parameter sets and the other for models"""
        if EntryPoint._instances < 2:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __getitem__(self, key) -> dict:
        return self._load_entry_point(key)()

    def _load_entry_point(self, key) -> Callable:
        """Check that ``key`` is a registered ``parameter_sets`` or ``models` ,
        and return the entry point for the parameter set/model, loading it needed."""
        if key not in self._all_entries:
            raise KeyError(f"Unknown parameter set or model: {key}")
        ps = self._all_entries[key]
        try:
            ps = self._all_entries[key] = ps.load()
        except AttributeError:
            pass
        return ps

    def __iter__(self):
        return self._all_entries.__iter__()

    def __len__(self) -> int:
        return len(self._all_entries)

    def get_docstring(self, key):
        """Return the docstring for the ``key`` parameter set or model"""
        return textwrap.dedent(self._load_entry_point(key).__doc__)

    def __getattribute__(self, name):
        try:
            return super().__getattribute__(name)
        except AttributeError as error:
              raise error

#: Singleton Instance of :class:ParameterSets """
parameter_sets = EntryPoint(group="pybamm_parameter_sets")

#: Singleton Instance of :class:ModelEntryPoints"""
models = EntryPoint(group="pybamm_models")

def Model(model:str):
    """
    Returns the loaded model object

    Parameters
    ----------
    model : str
        The model name or author name of the model mentioned at the model entry point.
    Returns
    -------
    pybamm.model
        Model object of the initialised model.
    Examples
    --------
    Listing available models:
        >>> import pybamm_reservoir_example
        >>> list(pybamm_reservoir_example.models)
        ['SPM', ...]
        >>> pybamm_reservoir_example.Model('Author/Year')
        <pybamm_reservoir_example.models.input.SPM.SPM object>
    """
    return models[model]
