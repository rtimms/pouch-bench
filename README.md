# 1+1+1D DFN benchmark
This repository contains code to benchmark 1+1+1D DFN pouch cell models in PyBaMM.

The benchmarking scripts uses the open-source battery modelling software [PyBaMM](https://github.com/pybamm-team/PyBaMM). To install the appropriate version of PyBaMM, run:
```
pip install -e git+https://github.com/pybamm-team/pybamm.git@develop#egg=pybamm
```

The repository contains 4 scripts that can be used to benchmarks different models:

- `benchmark_potential_pair.py` benchmarks a 1+1+1D "potential pair" model as described in [1, 2]. In this model the problem is split into a model for through-cell behaviour and a model for the transverse behaviour (here a 1D current collector). The through-cell behaviour is described by `N` coupled DFN models. We solve for the potential drop and temperature along the current collector, and the local potential difference provides the electrical boundary conditions for each of the DFN models. For the thermal problem we assume that the temperature is uniform across the thickness of the cell, but varies along the length on the current collector. We assume Newton cooling from all boundaries.
- `benchmark_isothermal_potential_pair.py` benchmarks an isothermal 1+1+1D "potential pair" model.
- `benchmark_equipotential_pair.py` benchmarks a similar problem in which the potential in each of the current collectors is uniform, so all of the DFN models see the same potential difference. We refer to this as a 1+1+1D "equipotential pair" model. The temperature can vary along the length of the current collector, and in this model we assume there is no surface cooling and that the temperature at either end of the current collector is fixed at 25&deg;C. We solve an equation to determine the current through each of the DFN models, ensuring charge is conserved.
- `benchmark_isothermal_potential_pair.py` benchmarks an isothermal 1+1+1D "equipotential pair" model.

To benchmark the models we solve them with an increasing number of coupled through-cell models. In each of the scripts you can provide a `filename` where the solve times will be stored as a pickled python dictionary, a list `npts` which is a list of the number of coupled DFN models (and corresponds directly to the number of finite volumes used to discretise the current collector domain), and an integer `repeats` which is the number of times to repeatedly call `solve` to collect timing statistics. The scripts create and solve simulations using each of the values in `npts` and store the following times:

- `setup time`. This is a one-off cost associated with setting up the solver on the first call to `solve`. Subsequent calls to `solve` have a `setup time` of effectively zero (on the order of microseconds).
- `integration time`. This is the time spent actually doing the numerical integration.
- `solve time`. This is the time spend in the call to `solve` and includes some overheads. This time includes the overheads and the `integration_time`.

The jupyter notebook `plots.ipynb` creates some plots using the results available in the repository. You can edit this to create your own plots or view the times in the dictionary directly. The script `combine_results` can be used to combine pickled dictionaries for easier manipulation.

## References

[1] R. Timms, S.G. Marquis, V. Sulzer, C.P. Please, S.J. Chapman, Asymptotic reduction of a lithium-ion pouch cell model, SIAM Journal on Applied Mathematics, 2021.
[2] S.G. Marquis, R. Timms, V. Sulzer, C.P. Please, S.J. Chapman, A suite of reduced-order models of a single-layer lithium-ion pouch cell, Journal of the Electrochemical Society, 2020.
