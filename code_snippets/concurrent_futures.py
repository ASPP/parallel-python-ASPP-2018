import time
from concurrent.futures import ThreadPoolExecutor

def do_nothing(t):
    time.sleep(t)
    print("Done.")

with ThreadPoolExecutor(max_workers=4) as executor:
    futures = [executor.submit(do_nothing, 1) for i in range(5)]

for future in futures:
    future.result()
