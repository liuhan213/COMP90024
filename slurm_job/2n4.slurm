#!/bin/bash
#SBATCH --partition physical
#SBATCH --time=00:50:00
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=4


echo 'run with 2 nodes and 4 cores'
module load Python/2.7.9-goolf-2015a
time mpiexec python cc1.py 
