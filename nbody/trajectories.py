import time

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np

from nbody import *

ims = []

fig, ax = plt.subplots()

sc = plt.scatter([], [])

def step(i):
    positions[0, :] = 0

    t1 = time.time()
    advance(0.0001, 100)
    t2 = time.time()

    x_list = positions[:, 0]
    y_list = positions[:, 1]

    sc.set_offsets(np.c_[x_list, y_list])
    plt.axis([-200, 200, -200, 200])
 
    print(t2-t1)

im_ani = animation.FuncAnimation(fig, step, 10, repeat=False)
plt.show()

print(positions[0, 0])
