from mpi4py import MPI

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

data = (rank)**2
data = comm.gather(data, root=0)


if rank == 0:
    for i in range(size):
        assert data[i] == (i)**2
        print "data is {}".format(data)
else:
    assert data is None
