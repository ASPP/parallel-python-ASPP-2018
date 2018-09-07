import glob
import os

import h5py
import numpy as np
import matplotlib.pyplot as plt

FILES = glob.glob('../../data/weather-big/*.hdf5')

with h5py.File(FILES[0]) as f:
    data_size = f['t2m'][...].shape

mean_data = np.zeros(data_size)

for fname in FILES:
    with h5py.File(fname) as f:
        dset = f['t2m']
        mean_data += dset[...]

print(mean_data / len(FILES))

