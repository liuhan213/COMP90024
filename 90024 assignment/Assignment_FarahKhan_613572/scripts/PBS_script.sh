#!/bin/bash
#PBS -N TwitterData_1Node_8Processor
#PBS -e error_node1_ppn8.dat
#PBS -q fast
#PBS -l nodes=2:ppn=4,walltime=00:30:00
#PBS -M farahk@student.unimelb.edu.au
cd $PBS_O_WORKDIR
sh JobDistribution.sh
