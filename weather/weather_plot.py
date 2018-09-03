import glob

import h5py
import numpy as np
import matplotlib.pyplot as plt

FILES = glob.glob('weather-big/*.hdf5')

for fname in FILES:
    with h5py.File(fname) as f:
        dset = f['t2m']
        plt.imshow(dset)
        plt.savefig(fname.replace('.hdf5', '.png'))
