from multiprocessing import Process
import time

import numpy as np

def generate_random_array(n):
    """
    Generate a random array of size 'n'
    """
    a = np.random.rand(int(n))
    print("Done.")

processes = []

for i in range(4):
    p = Process(target=generate_random_array, args=(1e8,))
    processes.append(p)
    p.start()

for p in processes:
    p.join()
