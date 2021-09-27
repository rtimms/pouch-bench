#
# Combine a list of results into a single dictionary
#

import pickle

# new filename
new_filename = "new_file.pkl"

# files to combine
filenames = [
    "results1.pkl",
    "results2.pkl",
]

# dict to hold combined results
new_results = {}

# loop over files and update results
for filename in filenames:
    with open("data/" + filename, "rb") as handle:
        times_and_states = pickle.load(handle)

    new_results.update(times_and_states)

# pickle new (combined) results
with open("data/" + new_filename, "wb") as handle:
    pickle.dump(new_results, handle, protocol=pickle.HIGHEST_PROTOCOL)
