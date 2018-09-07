import time

import numpy as np

import matplotlib.animation as animation
import matplotlib.pyplot as plt

def initialize(comm, T0, T1):
    rank = comm.Get_rank()
    size = comm.Get_size()
    T0[:, 0] = 1
    T0[:, -1] = 1
    if rank == 0:
        T0[0, :] = 1
    T1[...] = T0[...]

def diffusion_kernel(T0, T1):
    T1[1:-1, 1:-1] = (T0[1:-1, 2:]
                    + T0[1:-1, :-2]
                    + T0[2:, 1:-1]
                    + T0[:-2, 1:-1])/4.0

def converged(comm, T0, T1, rtol=1e-5, atol=1e-8):
    local_converged = np.asarray(int(np.all(np.abs(T1 - T0) <= (atol + rtol * np.abs(T1)))))
    global_converged = np.asarray(0)

    comm.Allreduce([local_converged, MPI.INT], [global_converged, MPI.INT])

    if global_converged == comm.Get_size():
        return True
    else:
        return False

def diffusion_step(comm, T0, T1, halos):
    top_send, bottom_send, top_recv, bottom_recv = halos
    rank = comm.Get_rank()
    size = comm.Get_size()

    if rank > 0:
        top_send[...] = T0[0, :]
        comm.Sendrecv(top_send, dest=rank-1, sendtag=10, recvbuf=top_recv, source=rank-1, recvtag=20)

    if rank < size-1:
        bottom_send[...] = T0[-1, :]
        comm.Sendrecv(bottom_send, dest=rank+1, sendtag=20, recvbuf=bottom_recv, source=rank+1, recvtag=10)

    diffusion_kernel(T0, T1)

    if rank > 0:
        T1[0, 1:-1] = (T0[0, 2:]
                     + T0[0, :-2]
                     + top_recv[1:-1]
                     + T0[1, 1:-1])/4.0

    if rank < size-1:
        T1[-1, 1:-1] = (T0[-1, :-2]
                      + T0[-1, 2:]
                      + bottom_recv[1:-1]
                      + T0[-2, 1:-1])/4.0

NX = 64
NY = NX * 4
MAX_STEPS = 10000
ALPHA = 1

from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

T0 = np.zeros([NY//size, NX], dtype=np.float64)
T1 = T0.copy()

T = np.zeros([NY, NX], dtype=np.float64)

top_send = np.zeros(NX, dtype=np.float64)
bottom_send = top_send.copy()
top_recv = top_send.copy()
bottom_recv = top_send.copy()

halos = [top_send, bottom_send, top_recv, bottom_recv]

initialize(comm, T0, T1)

def step(i):
    t1 = MPI.Wtime()
    if i % 2:
        diffusion_step(comm, T0, T1, halos)
    else:
        diffusion_step(comm, T1, T0, halos)
    t2 = MPI.Wtime()
    if rank == 0:
        print("Time for step {}: {}s".format(i, t2-t1))

for i in range(MAX_STEPS):
    step(i)
    if i % 100:
        comm.Barrier()
        if converged(comm, T0, T1):
            print("Convergence acheived after {} steps".format(i))
            break

comm.Gather( [T1, MPI.DOUBLE], [T, MPI.DOUBLE] )

if rank == 0:
    fig, ax = plt.subplots()
    im = ax.imshow(T)
    plt.show()
