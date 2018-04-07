#!/usr/bin/python
#hello.py
from mpi4py import MPI
import time
comm = MPI.COMM_WORLD

time_start = time.time()



size = comm.Get_size()
rank = comm.Get_rank()
name = MPI.Get_processor_name()
#print "hello world from process ", rank,"of", size


print "Hello world, I am process rank{} of size {} on name{}\n".format(rank,size,name)
