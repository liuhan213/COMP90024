from mpi4py import MPI
import numpy as np
import json

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

if rank == 0:
   data = [(x) for x in range(10)]

   data1 = np.array_split(data, size)
   print 'we will be scattering:',data1

else:
   data1 = None

#data2 = comm.scatter(data1, root=0)
#data2 += 1
#print 'rank',rank,'has data:',data2

#newData = comm.gather(data2,root=0)

#if rank == 0:
#   print 'master:',newData
