#!/bin/bash
#Calculate time
#FarahKhan_613572
echo  "Output for 1 node and 8 cores" > Output_1Node_8Cores
t2s()
{
  local T=$1;shift
  echo $((10#${T:0:2} * 3600 + 10#${T:3:2} * 60 + 10#${T:6:2})) 
}
start_time=13:12:56
total_time=0
for file in time*; do 
	cat $file | awk '{ print $4 }'  >>all_times
done
while read line
	do
	echo $line
	if [ "$line" != "$start_time" ];
	then
		end_time=$line
		diff_time=$(( $(t2s $end_time) - $(t2s $start_time) ))
		total_time=$[$total_time+$diff_time]
fi
done < all_times
number_of_times=8
average_time=$(echo $((total_time / number_of_times)))
echo "Average time by all 8 processors is: $average_time seconds" >> Output_1Node_8Cores
echo "**********************************************" >> Output_1Node_8Cores
for f in sorted*; do
   tail -n +2 "$f" > "${f}".tmp && mv "${f}".tmp "$f"
done
for file in sorted_tweeters*; do 
	head -15 $file >>all_tweeters

done 
echo "Top Ten Tweeters mentioned the most  on Twitter from given data:" >> Output_1Node_8Cores
awk '{A[$2]+=$1;next}END{for(i in A){print i,A[i]}}' all_tweeters | sort -r -nk2 | head >> Output_1Node_8Cores
echo "**********************************************" >> Output_1Node_8Cores 
for file in sorted_topics*; do
       head -15 $file >>all_topics
done
echo "Top Ten Topics in trending on Twitter from given data:" >> Output_1Node_8Cores
awk '{A[$2]+=$1;next}END{for(i in A){print i,A[i]}}' all_topics | sort -r -nk2 | head >> Output_1Node_8Cores
echo "**********************************************" >> Output_1Node_8Cores
count=0
for file in count*; do 
	temp=$(awk -F':' '{print $2;}' $file | sed 's/ //g' | sed 's/n//g')
	count_temp=$(echo "${temp%?}")
	echo $count_temp
	#$count=$count+$count_temp
	count=$[$count +$count_temp]
done	
echo $count
echo "The number of times term "football" exists in Twitter data is: $count" >>Output_1Node_8Cores
rm -rf all_tweeters all_topics all_times
 
