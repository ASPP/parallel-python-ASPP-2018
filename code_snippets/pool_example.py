import time

def func(a):
    time.sleep(5)
    return a + 1

import multiprocessing

with multiprocessing.Pool(4) as p:
    out = p.map(func, [2, 1, 9])

print(out)
