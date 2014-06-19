#Used to get ingredient frequencies 

from collections import defaultdict
import os
import glob
import csv
import pickle

filename = 'recipe_ingredients_v3.dict'
file = open(filename, 'rb')
recipe_list = pickle.load(file) # recipe_list[0] is blank, will skip
file.close()

ingredient_frequencies = defaultdict(int)

for i in range(1, len(recipe_list)):
    for ingredient in recipe_list[i]:
            ingredient_frequencies[ingredient] += 1
    
        
#print frequencies
writer = csv.writer(open('ingredient_frequencies_cleaned_v3.csv', 'wb'))
for key, value in ingredient_frequencies.items():
    writer.writerow([key, value])
 
#save whole dict 
file_pi = open('ingredient_frequencies_cleaned_v3.dict', 'w') 
pickle.dump(ingredient_frequencies, file_pi)    

#filter dict and save:
cutoff = 6
frequencies_with_cutoff = dict()
for item in ingredient_frequencies:
    if ingredient_frequencies[item] > cutoff:
        frequencies_with_cutoff[item] = ingredient_frequencies[item]

name = 'ingredient_frequencies_cleaned_cutoff_' +str(cutoff) + '_v3.dict'
name_csv = 'ingredient_frequencies_cleaned_cutoff_' +str(cutoff) + '_v3.csv'

#Save filtered dictionary
file_pi = open(name, 'w') 
pickle.dump(frequencies_with_cutoff, file_pi)   

#print frequencies to csv
writer = csv.writer(open((name_csv), 'wb'))
for key, value in frequencies_with_cutoff.items():
    writer.writerow([key, value])  
    
