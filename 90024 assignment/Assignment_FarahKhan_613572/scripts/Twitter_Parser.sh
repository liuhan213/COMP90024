#!/bin/bash
date > time_`hostname`_$$
cat $PBS_NODEFILE > n
NL='
'
FileName=$1
awk -F "\"*,\"*" '{print $5,$6,$7,$8,$9,$10 "|" }' $FileName | tr '|' '\n' |tr '[:upper:]' '[:lower:]' | grep -v '^$' > xaa_tweets_$$.txt

#Top ten Topics trending on twitter
sed 's/[\]/" "/g' xaa_tweets_$$.txt | egrep -o "(\s(#\S+))" | cut -d " " -f 2 > hashtags_$$.txt
sed "s/#/,\\$NL/g"  hashtags_$$.txt | sed 's/[:]//g' | sed 's/,$//' |sed 's/""$//' | sed 's/"$//' | sort | uniq -c | sort -n -r > sorted_topics_`hostname`_$$.txt

#Top ten tweeters mentioned 
sed 's/[\"]/" "/g' xaa_tweets_$$.txt | egrep -o "(\s(@\S+))" | cut -d " " -f 2 > tweeters_$$.txt
sed "s/@/,\\$NL/g" tweeters_$$.txt | sed 's/[:]/""/g' | sed 's/,$//' |sed 's/""$//' | sed 's/"$//' | sort | uniq -c | sort -n -r  > sorted_tweeters_`hostname`_$$.txt

#Number of times term "football" is found in twitter data
count_term=$(grep -o "football" xaa_tweets_$$.txt | wc -l) 
echo "\nNumber of times 'football' exists in this file is: ${count_term} \n" > count_`hostname`_$$.txt
echo `date` >> time_`hostname`_$$


rm -rf  xaa_tweets_$$.txt hashtags_$$.txt  tweeters_$$.txt
