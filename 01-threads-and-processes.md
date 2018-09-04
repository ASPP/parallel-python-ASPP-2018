# Threads and processes

The Python standard library provides the
[https://docs.python.org/3/library/threading.html](threading)
and
[https://docs.python.org/3.7/library/multiprocessing.html](multiprocessing)
for "parallelism".

How long does the following code take to run?

```
def do_nothing(t=5):
    """
    Do nothing for 't' seconds.
    """
    time.sleep(t)
    print("Done.")

for i in range(4):
    do_nothing()
```

How about the following?

```
from threading import Thread
import time

def do_nothing(t=5):
    """
    Do nothing for 't' seconds.
    """
    time.sleep(t)
    print("Done.")

threads = []

for i in range(4):
    t = Thread(target=do_nothing)
    threads.append(t)
    t.start()

for t in threads:
    t.join()
```

```python
from multiprocessing import Process
import time

def do_nothing(t=5):
    """
    Do nothing for 't' seconds.
    """
    time.sleep(t)
    print("Done.")

processes = []

for i in range(4):
    p = Process(target=do_nothing)
    processes.append(p)
    p.start()

for p in processes:
    p.join()

```

The following code takes 1-2 seconds to run on my laptop:

```
In [1]: %timeit np.random.rand(int(1e8))
1.74 s ± 21.9 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
```

Now, can you estimate the time that each of the following will take to run?

```
from threading import Thread
import time

import numpy as np

def generate_random_array(n):
    """
    Generate a random array of size 'n'
    """
    a = np.random.rand(int(n))
    print("Done.")

threads = []

for i in range(4):
    t = Thread(target=generate_random_array, args=(1e8,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
```

```
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
```

## The GIL

In CPython, only **one** thread can execute Python code at once,
due to the [Global Interpreter Lock](https://docs.python.org/3.7/glossary.html#term-global-interpreter-lock)
(pictured below):

![GIL](images/GIL_balrog.jpg)

The GIL ensures that when multiple threads access Python objects,
they do so without interfering with each other.
For example,
the following code *always* prints ``[11, 2, 3]``.

```
from threading import Thread

def update(a):
    a[0] += 1

a = [1, 2, 3]

threads = []

for i in range(10):
    t = Thread(target=update, args=(a,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print(a)
```


