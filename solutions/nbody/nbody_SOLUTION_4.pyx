# The Computer Language Benchmarks Game
# http://benchmarksgame.alioth.debian.org/
#
# originally by Kevin Carson
# modified by Tupteq, Fredrik Johansson, and Daniel Nanz
# modified by Maciej Fijalkowski
# 2to3

import argparse
import itertools
from threading import Thread
import time

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np

import cython

# ensure repeatable results
np.random.seed(0)

# number of time steps per frame
STEPS_PER_FRAME = 5

from numpy.linalg import norm

import cython

@cython.boundscheck(False)
def offset_p(int[:] p, double[:,:] positions, double[:,:] velocities, double[:] masses, double dt):
    """
    Calculate the offset for particles 'p'
    """
    dx_ = np.empty(3)
    cdef:
        double[:] x1, x2, v1, v2, dx = dx_
        double m1, m2, mag, b2m
        int p1, p2, i

    cdef int N = len(positions)
    cdef int M = len(p)
    
    with cython.nogil:
        for i in range(M):
            p1 = p[i]
            for p2 in range(N):
                x1 = positions[p1]
                x2 = positions[p2]

                m1 = masses[p1]
                m2 = masses[p2]

                v1 = velocities[p1]
                v2 = velocities[p2]

                dx[0] = x1[0] - x2[0]
                dx[1] = x1[1] - x2[1]
                dx[2] = x1[2] - x2[2]

                mag = dt * (dx[0]**2 + dx[1]**2 + dx[2]**2)**0.5

                b2m = m2 * mag

                if p1 < p2:
                    v1[0] += dx[0] * b2m
                    v1[1] += dx[1] * b2m
                    v1[2] += dx[2] * b2m
                else:
                    v1[0] -= dx[0] * b2m
                    v1[1] -= dx[1] * b2m
                    v1[2] -= dx[2] * b2m

def advance(dt, n, positions, velocities, masses):
    """
    Advance the simulation by 'n' time steps.
    """
    positions[0, :] = 0

    num_threads = 4

    N = len(positions)
    pN = N // num_threads
    
    for step in range(n):
        threads = []
        for i in range(num_threads):
            p1 = np.arange(i*pN, i*pN+pN, dtype=np.int32)
            t = Thread(
                    target=offset_p,
                    args=(p1, positions, velocities, masses, dt))
            t.start()
            threads.append(t)
        for t in threads: t.join()
        positions += dt * velocities

def __main__(args):
    parser = argparse.ArgumentParser(description='N-body simulation')
    parser.add_argument('N', default=5, type=int)
    parser.add_argument('nsteps', nargs='?', default=100, type=int)
    parser.add_argument('--animate', action='store_true')

    args = parser.parse_args(args)

    N = args.N
    nsteps = args.nsteps
    animate = args.animate

    positions = np.random.rand(N, 3) * 80 - 40
    velocities = np.random.rand(N, 3) * 2 - 1
    masses = np.random.rand(N) * 0.05

    # initial conditions:
    positions[0, :] = 0
    masses[0] = 10

    ims = []

    fig, ax = plt.subplots()
    sc = ax.scatter([], [])

    def init_func():
        ax.set_xlim([-100, 100])
        ax.set_ylim([-100, 100])
        return sc,

    def frame(i):
        """
        Compute one frame of the animation.
        """
        t1 = time.time()
        advance(0.001, 5, positions, velocities, masses)
        t2 = time.time()

        sc.set_offsets(positions[:, :2])

        print("Time for step {}: {}s".format(i, t2-t1))
        return sc,

    if animate:
        im_ani = animation.FuncAnimation(
                fig,
                frame,
                nsteps,
                repeat=False,
                blit=True,
                interval=10,
                init_func=init_func)
        plt.show()
    else:
        for i in range(nsteps):
            frame(i)

    print("Position of particle 2: {}".format(positions[2]))

if __name__ == "__main__":
   __main__()
