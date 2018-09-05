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
