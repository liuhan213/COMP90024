#!/bin/bash
#SBATCH --partition physical
#SBATCH --time=00:50:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --job-name=1node_1core

echo 'Run with 1 node and 1 core'

module load Python/2.7.9-goolf-2015a
time mpiexec python rank.py
