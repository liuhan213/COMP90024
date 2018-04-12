#!/bin/bash
#SBATCH -p physical
#SBATCH --nodes=2
#SBATCH --ntasks=8
#SBATCH --time=00:30:00
#SBATCH --mail-type=END,FAIL
#SBATCH --job-name=bigInstagram_2nodes_8cores
#SBATCH -e output/error/job3/error_%j.err
#SBATCH -o output/job3/slurm-%j.out

echo 'Run job with 2 node and 8 core'
echo ' '

module load Python/3.5.2-goolf-2015a
mpiexec python rank.py
