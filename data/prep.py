"""
(c) 2017-2018, Anaconda, Inc. and contributors
All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

Redistributions of source code must retain the above copyright notice,
this list of conditions and the following disclaimer.

Redistributions in binary form must reproduce the above copyright notice,
this list of conditions and the following disclaimer in the documentation
and/or other materials provided with the distribution.

Neither the name of Anaconda nor the names of any contributors may be used to
endorse or promote products derived from this software without specific prior
written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
THE POSSIBILITY OF SUCH DAMAGE.
"""

import os
import numpy as np
from glob import glob

data_dir = here = os.path.dirname(__file__)

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
