from mpi4py import MPI
comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

if rank == 0:
    data = [(i)**2 for i in range(size)]
    print(data)

else:
    data = None

data = comm.scatter(data, root=0)
#print "before assert: data on rank {} is:{}".format(rank,data)
#assert data == (rank)**2
print "data on rank {} is:{}".format(rank,data)
