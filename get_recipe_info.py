from collections import defaultdict
import os
import csv
import pickle
import prep_removal_defs as pr
import recipe_info_defs as rid
from sys import argv

script, version = argv
#stored_recipes = 'salad_data'
files = os.listdir("salad_data")
print len(files)

recipe_list = defaultdict(list)
feature_list = defaultdict(list)
counter = 0
#version = 'v4' #For referencing most current list


for filey in files:

    location = 'salad_data/' + str(filey)
   # print location
    fileythis = open(location) #bad code
    fileylines = str(fileythis.read()).split('\n')

    recipe_list[counter] = rid.get_ingredient_list(fileylines, location)

    feature_list[counter] = rid.get_feature_list(fileylines)

    #nutrition_list[counter] = rid.get_nutrition(fileylines, location)
    
    fileythis.close()

    counter+=1

#Remove prep info, other stuff from recipes
filename = 'prep_word_file.txt'
set_prep_words = pr.get_prep_words(filename)

pr.remove_prep_words(recipe_list, set_prep_words)

#Get ingredient frequencies
ingredient_frequency_list, ingredient_frequency_cutoff = rid.get_ingredient_frequencies(recipe_list)

#Get color score
file = 'color_dictionary.pi'
load = open(file)
color_dict = pickle.load(load)

color_score_regular = dict()
color_score_normalized = dict()
for key, value in recipe_list.items():
    color_score_regular[key] = rid.get_color_score(value, color_dict,ingredient_frequency_cutoff, False)
    color_score_normalized[key] = rid.get_color_score(value, color_dict, ingredient_frequency_cutoff, True)



#Create feature matrix:
feature_matrix = rid.create_ingredient_matrix(recipe_list, ingredient_frequency_cutoff, feature_list, False, [])

feature_matrix_color_reg = rid.create_ingredient_matrix(recipe_list, ingredient_frequency_cutoff, feature_list, True, color_score_regular)

feature_matrix_color_norm = rid.create_ingredient_matrix(recipe_list, ingredient_frequency_cutoff, feature_list, True, color_score_normalized)

#for recipes with at least 5 reviews
feature_matrix_cutoff = []
fm_color_norm_cutoff =[]
fm_color_reg_cutoff = []
for i in range(0, len(feature_matrix)):
    if feature_matrix[i][1] >=5:
        feature_matrix_cutoff.append(feature_matrix[i])
        fm_color_norm_cutoff.append(feature_matrix_color_norm[i])
        fm_color_reg_cutoff.append(feature_matrix_color_reg[i])

print len(feature_matrix_cutoff), len(fm_color_norm_cutoff), len(fm_color_reg_cutoff)



#Printing stuff to files

#Printing feature matrix
feature_file_name = 'feature_vector_matrix_cleaned_'+version+'.pi'
open_file = open(feature_file_name, 'w')
pickle.dump(feature_matrix, open_file)
open_file.close()
#Print feature matrix w/ 5 reviews
file_name = 'feature_vector_matrix_over_5_reviews_cleaned_' + version + '.pi'
a_file = open(file_name, 'w')
pickle.dump(feature_matrix_cutoff, a_file)
a_file.close()

file_2 = 'fvm_over_5_rev_cleaned_color_norm_' + version + '.pi'
file_3 = 'fvm_over_5_rev_cleaned_color_reg_' + version + '.pi'

of_1 = open(file_2, 'w')
pickle.dump(fm_color_norm_cutoff, of_1)
of_1.close()

of_2 = open(file_3, 'w')
pickle.dump(fm_color_reg_cutoff, of_2)
of_2.close()


#print recipe dictionary
csv_name = 'full_recipe_ingredient_list_cleaned_'+version+'.csv'
writer = csv.writer(open(csv_name, 'wb'))
for key, value in recipe_list.items():
    writer.writerow([key, value])
#save recipe dictionary
dict_name = 'recipe_ingredients_'+version +'.dict'
file_pi = open(dict_name, 'w') 
pickle.dump(recipe_list, file_pi)    
file_pi.close()


#print frequencies
freq_name = 'ingredient_frequencies_cleaned_'+version+'.csv'
writer = csv.writer(open(freq_name, 'wb'))
for key, value in ingredient_frequency_list.items():
    writer.writerow([key, value])
 
#save whole dict
dict_name ='ingredient_frequencies_cleaned_'+version+'.dict'
file_pi = open(dict_name, 'w') 
pickle.dump(ingredient_frequency_list, file_pi)

#save ingredient frequencies with cutodd
name = 'ingredient_frequencies_cleaned_cutoff_6_'+version +'.dict'
name_csv = 'ingredient_frequencies_cleaned_cutoff_6_' + version+ '.csv'

#Save filtered frequency dictionary
file_pi = open(name, 'w') 
pickle.dump(ingredient_frequency_cutoff, file_pi)   
file_pi.close
#print frequencies to csv
writer = csv.writer(open((name_csv), 'wb'))
for key, value in ingredient_frequency_cutoff.items():
    writer.writerow([key, value])  
