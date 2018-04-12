#!/bin/bash
#SBATCH -p physical
#SBATCH --nodes=2
#SBATCH --ntasks=8
#SBATCH --time=00:50:00
#SBATCH --job-name=bigInstagram_1node_8cores

echo 'Run job with 2 nodes and 8 cores'
echo ' '

module load Python/3.5.2-goolf-2015a
mpiexec python count2.py
