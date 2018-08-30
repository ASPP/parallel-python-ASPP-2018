# The Computer Language Benchmarks Game
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

N = 50

from multiprocessing.sharedctypes import RawArray

buf_1 = RawArray('d', N * 3)
buf_2 = RawArray('d', N * 3)
buf_3 = RawArray('d', N)

positions = np.frombuffer(buf_1).reshape([N, 3])
velocities = np.frombuffer(buf_2).reshape([N, 3])
masses = np.frombuffer(buf_3).reshape([N,])

positions[...] = np.loadtxt('initial_positions.txt')
velocities[...] = np.loadtxt('initial_velocities.txt')
masses[...] = np.loadtxt('masses.txt')

def velocity_offsets(pair, dt):
    x1, x2 = positions[pair[0]], positions[pair[1]]
    v1, v2 = velocities[pair[0]], velocities[pair[1]]
    m1, m2 = masses[pair[0]], masses[pair[1]]
    dx = x1 - x2
    mag = dt * np.linalg.norm(dx)
    b1m = m1 * mag
    b2m = m2 * mag
    dv1 = dx * b2m
    dv2 = dx * b1m
    return dv1, dv2

def update_velocities(dv):
    for i, pair in enumerate(itertools.combinations(range(N), 2)):
        v1, v2 = velocities[pair[0]], velocities[pair[1]]
        v1 += dv[i][0]
        v2 += dv[i][1]

p = multiprocessing.Pool(8)

def advance(dt, n, positions=positions, velocities=velocities):
    for step in range(n):
        dv = p.starmap(velocity_offsets, zip(itertools.combinations(range(N), 2), itertools.repeat(dt)))
        update_velocities(dv)
        positions += dt * velocities


ims = []

fig, ax = plt.subplots()

sc = plt.scatter([], [])

def step(i):
    positions[0, :] = 0

    t1 = time.time()
    advance(0.001, 5)
    t2 = time.time()

    x_list = positions[:, 0]
    y_list = positions[:, 1]

    sc.set_offsets(np.c_[x_list, y_list])
    plt.axis([-200, 200, -200, 200])

    print(t2-t1)

im_ani = animation.FuncAnimation(fig, step, 100, repeat=False)
plt.show()

print("Position of particle 5: {}".format(positions[5]))
