import glob

import dask.array as da
import h5py
import numpy as np

import dask


data_size = h5py.File('weather-big/2014-01-10.hdf5')['t2m'][...].shape

dsets = [h5py.File(fname) for fname in glob.glob('weather-big/*.hdf5')]

full_data = da.stack([da.from_array(dset['t2m'], chunks=data_size)[...] for dset in dsets])

min_val, max_val = dask.compute(
    full_data.min(),
    full_data.max(),
    scheduler='processes',
    num_workers=4)

print(min_val)
print(max_val)
print(full_data.min())

#print("Maximum temperature for the dataset: {}".format(max_val))
#print("Minimum temperature for the dataset: {}".format(min_val))
