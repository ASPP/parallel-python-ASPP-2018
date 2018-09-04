from multiprocessing import Process

def update(a):
    a[0] += 1

a = [1, 2, 3]

processes = []

for i in range(10):
    p = Process(target=update, args=(a,))
    processes.append(p)
    p.start()

for p in processes:
    p.join()

print(a)
