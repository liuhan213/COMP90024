#!/bin/bash
#SBATCH -p physical
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=00:50:00
#SBATCH --job-name=bigInstagram_1node_1cores

echo 'Run job with 1 node and 1 core'
echo ' '

module load Python/3.5.2-goolf-2015a
mpiexec python count2.py
