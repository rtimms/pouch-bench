#
# Benchmark a "1+1+1D DFN" equipotential pair pouch cell model in PyBaMM
#
import pybamm
from models.dfn_pouch_model import IsothermalDFNPouch
from benchmark import benchmark

# file to save times to
filename = "isothermal_equipotential_pair.pkl"

# number of finite volumes in current colector domain (must be 1 or >2)
npts = [1, 3, 4, 8, 16, 32, 64, 128]

# number of repeated solves
repeats = 3

# load 1+1D model (standard DFN)
dfn = pybamm.lithium_ion.DFN(name="1+1D DFN")

# load 1+1+1D model
dfn_pouch = IsothermalDFNPouch()

# benchmark
benchmark(dfn, dfn_pouch, filename, npts, repeats)
