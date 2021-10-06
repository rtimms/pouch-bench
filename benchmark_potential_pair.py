#
# Benchmark a "1+1+1D DFN" potential pair pouch cell model in PyBaMM
#

import pybamm
from benchmark import benchmark

# file to save times to
filename = "potential_pair.pkl"

# number of finite volumes in current colector domain (must be 1 or >2)
npts = [1, 3, 4, 8, 16, 32, 64, 128]

# number of repeated solves
repeats = 3

# load 1+1D model (standard DFN)
dfn = pybamm.lithium_ion.DFN(
    options={
        "thermal": "lumped",
    },
    name="1+1D DFN",
)

# load 1+1+1D model
dfn_pouch = pybamm.lithium_ion.DFN(
    options={
        "current collector": "potential pair",
        "dimensionality": 1,
        "thermal": "x-lumped",
    },
    name="1+1+1D DFN",
)

# benchmark
benchmark(dfn, dfn_pouch, filename, npts, repeats)
