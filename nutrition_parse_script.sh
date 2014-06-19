#!/bin/sh

#  nutrition_parse_script.sh
#  
#
#  Created by Galeota-Sprung, Jonah on 12/3/12.
#  Copyright (c) 2012 __MyCompanyName__. All rights reserved.

cd ~/Documents/SALADAZ

count=0
for file in `ls ~/Documents/SALADAZ/salad_recipes_test/salads-*`
do

echo -e "\nFat Content" >> salad_nutr_test/salad-nutr-$count

grep "fatContent" -A 1 $file |cut -d\> -f2 -f4 |cut -d\< -f1 >> salad_nutr_test/salad-nutr-$count

echo -e "\nSaturated Fat" >> salad_nutr_test/salad-nutr-$count

grep "saturatedFatContent" -A 1 $file |cut -d\> -f2 -f4 |cut -d\< -f1 >> salad_nutr_test/salad-nutr-$count

echo -e "\nCholesterol" >> salad_nutr_test/salad-nutr-$count

grep "cholesterolContent" -A 1 $file |cut -d\> -f2 -f4 |cut -d\< -f1 >> salad_nutr_test/salad-nutr-$count

echo -e "\nSodium" >> salad_nutr_test/salad-nutr-$count

grep "sodiumContent" -A 1 $file |cut -d\> -f2 -f4 |cut -d\< -f1 >> salad_nutr_test/salad-nutr-$count

echo -e "\n" >> salad_nutr_test/salad-nutr-$count

grep "Potassium" -A 2 $file |cut -d\> -f2 -f4 |cut -d\< -f1  >> salad_nutr_test/salad-nutr-$count

echo -e "\nTotal Carbohydrates" >> salad_nutr_test/salad-nutr-$count

grep "carbohydrateContent" -A 1 $file |cut -d\> -f2 -f4 |cut -d\< -f1 >> salad_nutr_test/salad-nutr-$count

echo -e "\nDietary Fiber" >> salad_nutr_test/salad-nutr-$count

grep "fiberContent" -A 1 $file |cut -d\> -f2 -f4 |cut -d\< -f1 >> salad_nutr_test/salad-nutr-$count

echo -e "\nProtein" >> salad_nutr_test/salad-nutr-$count

grep "proteinContent" -A 1 $file |cut -d\> -f2 -f4 |cut -d\< -f1 >> salad_nutr_test/salad-nutr-$count

echo -e "\nSugars" >> salad_nutr_test/salad-nutr-$count

grep "sugarContent" -A 1 $file |cut -d\> -f2 -f4 |cut -d\< -f1 >> salad_nutr_test/salad-nutr-$count

echo -e "\n" >> salad_nutr_test/salad-nutr-$count

grep "Vitamin A" -A 2 $file |cut -d\> -f2 -f4 |cut -d\< -f1  >> salad_nutr_test/salad-nutr-$count

echo -e "\n" >> salad_nutr_test/salad-nutr-$count

grep "Vitamin C" -A 2 $file |cut -d\> -f2 -f4 |cut -d\< -f1  >> salad_nutr_test/salad-nutr-$count

echo -e "\n" >> salad_nutr_test/salad-nutr-$count

grep "Calcium" -A 2 $file |cut -d\> -f2 -f4 |cut -d\< -f1  >> salad_nutr_test/salad-nutr-$count

echo -e "\n" >> salad_nutr_test/salad-nutr-$count

grep "Iron" -A 2 $file |cut -d\> -f2 -f4 |cut -d\< -f1  >> salad_nutr_test/salad-nutr-$count

echo -e "\n" >> salad_nutr_test/salad-nutr-$count

grep "Thiamin" -A 2 $file |cut -d\> -f2 -f4 |cut -d\< -f1  >> salad_nutr_test/salad-nutr-$count

echo -e "\n" >> salad_nutr_test/salad-nutr-$count

grep "Niacin" -A 2 $file |cut -d\> -f2 -f4 |cut -d\< -f1  >> salad_nutr_test/salad-nutr-$count

echo -e "\n" >> salad_nutr_test/salad-nutr-$count

grep "Vitamin B6" -A 2 $file |cut -d\> -f2 -f4 |cut -d\< -f1  >> salad_nutr_test/salad-nutr-$count

echo -e "\n" >> salad_nutr_test/salad-nutr-$count

grep "Magnesium" -A 2 $file |cut -d\> -f2 -f4 |cut -d\< -f1  >> salad_nutr_test/salad-nutr-$count

echo -e "\n" >> salad_nutr_test/salad-nutr-$count

grep "Folate" -A 2 $file |cut -d\> -f2 -f4 |cut -d\< -f1  >> salad_nutr_test/salad-nutr-$count

count=$((count+1))

done 