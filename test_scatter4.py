#!/usr/bin/env python

from mpi4py import MPI

import numpy as np

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

# Use default communicator. No need to complicate things.
COMM = MPI.COMM_WORLD


def split(container, count):
    return [container[_i::count] for _i in range(count)]


# Collect whatever has to be done in a list. Here we'll just collect a list of
# numbers. Only the first rank has to do this.
if rank == 0:
    jobs = list(range(10))
    # Split into however many cores are available.
    jobs = split(jobs, size)
else:
    jobs = None

# Scatter jobs across cores.
jobs = COMM.scatter(jobs, root=0)

# Now each rank just does its jobs and collects everything in a results list.
# Make sure to not use super big objects in there as they will be pickled to be
# exchanged over MPI.
results = []
for job in jobs:
    # Do something meaningful here...
    results.append(job+5)

# Gather results on rank 0.
results = MPI.COMM_WORLD.gather(results, root=0)

if COMM.rank == 0:
    # Flatten list of lists.
    results = [_i for temp in results for _i in temp]

    print("Results:", results)
