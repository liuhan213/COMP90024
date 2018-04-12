#!/bin/bash
#SBATCH --partition physical
#SBATCH --time=00:50:00
#SBATCH --nodes=1
#SBATCH --ntasks=8
#SBATCH --job-name=1node_8cores

echo 'Run with one node and 8 cores'
module load Python/3.5.2-goolf-2015a
time mpiexec python cc1.py
