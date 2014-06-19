import re
import pickle
import os
# load pickled ingredient dictionary

recipe_file = 'recipe_ingredients_v3.dict'

filer = open(recipe_file, 'rb')
recipe_list_dict = pickle.load(filer)
filer.close()

ingredient_file = 'ingredient_frequencies_cleaned_cutoff_6_v3.dict'
file_i = open(ingredient_file, 'rb')
ingredient_frequency_dict = pickle.load(file_i)
print len(ingredient_frequency_dict)
file_i.close()

# need to return a vector of ones and zero

def create_ingredient_vector(recipe):
	# will be of the form ingredient:0/1
    ingredient_vec_dict = dict()
	
    for ingredient in ingredient_frequency_dict:
        if ingredient in recipe:
            ingredient_vec_dict[ingredient] = 1
        else:
            ingredient_vec_dict[ingredient] = 0
            
	master_tuple_vec = sorted(ingredient_vec_dict.items())

    
    ingredient_vec = []
    for key, value in master_tuple_vec:
		ingredient_vec.append(value)
    
    return ingredient_vec

num_recipes = len(recipe_list_dict)-1
matrix = [[]] * num_recipes
print len(matrix)
print num_recipes

for i in range(0,num_recipes):
    recipe = recipe_list_dict[i+1] #recipe_list_dict[0] is blank list
    vector = create_ingredient_vector(recipe) 
    matrix[i] = vector
   
name = 'ingredient_vector_matrix_cleaned.pi'
file_pi = open(name, 'w') 
pickle.dump(matrix, file_pi)
