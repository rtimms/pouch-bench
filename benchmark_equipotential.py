#
# Benchmark a "1+1D DFN" pouch cell model in PyBaMM
#
import pybamm
import pickle
import numpy as np
from models.dfn_pouch_model import DFNPouch

# filename to save times to
filename = "equipotential.pkl"

# number of finite volume in current colector domain (must be 1 or >2)
npts = [1, 3, 4, 8, 16, 32, 64, 128, 256, 512]

# number of repeated solves
repeats = 3


# setup -----------------------------------------------------------------------

# load 1+1D model (standard DFN)
dfn = pybamm.lithium_ion.DFN()

# load 1+1+1D model
dfn_pouch = DFNPouch()

# pick parameters
chemistry = pybamm.parameter_sets.Ecker2015
params = pybamm.ParameterValues(chemistry=chemistry)

# pick grid - 16 finite volumes per domain
var = pybamm.standard_spatial_vars
var_pts = {
    var.x_n: 16,
    var.x_s: 16,
    var.x_p: 16,
    var.r_n: 16,
    var.r_p: 16,
}

# pick solver
solver = pybamm.CasadiSolver(mode="fast", atol=1e-6, rtol=1e-6)


# solve models ----------------------------------------------------------------

# dict to hold times and states for each N
times_and_states = dict.fromkeys(npts)

for N in npts:

    # dict to hold times and states
    times_and_states[N] = {
        "states": np.nan,
        "setup times": [np.nan] * repeats,
        "solve times": [np.nan] * repeats,
        "integration times": [np.nan] * repeats,
    }

    # pick model
    if N == 1:
        model = dfn
    else:
        model = dfn_pouch

    # update grid
    var_pts[var.z] = N

    # set up and build simulation
    sim = pybamm.Simulation(
        model, parameter_values=params, var_pts=var_pts, solver=solver
    )
    sim.build()
    times_and_states[N][
        "states"
    ] = sim.built_model.concatenated_initial_conditions.shape[0]

    # solve simulation
    print(f"Solving 1+1+1D DFN with {N} coupled models...")
    for i in range(repeats):
        try:
            sol = sim.solve([0, 3600])  # 1hr 1C discharge
            times_and_states[N]["setup times"][i] = sol.set_up_time.value
            times_and_states[N]["solve times"][i] = sol.solve_time.value
            times_and_states[N]["integration times"][i] = sol.integration_time.value
            # print times
            print(
                f"Set-up time: {sol.set_up_time},",
                f"Solve time: {sol.solve_time} "
                + f"(of which integration time: {sol.integration_time}),",
                f"Total time: {sol.total_time}",
            )
        except pybamm.SolverError:
            print("Solver failed!")

    # take first setup time (this is a one off cost)
    times_and_states[N]["setup time"] = times_and_states[N]["setup times"][0]
    # compute average solve and integration times
    times_and_states[N]["average solve time"] = np.mean(
        times_and_states[N]["solve times"]
    )
    times_and_states[N]["average integration time"] = np.mean(
        times_and_states[N]["integration times"]
    )


# Pickle times and states dict ------------------------------------------------

with open("data/" + filename, "wb") as handle:
    pickle.dump(times_and_states, handle, protocol=pickle.HIGHEST_PROTOCOL)
