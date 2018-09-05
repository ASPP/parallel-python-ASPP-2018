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
