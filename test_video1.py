from mpi4py import MPI

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

if rank == 0:
    # original data
   data = [{"id":"a1","count":13},{"id":"a2","count":16},{"id":"a1","count":14},{"id":"a4","count":19},{"id":"a5","count":13},{"id":"a1","count":16},{"id":"a1","count":14},{"id":"a8","count":19}]
   print 'we will be scattering:',data
   print 'number of list', len(data)
   # divide data
   divided_data = []
   divided_data = [data[i::size] for i in range(size)]

   print 'after divide:',divided_data
   print 'number of list',len(divided_data)

else:
   data = None



#chunks = [big_chunk[i::size] for i in range(count)]

after_scatter = comm.scatter(divided_data, root=0)
print 'rank',rank,':after_scatter_has data:',after_scatter
gather_chunk = comm.gather(after_scatter,root=0)

if rank == 0:
    result = []
    print 'type of newdata:',type(gather_chunk)
    print 'len of newdata:',len(gather_chunk)
    print 'master:', gather_chunk
