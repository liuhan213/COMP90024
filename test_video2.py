from mpi4py import MPI

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

if rank == 0:
    # original data
   original_data = [{"id":"a1","count":13},{"id":"a2","count":16},{"id":"a1","count":14},{"id":"a4","count":19},{"id":"a5","count":13},{"id":"a1","count":16},{"id":"a1","count":14},{"id":"a8","count":19}]
#   print 'we will be scattering:', original_data
#   print 'number of list', len(original_data)
   # divide data

   divided_data = [original_data[i::size] for i in range(size)]

#   print 'after divide:',divided_data
#   print 'number of list',len(divided_data)

else:
   divided_data = None

after_scatter = comm.scatter(divided_data, root=0)
# print 'rank',rank,':after_scatter_has data:',after_scatter

gather_chunk = comm.gather(after_scatter,root=0)
#print 'rank',rank,':after_gather_has data:',gather_chunk
if rank == 0:
    result = []
    print 'type of newdata:',type(gather_chunk)
    print 'len of newdata:',len(gather_chunk)
    print 'master:', gather_chunk
    for chunk in gather_chunk:
        for coord in chunk:
            result.append(coord)
    print('result-------')
    print(result)


#    print('melbGrid_list--------')
#    print(melbGrid_list)
#    print('coords_list--------')
#    print(coords_list)
