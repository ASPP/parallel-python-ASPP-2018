import time

import numpy as np

import matplotlib.animation as animation
import matplotlib.pyplot as plt

from numba import jit

def diffusion_kernel(T0, T1):
    T1[1:-1, 1:-1] = (T0[1:-1,2:] + T0[1:-1,:-2] +
                      T0[2:,1:-1] + T0[:-2,1:-1])/4.0

def converged(T0, T1, rtol=1e-5, atol=1e-8):
    return np.all (np.abs(T1 - T0) <= (atol + rtol * np.abs(T1)))

NX = 64
NY = NX * 4
MAX_STEPS = 100000
ALPHA = 1
animate = False

T0 = np.zeros([NY, NX], dtype=np.float64)
T0[:,0] = T0[:,-1] = T0[0,:] = 1
T1 = T0.copy()

def step(i):
    t1 = time.time()
    if i % 2:
        diffusion_kernel(T0, T1)
    else:
        diffusion_kernel(T1, T0)
    t2 = time.time()
    print("Time for step {}: {}".format(i, t2-t1))

if animate:
    def init_func():
        ax.set_xlim([0, NX])
        ax.set_ylim([0, NY])
        return im,

    def frame(i):
        step(i)
        t2 = time.time()
        im.set_data(T0)
        return im,

    fig, ax = plt.subplots()
    im = ax.imshow(T0)
    fig.colorbar(im)
    im_ani = animation.FuncAnimation(
        fig,
        frame,
        MAX_STEPS,
        repeat=False,
        blit=True,
        interval=10,
        init_func=init_func)

    plt.show()

else:
    for i in range(MAX_STEPS):
        step(i)
        if i % 100:
            if converged(T0, T1):
                print("Convergence acheived after {} steps".format(i))
                break

    fig, ax = plt.subplots()
    im = ax.imshow(T0)
    fig.colorbar(im)
    plt.show()
