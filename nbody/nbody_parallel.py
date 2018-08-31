# The Computer Language Benchmarks G
# http://benchmarksgame.alioth.debian.org/
#
# originally by Kevin Carson
# modified by Tupteq, Fredrik Johansson, and Daniel Nanz
# modified by Maciej Fijalkowski
# 2to3

import itertools
import multiprocessing
import sys
import time

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np

from multiprocessing.sharedctypes import RawArray

positions = np.loadtxt('initial_positions.txt')

N = len(positions)

pairs = np.array(list(itertools.combinations(range(N), 2)), dtype=np.int32)
num_pairs = len(pairs)

buf_1 = RawArray('d', N * 3)
buf_2 = RawArray('d', N * 3)
buf_3 = RawArray('d', N)
buf_4 = RawArray('d', num_pairs * 2 * 3)

positions = np.frombuffer(buf_1).reshape([N, 3])
velocities = np.frombuffer(buf_2).reshape([N, 3])
masses = np.frombuffer(buf_3).reshape([N,])
offsets = np.frombuffer(buf_4).reshape([num_pairs, 2, 3])

positions[...] = np.loadtxt('initial_positions.txt')
velocities[...] = np.loadtxt('initial_velocities.txt')
masses[...] = np.loadtxt('masses.txt')

def velocity_offsets(p1, p2, dt, i):
    x1, x2 = positions[p1], positions[p2]
    v1, v2 = velocities[p1], velocities[p2]
    m1, m2 = masses[p1], masses[p2]
    dx = x1 - x2
    mag = dt * np.linalg.norm(dx)
    b1m = m1 * mag
    b2m = m2 * mag
    dv1 = dx * b2m
    dv2 = dx * b1m
    offsets[i, 0] = dv1
    offsets[i, 1] = dv2

p = multiprocessing.Pool(4)

def advance(dt, n, positions=positions, velocities=velocities, masses=masses, pairs=pairs, offsets=offsets):
    for step in range(n):
        p.starmap(velocity_offsets,
                  zip(
                      pairs[:,0],
                      pairs[:,1],
                      itertools.repeat(dt),
                      range(num_pairs)))
        for i in range(len(pairs)):
            p1 = pairs[i, 0]
            p2 = pairs[i, 1]
            velocities[p1] += offsets[i, 0]
            velocities[p2] += offsets[i, 1]
        positions += dt * velocities

ims = []

fig, ax = plt.subplots()
sc = ax.scatter([], [])

def init_func():
    ax.set_xlim([-100, 100])
    ax.set_ylim([-100, 100])
    return sc,

def step(i):
    positions[0, :] = 0

    t1 = time.time()
    advance(0.001, 5)
    t2 = time.time()

    sc.set_offsets(positions[:, :2])

    print(t2-t1)
    return sc,

im_ani = animation.FuncAnimation(fig, step, 100, repeat=False, blit=True, init_func=init_func)
plt.show()

print("Position of particle 5: {}".format(positions[5]))
