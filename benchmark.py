import pybamm
import pickle
import numpy as np


def bench_sim(model, pouch_model, solver, N, repeats):
    # pick model
    if N == 1:
        dfn = model
    else:
        dfn = pouch_model

    # pick parameters
    chemistry = pybamm.parameter_sets.Ecker2015
    params = pybamm.ParameterValues(chemistry=chemistry)

    # update grid
    var = pybamm.standard_spatial_vars
    var_pts = {
        var.x_n: 16,
        var.x_s: 16,
        var.x_p: 16,
        var.r_n: 16,
        var.r_p: 16,
        var.z: N,
    }

    # set up and build simulation
    sim = pybamm.Simulation(
        dfn, parameter_values=params, var_pts=var_pts, solver=solver
    )
    sim.build()

    # dict to hold times and states
    times_and_states = {
        "states": np.nan,
        "setup times": [np.nan] * repeats,
        "solve times": [np.nan] * repeats,
        "integration times": [np.nan] * repeats,
    }

    times_and_states["states"] = sim.built_model.concatenated_initial_conditions.shape[
        0
    ]

    # solve simulation
    print(f"Solving 1+1+1D DFN with {N} coupled models...")
    for i in range(repeats):
        try:
            sol = sim.solve([0, 3600])  # 1hr 1C discharge
            times_and_states["setup times"][i] = sol.set_up_time.value
            times_and_states["solve times"][i] = sol.solve_time.value
            times_and_states["integration times"][i] = sol.integration_time.value
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
    times_and_states["setup time"] = times_and_states["setup times"][0]
    # compute average solve and integration times
    times_and_states["average solve time"] = np.mean(times_and_states["solve times"])
    times_and_states["average integration time"] = np.mean(
        times_and_states["integration times"]
    )

    return times_and_states


def benchmark(
    model,
    pouch_model,
    solver,
    npts=[1, 4, 8, 16],
    repeats=3,
    filename="benchmark.pkl",
):
    """Benchmark the provided 1D and pouch models"""

    # dict to hold times and states for each N
    times_and_states = dict.fromkeys(npts)

    for N in npts:
        times_and_states[N] = bench_sim(model, pouch_model, solver, N, repeats)

    # pickle times and states dict
    with open("data/" + filename, "wb") as handle:
        pickle.dump(times_and_states, handle, protocol=pickle.HIGHEST_PROTOCOL)
