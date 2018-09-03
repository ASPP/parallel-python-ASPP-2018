import glob
import multiprocessing

import h5py
import numpy as np
import matplotlib.pyplot as plt

def plot_weather_data(fname):
    with h5py.File(fname) as f:
        dset = f['t2m']
        plt.imshow(dset)
        plt.savefig(fname.replace('.hdf5', '.png'))

FILES = glob.glob('weather-big/*.hdf5')

p = multiprocessing.Pool(4)
p.map(plot_weather_data, FILES)
