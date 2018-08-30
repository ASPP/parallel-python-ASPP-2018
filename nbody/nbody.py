# The Computer Language Benchmarks Game
# http://benchmarksgame.alioth.debian.org/
#
# originally by Kevin Carson
# modified by Tupteq, Fredrik Johansson, and Daniel Nanz
# modified by Maciej Fijalkowski
# 2to3

import sys
import itertools

import numpy as np

import multiprocessing

def combinations(l):
    result = []
    for x in range(len(l) - 1):
        ls = l[x+1:]
        for y in ls:
            result.append((l[x],y))
    return result

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

masses[0] = 10

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
    for dvi, pair in zip(dv, itertools.combinations(range(N), 2)):
        velocities[pair[0]] += dvi[0]
        velocities[pair[1]] += dvi[1]

p = multiprocessing.Pool(8)

def advance(dt, n, positions=positions, velocities=velocities):

    for step in range(n):
        dv = p.starmap(velocity_offsets, zip(itertools.combinations(range(N), 2), itertools.repeat(dt)))
        update_velocities(dv)
        positions += dt * velocities
