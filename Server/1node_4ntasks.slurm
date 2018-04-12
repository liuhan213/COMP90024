#!/bin/bash
#SBATCH --partition physical
#SBATCH --time=00:50:00
#SBATCH --nodes=1
#SBATCH --ntasks=4
#SBATCH --job-name=1node_4ntasks

echo 'Run with 1 node and 4 ntasks'

module load Python/2.7.9-goolf-2015a
time mpiexec python rank.py
