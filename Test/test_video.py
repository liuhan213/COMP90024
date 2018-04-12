from mpi4py import MPI

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

if rank == 0:
   data = [{"id":"a1","count":13},{"id":"a2","count":16},{"id":"a3","count":14},{"id":"a4","count":19},{"id":"a1","count":13},{"id":"a2","count":16},{"id":"a3","count":14},{"id":"a4","count":19}]
   print 'we will be scattering:',data
else:
   data = None
data = [data[i::size] for i in range(size)]
#chunks = [big_chunk[i::size] for i in range(count)]
print 'after divide, we will be scattering:',data
data = comm.scatter(data, root=0)
#data += 1
print 'rank',rank,'has data:',data

newData = comm.gather(data,root=0)

if rank == 0:
   print 'master:',newData
