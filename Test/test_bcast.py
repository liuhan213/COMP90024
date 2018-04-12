from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()

if rank == 0:
    data = {'key1':[7,2.72,2+3j],'key2':('abc','xyz')}
    print "rank0{}".format(data)
else:
    data = None

data = comm.bcast(data, root=0)
print "bcast finished and data on rank {} is: {}".format(rank,data)
