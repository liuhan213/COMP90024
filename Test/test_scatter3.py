
from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

if rank == 0:
    data = [i for i in range(8)]
# dividing data into chunks
    chunks = [[] for _ in range(size)]

    for i, chunk in enumerate(data):
        chunks[i % size].append(chunk)
else:
    data = None
    chunks = None
data = comm.scatter(chunks, root=0)
# how to calculate
for i in chunks:
    i = i+1
print str(rank) + ': ' + str(data)

# how to scatter
#newData = comm.gather(data,root=0)
#print'data_gather:',newData
