# Exercise

* Navigate to the directory `exercises/weather-stats`.

* The files `data/weather-big/*.hdf5` contain temperature data
for the year 2014 at discrete points: a (2880, 5760) grid.
Our objective is to compute the min, max and mean temperature at each point.
Use the file `weather_stats.py` as a starting point.

1. Write a serial program to compute the min, max and mean temperatures.
2. Could you use multiprocessing to parallelize the computation?
3. Write a parallel implementation using Dask. How does this compare with the serial implementation?
