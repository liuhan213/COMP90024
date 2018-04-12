#!/bin/bash
#FarahKhan_613572
dir="/home/farahk/results"
Walltime=00:30:00
find /home/farahk/results -name 'Twitter_Segments*' >Twitter_SegFiles
paste -d,  $PBS_NODEFILE Twitter_SegFiles > Tasks

for Task in $(cat $dir/Tasks); do 
Core=$(echo $Task | awk -F"," '{print $1}')
File=$(echo $Task | awk -F"," '{print $2}')
ssh -X -o 'StrictHostKeyChecking=no' $Core $dir/Twitter_Parser.sh $File  >> OUTPUT &
done
sleep 5m
rm -rf Twitter_SegFiles Tasks
