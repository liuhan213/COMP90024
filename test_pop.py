from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

if rank == 0:
    data = {'a': 7, 'b': 3.14}
    comm.send(data, dest=1, tag=11)
    print "this is from process ", rank,"of", size
    print "Message sent, data is:{} ".format(data)
elif rank == 1:
    data = comm.recv(source=0, tag=11)
    print "hello world from process ", rank,"of", size
    print "Message Received, data is:{}".format(data)
