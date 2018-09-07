# Exercise

The file `diffusion_MPI.py` contains an MPI implementation of the 2-D heat equation.

Your objective is to write the function `converged`:

```python
    def converged(comm, T0, T1, rtol=1e-5, atol=1e-8):
        return False
```

The equivalent serial implementation is:


```python
def converged(T0, T1, rtol=1e-5, atol=1e-8):
    return np.all (np.abs(T1 - T0) <= (atol + rtol * np.abs(T1)))
```
