import json
from mpi4py import MPI
import time
import numpy as np


start_time = time.time()

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()


data1 = [i for i in range(10)]
#print(data1)

# hunk=[]
if rank == 0:
     chunks = np.array_split(data1, size)

#     print chunks,'\n'

else:
    chunks = None

chunk = comm.scatter(chunks, root=0)
result = comm.gather(chunk)

print result

#or i in chunk:
#    i = i + 5
#print chunk,'\n'
#print 'chunk',rank,chunk,'\n'

#result=[]
#if rank ==0:
#    result = comm.gather(chunks)
#    print result


#    for i in chunk:
#        i = i+1
#    print'i am rank' ,rank, 'from size', size ,'and the +1 chunks is ',chunk,'\n'
# Gather all of results from child process
#result = comm.gather(chunk)
#print 'i am rank' ,rank, 'from size', size ,'and the final chunks is ',result,'\n'
