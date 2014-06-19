from collections import defaultdict
import pickle
import os
import math

#builds feaute vector matrix
def create_ingredient_matrix(recipe_list_dict, ingredient_frequency_dict, feature_list, useColor, color_score):

    num_recipes = len(recipe_list_dict)-1
    matrix = [[]] * num_recipes
    print len(matrix)
    print num_recipes

    for i in range(0,num_recipes):
        recipe = recipe_list_dict[i+1] #recipe_list_dict[0] is blank list
        vector = create_ingredient_vector(recipe, ingredient_frequency_dict)
        features = feature_list[i+1]
        if useColor:
             matrix[i] = features + vector + [color_score[i+1]]
        else:
            matrix[i] = features + vector
    
    return matrix
   # name = 'ingredient_vector_matrix_cleaned.pi'
    #file_pi = open(name, 'w') 
    #pickle.dump(matrix, file_pi)

#Creates ingredient vector of the form 0/1
def create_ingredient_vector(recipe, ingredient_frequency_dict):
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

#Retrieve list of ingredinets from lines 'in_file' from corresponding file at 'location'
def get_ingredient_list(in_file, location):
    booly = 0
    ingredient_list = []
    for line in in_file:

        if line == "Ingredient Amounts (grams):":
            booly = 0

        if booly == 1:
            ingredient_list.append(line)

        if line == "Ingredients:":
            #do nothing
            booly = 1
    if len(ingredient_list) >0:
        ingredient_list.pop()
    else:
        print location

    return ingredient_list

# returns features of recipe as following list [rating, num_reviews, prep_time]
def get_feature_list(in_file):
    feature_list = []
    num_reviews = 0
    rating = 0
    prep_time = 0
    marker = 0
    k =1
    for line in in_file:
        if k==3:
            rating = float(line)

        
            marker = 0
        if marker == 2:
            if line.isdigit():
                num_reviews = int(line)
            else:
                num_reviews = 0
            marker = 0
            
        if marker == 3:
            if line.isdigit():
                prep_time = int(line)
            else:
                prep_time = 0
            marker = 0
                

        if line == 'Number of Reviews:':
            marker = 2
        if line == 'Preparation Time:':
            marker = 3
        k+=1

    return [rating, num_reviews, prep_time]

# returns dictionary of ingredient frequencies
def get_ingredient_frequencies(recipe_list):
    from collections import defaultdict
    
    ingredient_frequencies = defaultdict(int)

    for i in range(1, len(recipe_list)): #note that recipe_list[0] returns blank
        for ingredient in recipe_list[i]:
            ingredient_frequencies[ingredient] += 1

    cutoff = 6
    frequencies_with_cutoff = dict()
    for item in ingredient_frequencies:
        if ingredient_frequencies[item] > cutoff:
            frequencies_with_cutoff[item] = ingredient_frequencies[item]

    return ingredient_frequencies, frequencies_with_cutoff

#retrieves nutrition information from recipe file
def get_nutrition(in_file, location):
    nutrition_dict = dict()
    
    for i in range(0,18):
        nutrition_dict[i] = -1
        
    marker = -1
    #initial gathering
    for line in in_file:

        
        if 'Fat Content' in line:
            marker = 0
        if 'Saturated Fat' in line:
            marker = 1
        if 'Cholesterol' in line:
            marker = 2
        if 'Sodium' in line:
            marker = 3
        if 'Potassium' in line:
            marker = 4
        if 'Total Carbohydrates' in line:
            marker = 5
        if 'Dietary Fiber' in line:
            marker = 6
        if 'Protein' in line:
            marker = 7
        if 'Sugars' in line:
            marker = 8
        if 'Vitamin A' in line:
            marker = 9
        if 'Vitamin C' in line:
            marker = 10
        if 'Calcium' in line:
            marker = 11
        if 'Iron' in line:
            marker = 12
        if 'Thiamin' in line:
            marker = 13
        if 'Niacin' in line:
            marker = 14
        if 'Vitamin B6' in line:
            marker = 15
        if 'Magnesium' in line:
            marker = 16
        if 'Folate' in line:
            marker = 17

        #Adding nutritional informatinon to dicitonary.
        #Note: first item in each list is the nutritional label
        if marker != -1 and '%' in line:
            percent = line.strip(' %\n')
            if 'N/A' in percent:
                nutrition_dict[marker] = -1
            else:
                nutrition_dict[marker]=float(int(percent))/100

        nutrition_list = []
        for key, value in nutrition_dict.items():
            nutrition_list.append(value)
        
            
    return nutrition_list

#Returns color score for a recipe, where 0 is monocolor, 1 is completely diverse
# Color dictionary: key is ingredient name. value is color
# recipe_list is a list
def get_color_score(ingredient_list, color_dictionary, frequency, isNormalized):

    color_vector = defaultdict(int)

    for ingredient in ingredient_list:
        if ingredient in frequency:
            color = color_dictionary[ingredient]
            if color is not ('N/A' or 'colorless'):
                color_vector[color]+=1

    total = len(ingredient_list)
    score = 0
    for key, value in color_vector.items():
        init = float(total)/value
        score += math.log(init)

    if isNormalized:
        if total !=0:
            norm = total * math.log(total)
            score = score/norm

    return score


        
        
