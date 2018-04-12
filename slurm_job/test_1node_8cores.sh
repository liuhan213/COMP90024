#!/bin/bash
#SBATCH -p physical
#SBATCH --nodes=1
#SBATCH --ntasks=8
#SBATCH --time=00:30:00
#SBATCH --mail-type=END,FAIL
#SBATCH --job-name=bigInstagram_1node_8cores
#SBATCH -e output/error/job2/error_%j.err
#SBATCH -o output/job2/slurm-%j.out

echo 'Run job with 1 node and 8 cores'
echo ' '

module load Python/3.5.2-goolf-2015a
mpiexec python count.py
