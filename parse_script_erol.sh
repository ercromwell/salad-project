#!/bin/sh

#  parse_script_erol.sh
#  
#
#  Created by Galeota-Sprung, Jonah on 12/3/12.
#  Copyright (c) 2012 __MyCompanyName__. All rights reserved.

cd ~/Documents/Summer_Work/redo_salads

count=0
for file in `ls ~/Documents/Summer_Work/redo_salads/salad_recipes/salads-*`
do

#new name grep, should work
name=`grep "metaOpenGraphURL" $file | cut -d\/ -f5`

echo -e "\nRating: " >> salad_data/$name

grep "ratingValue" $file | cut -d\" -f4  >> salad_data/$name

echo -e "\nNumber of Reviews:" >> salad_data/$name

grep "reviewCount" $file | cut -d\" -f6  >> salad_data/$name

echo -e "\nIngredients:" >> salad_data/$name

grep "ingredient-name" $file | cut -d\> -f2 | cut -d\< -f1 >> salad_data/$name

echo -e "\nIngredient Amounts (grams):" >> salad_data/$name

grep "liIngredient" $file | cut -d\" -f6 >> salad_data/$name

echo -e "\nIngredient Amounts (various measures):" >> salad_data/$name

grep "ingredient-amount" $file | cut -d\> -f2 |cut -d\< -f1 >> salad_data/$name

echo -e "\nPreparation Time:" >> salad_data/$name

grep "totalMinsSpan" $file | cut -d\> -f3 | cut -d\< -f1 >> salad_data/$name

#echo -e "\nDirections:" >> salad_data/$name

#grep "plaincharacterwrap break" $file | cut -d\> -f3 >> salad_data/$name


echo -e "Nutrition Information:" >> salad_data/$name

echo -e "\nFat Content" >> salad_data/$name

grep "fatContent" -A 1 $file |cut -d\> -f2 -f4 |cut -d\< -f1 >> salad_data/$name

echo -e "\nSaturated Fat" >> salad_data/$name

grep "saturatedFatContent" -A 1 $file |cut -d\> -f2 -f4 |cut -d\< -f1 >> salad_data/$name

echo -e "\nCholesterol" >> salad_data/$name

grep "cholesterolContent" -A 1 $file |cut -d\> -f2 -f4 |cut -d\< -f1 >> salad_data/$name

echo -e "\nSodium" >> salad_data/$name

grep "sodiumContent" -A 1 $file |cut -d\> -f2 -f4 |cut -d\< -f1 >> salad_data/$name

echo -e "\n" >> salad_data/$name

grep "Potassium" -A 2 $file |cut -d\> -f2 -f4 |cut -d\< -f1  >> salad_data/$name

echo -e "\nTotal Carbohydrates" >> salad_data/$name

grep "carbohydrateContent" -A 1 $file |cut -d\> -f2 -f4 |cut -d\< -f1 >> salad_data/$name

echo -e "\nDietary Fiber" >> salad_data/$name

grep "fiberContent" -A 1 $file |cut -d\> -f2 -f4 |cut -d\< -f1 >> salad_data/$name

echo -e "\nProtein" >> salad_data/$name

grep "proteinContent" -A 1 $file |cut -d\> -f2 -f4 |cut -d\< -f1 >> salad_data/$name

echo -e "\nSugars" >> salad_data/$name

#grep "sugarContent" -A 1 $file |cut -d\> -f2 -f4 |cut -d\< -f1 >> salad_data/$name

echo -e "\n" >> salad_data/$name

grep "Vitamin A" -A 2 $file |cut -d\> -f2 -f4 |cut -d\< -f1  >> salad_data/$name

echo -e "\n" >> salad_data/$name

grep "Vitamin C" -A 2 $file |cut -d\> -f2 -f4 |cut -d\< -f1  >> salad_data/$name

echo -e "\n" >> salad_data/$name

grep "Calcium" -A 2 $file |cut -d\> -f2 -f4 |cut -d\< -f1  >> salad_data/$name

echo -e "\n" >> salad_data/$name

grep "Iron" -A 2 $file |cut -d\> -f2 -f4 |cut -d\< -f1  >> salad_data/$name

echo -e "\n" >> salad_data/$name

grep "Thiamin" -A 2 $file |cut -d\> -f2 -f4 |cut -d\< -f1  >> salad_data/$name

echo -e "\n" >> salad_data/$name

grep "Niacin" -A 2 $file |cut -d\> -f2 -f4 |cut -d\< -f1  >> salad_data/$name

echo -e "\n" >> salad_data/$name

grep "Vitamin B6" -A 2 $file |cut -d\> -f2 -f4 |cut -d\< -f1  >> salad_data/$name

echo -e "\n" >> salad_data/$name

grep "Magnesium" -A 2 $file |cut -d\> -f2 -f4 |cut -d\< -f1  >> salad_data/$name

echo -e "\n" >> salad_data/$name

grep "Folate" -A 2 $file |cut -d\> -f2 -f4 |cut -d\< -f1  >> salad_data/$name



count=$((count+1))

done 
