#!/bin/bash
#SBATCH -p physical
#SBATCH --nodes=1
#SBATCH --ntasks=4
#SBATCH --time=00:05:00
#SBATCH --mail-type=END,FAIL
#SBATCH --job-name=bigInstagram_1node_4cores
#SBATCH -e output/error/job1/error_%j.err
#SBATCH -o output/job1/slurm-%j.out

echo 'Run job with 1 node and 4 cores'
echo ' '

module load  Python/3.5.2-goolf-2015a
mpiexec python rank.py
