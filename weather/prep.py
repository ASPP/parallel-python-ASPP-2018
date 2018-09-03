import os
import numpy as np
import pandas as pd
from glob import glob
import tarfile
import urllib.request
import zipfile

here = os.path.dirname(__file__)

data_dir = here

def create_weather(growth=16):
    filenames = sorted(glob(os.path.join(data_dir, 'weather-small', '*.hdf5')))

    if not filenames:
        ws_dir = os.path.join(data_dir, 'weather-small')
        raise ValueError('Did not find any hdf5 files in {}'.format(ws_dir))

    if not os.path.exists(os.path.join(data_dir, 'weather-big')):
        os.mkdir(os.path.join(data_dir, 'weather-big'))

    if all(os.path.exists(fn.replace('small', 'big')) for fn in filenames):
        return

    from skimage.transform import resize
    import h5py

    print('Exploding weather data')
    for fn in filenames:
        with h5py.File(fn, mode='r') as f:
            x = f['/t2m'][:]

        y = resize(x, (x.shape[0] * growth, x.shape[1] * growth), mode='constant')

        out_fn = os.path.join(data_dir, 'weather-big', os.path.split(fn)[-1].replace('hdf5', 'npy'))


        out_fn = os.path.join(data_dir, 'weather-big', os.path.split(fn)[-1])

        try:
            with h5py.File(out_fn) as f:
                f.create_dataset('/t2m', data=y, chunks=(500, 500))
        except:
            pass

if __name__ == '__main__':
    create_weather()
