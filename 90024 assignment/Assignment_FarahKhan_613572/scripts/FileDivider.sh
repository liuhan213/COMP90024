#!/bin/bash
#Farahkhan_613572
FileName='/home/farahk/data/Twitter.csv'
Segments=8
LineCount=`cat $FileName | wc -l`
Segment_Lines=`expr \( $LineCount + $Segments - 1 \) / $Segments` 
echo $Segment_Lines
echo $LineCount
split -l $Segment_Lines $FileName Twitter_Segments_
