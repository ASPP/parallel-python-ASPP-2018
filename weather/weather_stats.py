import glob

import h5py
import numpy as np

FILES = glob.glob('weather-big/*.hdf5')

max_vals = []
min_vals = []

for fname in FILES:
    with h5py.File(fname) as f:
        dset = f['t2m']
        max_vals.append(dset[...].max())
        min_vals.append(dset[...].min())

print("Maximum temperature for the dataset: {}".format(max(max_vals)))
print("Minimum temperature for the dataset: {}".format(min(min_vals)))
