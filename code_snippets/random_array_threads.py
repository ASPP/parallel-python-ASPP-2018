from threading import Thread
import time

import numpy as np

def generate_random_array(n):
    """
    Generate a random array of size 'n'
    """
    a = np.random.RandomState().randint(0, 10, (int(n),))
    print("Done.")

threads = []

for i in range(4):
    t = Thread(target=generate_random_array, args=(1e8,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
