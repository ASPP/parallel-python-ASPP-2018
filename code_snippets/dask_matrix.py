# Adapted from SciPy 2018 Dask Tutorial:
# https://github.com/martindurant/dask-tutorial-scipy-2018/

import numpy as np
import dask.array as da

# make a random collection of particles
def make_cluster(natoms, radius=40, seed=1981):
    np.random.seed(seed)
    cluster = np.random.normal(0, radius, (natoms,3))-0.5
    return cluster

# build the matrix of distances
def distances(cluster):
    diff = cluster[:, np.newaxis, :] - cluster[np.newaxis, :, :]
    mat = (diff*diff).sum(-1)
    return mat

cluster = make_cluster(int(7e3), radius=500)
print(distances(cluster))
