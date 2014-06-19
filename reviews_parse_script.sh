#!/bin/sh

#  parse_script.sh
#  
#
#  Created by Galeota-Sprung, Jonah on 12/3/12.
#  still under production; currently just saving greps

cd ~/Documents/SALADAZ

count=0
for file in `ls ~/Documents/SALADAZ/review_pages/reviews-*-*`
do

#get actual reviews
grep -A 2 "listItemReviewFull" $file | cut -d ">" -f2 >> reviews_output_sample


count=$((count+1))
done
