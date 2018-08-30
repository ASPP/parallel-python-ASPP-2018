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

N = 25

from multiprocessing.sharedctypes import RawArray

buf_1 = RawArray('d', N * 3)
buf_2 = RawArray('d', N * 3)
buf_3 = RawArray('d', N)

positions = np.frombuffer(buf_1).reshape([N, 3])
velocities = np.frombuffer(buf_2).reshape([N, 3])
masses = np.frombuffer(buf_3).reshape([N,])

positions[...] = np.random.rand(N, 3) * 80 - 40
velocities[...] = np.random.rand(N, 3) * 2 - 1
masses[...] = np.random.rand(N) * 0.05

masses[0] = 1

print(positions)
print(velocities)
print(masses)

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
    v1 += dv1
    v2 += dv2

p = multiprocessing.Pool(3)

def advance(dt, n, positions=positions):
    for step in range(n):
        p.starmap(velocity_offsets, zip(itertools.combinations(range(N), 2), itertools.repeat(dt)))
        positions += dt * velocities

"""
def report_energy(bodies=SYSTEM, pairs=PAIRS, e=0.0):
    for (((x1, y1, z1), v1, m1),
         ((x2, y2, z2), v2, m2)) in pairs:
        dx = x1 - x2
        dy = y1 - y2
        dz = z1 - z2
        e -= (m1 * m2) / ((dx * dx + dy * dy + dz * dz) ** 0.5)
    for (r, [vx, vy, vz], m) in bodies:
        e += m * (vx * vx + vy * vy + vz * vz) / 2.
    return e

def report_momentum(bodies=SYSTEM, pairs=PAIRS, px=0.0, py=0.0, pz=0.0):
    for (r, [vx, vy, vz], m) in bodies:
        px -= m*vx
        py -= m*vy
        pz -= m*vz
    return [px, py, pz]

def main(n, ref='sun'):
    offset_momentum(BODIES[ref])
    advance(0.01, n)

if __name__ == '__main__':
    main(int(sys.argv[1]))

"""
