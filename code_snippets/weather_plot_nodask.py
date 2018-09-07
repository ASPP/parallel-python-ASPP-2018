import glob
import os

import h5py
import numpy as np
import matplotlib.pyplot as plt

import dask
import dask.multiprocessing

FILES = glob.glob('../data/weather-big/*.hdf5')

def read_temperature(fname):
    f = h5py.File(fname, 'r')
    dset = f['t2m']
    return dset

def plot_temperature(dset, fname):
    plt.imshow(dset)
    h = plt.savefig(fname)
    return h

for fname in FILES:
    dset = read_temperature(fname)
    plot_temperature(dset, os.path.basename(fname.replace('.hdf5', '.png')))
