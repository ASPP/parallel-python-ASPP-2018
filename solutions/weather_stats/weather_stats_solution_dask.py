import glob

import h5py
import numpy as np

import dask.array as da

FILES = glob.glob('../../data/weather-big/*.hdf5')

with h5py.File(FILES[0]) as f:
    data_size = f['t2m'][...].shape


dsets = [h5py.File(fname) for fname in FILES]

all_data = da.stack(
    [da.from_array(dset['t2m'], chunks=(500,500)) for dset in dsets])

print(all_data.mean(axis=0).compute())
