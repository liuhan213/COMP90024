from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

if rank == 0:
   data = [(x+1) for x in range(30)]
   print 'we will be scattering:',data
   data_split = np.array_split(data, size)
   print 'data_split:',data_split


else:
   data = None

data_scatter = comm.scatter(data_split, root=0)
#for i in data_scatter:
#    i=i+5
print'data_scatter:',data_scatter

#for i in data:
#    i = i+1
#print 'rank',rank,'has data:',data

newData = comm.gather(data_scatter,root=0)
print'data_gather:',newData
#if rank == 0:
#   print 'master:',newData
