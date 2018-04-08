#!/usr/bin/env python

from mpi4py import MPI

import numpy as np

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

# Use default communicator. No need to complicate things.



def split(list, count):
    return [list[i::count] for i in range(count)]


# Collect whatever has to be done in a list. Here we'll just collect a list of
# numbers. Only the first rank has to do this.
if rank == 0:
    jobs = [{'id':'a1','count':6},{'id':'a2','count':7},{'id':'a3','count':7},{'id':'a4','count':8},{'id':'a5','count':9}]
    # Split into however many cores are available.
    jobs = split(jobs, size)
    print(jobs)
else:
    jobs = None

# Scatter jobs across cores.
jobs = comm.scatter(jobs, root=0)
print('jobs after acatter-------')
print(jobs)
# Now each rank just does its jobs and collects everything in a results list.
# Make sure to not use super big objects in there as they will be pickled to be
# exchanged over MPI.
result = []
for job in jobs:
    # Do something meaningful here...
    job['count'] = job['count'] +10
    result.append(job)
    print str(rank) + ': ' + str(result)+'\n'

# Gather results on rank 0.
results = comm.gather(result, root=0)

if rank == 0:
    # Flatten list of lists.
    results = [_i for temp in results for _i in temp]

    print("Results:", results)
