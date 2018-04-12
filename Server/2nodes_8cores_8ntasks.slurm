#!/bin/bash
#SBATCH --partition physical
#SBATCH --time=00:50:00
#SBATCH --nodes=2
#SBATCH --ntasks=8
#SBATCH --ntasks-per-node=4
#SBATCH --job-name=2node_4cores_8ntasks

echo 'Run with 2 nodes 8cores and 8 ntasks'

module load Python/2.7.9-goolf-2015a
time mpiexec python rank.py
