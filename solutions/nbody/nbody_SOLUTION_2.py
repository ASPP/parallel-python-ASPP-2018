# The Computer Language Benchmarks Game
# http://benchmarksgame.alioth.debian.org/
#
# originally by Kevin Carson
# modified by Tupteq, Fredrik Johansson, and Daniel Nanz
# modified by Maciej Fijalkowski
# 2to3

import argparse
import itertools
import multiprocessing
import time

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np

# ensure repeatable results
np.random.seed(0)

# number of time steps per frame
STEPS_PER_FRAME = 5

def offset_p(p, positions, velocities, masses, dt):
    """
    Calculate the offset for particle 'p'
    """
    p1 = p

    for p2 in range(len(positions)):
        x1 = positions[p1]
        x2 = positions[p2]

        m1 = masses[p1]
        m2 = masses[p2]

        v1 = velocities[p1]
        v2 = velocities[p2]

        dx = x1 - x2

        mag = dt * np.linalg.norm(dx)

        offset = m2 * mag
        
        if p1 < p2:
            offsets[p1] += dx * offset
        else:
            offsets[p1] -= dx * offset

def advance(dt, n, positions, velocities, masses):
    """
    Advance the simulation by 'n' time steps.
    """
    for step in range(n):
        positions[0, :] = 0
        offsets[...] = 0
        pool.starmap(
            offset_p,
            zip(
                range(len(positions)),
                itertools.repeat(positions),
                itertools.repeat(velocities),
                itertools.repeat(masses),
                itertools.repeat(dt)
            )
        )
        velocities += offsets
        positions += dt * velocities

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='N-body simulation')
    parser.add_argument('N', default=5, type=int)
    parser.add_argument('nsteps', nargs='?', default=100, type=int)
    parser.add_argument('--animate', action='store_true')

    args = parser.parse_args()

    N = args.N
    nsteps = args.nsteps
    animate = args.animate

    positions = np.random.rand(N, 3) * 80 - 40
    velocities = np.random.rand(N, 3) * 2 - 1
    masses = np.random.rand(N) * 0.05

    from multiprocessing.sharedctypes import RawArray

    buf = RawArray('d', N*3)
    offsets = np.frombuffer(buf).reshape((N, 3))

    # initial conditions:
    positions[0, :] = 0
    masses[0] = 100

    ims = []

    fig, ax = plt.subplots()
    sc = ax.scatter([], [])

    def init_func():
        ax.set_xlim([-100, 100])
        ax.set_ylim([-100, 100])
        return sc,

    def frame(i):
        t1 = time.time()
        advance(0.001, STEPS_PER_FRAME, positions, velocities, masses)
        t2 = time.time()

        sc.set_offsets(positions[:, :2])

        print("Time for step {}: {}s".format(i, t2-t1))
        return sc,

    with multiprocessing.Pool(4) as pool:
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
