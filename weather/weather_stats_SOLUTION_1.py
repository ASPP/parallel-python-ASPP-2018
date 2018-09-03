import glob
import multiprocessing

import h5py
import numpy as np
import matplotlib.pyplot as plt

def calc_max_val(fname):
    with h5py.File(fname) as f:
        dset = f['t2m']
        max_val = dset[...].max()
        min_val = dset[...].min()
    return max_val, min_val

FILES = glob.glob('weather-big/*.hdf5')

p = multiprocessing.Pool(4)
max_and_min = p.map(calc_max_val, FILES)

max_vals = [val[0] for val in max_and_min]
min_vals = [val[1] for val in max_and_min]

print("Maximum temperature for the dataset: {}".format(max(max_vals)))
print("Minimum temperature for the dataset: {}".format(min(min_vals)))
