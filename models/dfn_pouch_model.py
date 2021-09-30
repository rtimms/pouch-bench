import pybamm
from .current_collector_submodel import EquipotentialPair
from .electrode_submodel import FullPotentiostatic
from .thermal_submodel import HeatEquation1D


class DFNPouch(pybamm.lithium_ion.DFN):
    def __init__(self, options=None, name="1+1+1D DFN", build=True):
        options = {
            "dimensionality": 1,
        }
        super().__init__(options=options, name=name)

    def set_current_collector_submodel(self):
        self.submodels["current collector"] = EquipotentialPair(self.param)

    def set_solid_submodel(self):
        self.submodels["negative electrode potential"] = FullPotentiostatic(
            self.param, "Negative", self.options
        )
        self.submodels["positive electrode potential"] = FullPotentiostatic(
            self.param, "Positive", self.options
        )

    def set_thermal_submodel(self):
        self.submodels["thermal"] = HeatEquation1D(self.param)


class IsothermalDFNPouch(pybamm.lithium_ion.DFN):
    def __init__(self, options=None, name="1+1+1D DFN", build=True):
        options = {
            "dimensionality": 1,
        }
        super().__init__(options=options, name=name)

    def set_current_collector_submodel(self):
        self.submodels["current collector"] = EquipotentialPair(self.param)

    def set_solid_submodel(self):
        self.submodels["negative electrode potential"] = FullPotentiostatic(
            self.param, "Negative", self.options
        )
        self.submodels["positive electrode potential"] = FullPotentiostatic(
            self.param, "Positive", self.options
        )

    def set_thermal_submodel(self):
        self.submodels["thermal"] = pybamm.thermal.isothermal.Isothermal(
            self.param, self.options
        )
