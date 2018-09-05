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
    
