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

import numpy as np

def step(num_steps, positions, velocities, masses, dt):
    """
    Advance the simulation by 'num_steps' time steps.
    """
    positions[0, :] = 0

    for step in range(num_steps):

        for i in range(N):
            for j in range(N):

                x1, x2 = positions[i], positions[j]
                v1, v2 = velocities[i], velocities[j]
                m1, m2 = masses[i], masses[j]

                dx = x1 - x2

                mag = dt * np.linalg.norm(dx)
                F = m2 * mag * dx

                if i < j:
                    velocities[i] += F
                else:
                    velocities[i] -= F

        positions += dt * velocities

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='N-body simulation')
    parser.add_argument('N', default=5, type=int)
    parser.add_argument('nsteps', nargs='?', default=100, type=int)
    parser.add_argument('--animate', action='store_true')

    args = parser.parse_args()

    # ensure repeatable results
    np.random.seed(0)

    # number of time steps per frame
    STEPS_PER_FRAME = 5

    N = args.N
    nsteps = args.nsteps
    animate = args.animate

    if not animate:
        import matplotlib
        matplotlib.use('Agg')

    import matplotlib.animation as animation
    import matplotlib.pyplot as plt

    positions = np.random.rand(N, 3) * 80 - 40
    velocities = np.random.rand(N, 3) * 2 - 1
    masses = np.random.rand(N) * 0.05

    dt = 0.001

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
        """
        Compute one frame of the animation.
        """
        t1 = time.time()
        step(STEPS_PER_FRAME, positions, velocities, masses, dt)
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
