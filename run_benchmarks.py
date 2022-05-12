#
# Benchmark a "1+1+1D DFN" pouch cell model in PyBaMM
#
import pybamm
from benchmark import benchmark

# choose thermal option "isothermal" or "x-lumped"
thermal_option = "isothermal"
# thermal_option = "x-lumped"

# load 1+1D model (standard DFN)
model = pybamm.lithium_ion.DFN(
    options={
        "cell geometry": "pouch",
        "thermal": thermal_option,
    },
    name="1+1D DFN",
)

# load 1+1+1D model
pouch_model = pybamm.lithium_ion.DFN(
    options={
        "cell geometry": "pouch",
        "current collector": "potential pair",
        "dimensionality": 1,
        "thermal": thermal_option,
    },
    name="1+1+1D DFN",
)

# solver
solver = pybamm.IDAKLUSolver(atol=1e-6, rtol=1e-6)
# solver = pybamm.CasadiSolver(mode="fast with events", atol=1e-6, rtol=1e-6)

# number of finite volumes in current colector domain (must be 1 or >2)
npts = [1, 3, 4, 8, 16, 32, 64, 128]

# number of repeated solves
repeats = 1

# file to save times to
filename = "isothermal_idaklu.pkl"

# benchmark
benchmark(model, pouch_model, solver, npts, repeats, filename)
