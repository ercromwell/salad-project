# List of methods:
#def generate_random_recipes : Create initial recipe population. Can be completely random or based on random walk
#def random_graph_walk : Random walk on compliment graph to create intitial recipe population
#def rank_recipes : 

import random
import networkx
from collections import defaultdict
import ingredient_networks as inet
import centrality_measures as cm
import numpy as np
import salad_defs
import math

# Generates random recipes for fitness function to evaluate
# Need to establish what the length of the recipes generated should be, look into average length of recipe
# Use initial length of 8
# DO i just randomly choose ingredients, or choose based on some weight, probability??????
# length_range is touple and or list, first entry is lower bound, second boundary is upper bound
def generate_random_recipes( num_recipes, num_ingred, random_walk = False, compliment_graph=[],  recipe_length = 8):
    recipe_list = []

    #intiial starting length for recipes, mean length of recipes
    #recipe_length = 8
    
    for i in range(0, num_recipes):

        # Creating ingredient list using random walk
        if random_walk:
            ingredients = random_graph_walk(compliment_graph, num_ingred, recipe_length)
        #Randomly generating ingredient list
        else:
            ingredients = random.sample(range(0,num_ingred), recipe_length)


        
        ingred_vec = [0]*num_ingred
        for ingred in ingredients:
            ingred_vec[ingred] = 1
    
        recipe_list.append(ingred_vec)

    return recipe_list

#Returns  list of ingredients by doing a random walk on the compliment graph
def random_graph_walk(compliment_graph, num_ingred, recipe_length):
    start = random.randint(0,num_ingred-1)
    
    list_of_nodes = sorted(compliment_graph.nodes())
    current_ingred = list_of_nodes[start] #string

    #Set to make sure we use each ingredient only once
    set_nodes = set()
    set_nodes.add(start)

    #list of ingredients 
    ingredients = [start]
    
    #Generating ingredient list
    while len(ingredients) < 8:

        #Create probabilites for random walk
        neighbors = compliment_graph.neighbors(current_ingred)
        interval = [0.0] #interval will be probability intervals
        for n in neighbors:
            w = compliment_graph[current_ingred][n]['weight']
            interval.append(w)

        total = sum(interval)

        #Create probability intervals
        for i in range(1, len(interval)):
            interval[i] = interval[i]/total + interval[i-1]

        # Random walk
        walk = random.random()

        next_ingred = find_interval(walk, interval)

        current_ingred = neighbors[next_ingred]
        add_ingred = list_of_nodes.index(current_ingred)
                
        if add_ingred not in set_nodes:
            ingredients.append(add_ingred)
            set_nodes.add(add_ingred)
            
        
      
    return ingredients
# Rank recipes against each other, score is number of competitions a recipe wins
def rank_recipes(recipe_pairs, gtbs):
    recipe_score = defaultdict(int)

    #First two entries represent which recipes compose pair, denoted by an integer
    for pair in recipe_pairs:
        first = pair[0]
        second = pair[1]
        
        p = gtbs.predict(pair[2:])

        if p == 1:
            recipe_score[first] += 1
            recipe_score[second] += 0
        else:
            recipe_score[second] += 1
            recipe_score[first] += 0

    return recipe_score

# Create probability intervals to choose parents, based on scores
# recipe_score is a list
def create_parent_probabilty_interval(recipe_score):
    
    total = sum(recipe_score)
    parent_prob = [0.0]

    #testing
    pr = 0
    
    for recipe in range(0, len(recipe_score)):
        
        parent_prob.append( float(recipe_score[recipe])/total  + parent_prob[recipe] )

    return parent_prob

#Print ingredients in recipe
def print_ingredients(recipe_vec, list_of_ingredients):
    list = []

    for i in range(0,len(recipe_vec)):
        if recipe_vec[i] == 1:
            list.append(list_of_ingredients[i])

    print list

#Find where walk lies in probability intervals, choosing parent
def find_interval(random_num, prob_interval):
    interval = -1 
    location = 0 # current interval location
    while interval < 0:
            #Check measure
            if location == len(prob_interval)-1:
                print 'You did not find the interval'

            if  random_num < prob_interval[location+1]:
                interval = location
            else:
                location += 1

    return interval
#### Methods for bulding children recipes

# Create children recipes given two recipes, by splitting somewhere randomly
def create_children(recipe_1, recipe_2, num_ingred):
    #find first, last location for ingredient
    def first_last(recipe):
        if 1 not in recipe:
            first = 0
        else:
            first = recipe.index(1)
        last = 1
        for i in range(0,len(recipe)):
            if recipe[i] == 1:
                last = i
        return first, last


    first_1, last_1 = first_last(recipe_1)
    first_2, last_2 = first_last(recipe_2)
    
    f=first_1
    l=last_1

    if f > first_2:
        f = first_2

    if l < last_2:
        l = last_2

    split = random.randint(f+1 ,l-1) #forced crossover

    child_1 = recipe_1[:split] + recipe_2[split:]
    child_2 = recipe_2[:split] + recipe_1[split:]

    return child_1, child_2

def build_feature_recipes(recipes, compliment_graph, rank_k, start_ingred, end_ingred, cmv):

    network_community = inet.create_network_community(compliment_graph, recipes, rank_k = rank_k)

    feature_recipes = []
    for i in range(0,len(recipes)):   
        cv = cm.centrality_vector(recipes[i][start_ingred:end_ingred], cmv)
        feature_recipes.append(recipes[i] + cv + network_community[i])

    return feature_recipes

# returns top n ranked recipes
def top_n_recipes(recipe_score, n):

    pairs = [ (score, recipe) for (recipe, score) in recipe_score.iteritems() ]
    
    s = sorted(pairs, reverse = True)

    top = s[:n]

    return top
            
    
# Returns bottom n ranked recipes
def bottom_n_recipes(recipe_score, n):
    pairs = [ (score,recipe) for (recipe, score) in recipe_score.iteritems() ]

    s = sorted(pairs)

    bottom = s[:n]

    return bottom

# Random(for now) mutations to children recipes
def mutations(children_recipes):

    mutation_chance = 0.10
    prob_add = 0.3333
    prob_remove = 0.66667
    prob_sub = 1
    
    for child in children_recipes:

        if sum(child) != 0: #check measure
            mutate = random.random()

            if mutate < mutation_chance: # mutation occurs
                t = random.random()
                if t <= prob_add:
                    add_ingredient(child)
                elif t > prob_add and t <= prob_remove:
                    remove_ingredient(child)
                else:
                    substitute_ingredient(child)            


#random for now, recipe is lsit aka mutable
def add_ingredient(recipe):

    no_ingred = []
    for i in range(0, len(recipe)):
        if recipe[i] == 0:
            no_ingred.append(i)

    new_ingred = random.sample(no_ingred, 1)[0]

    recipe[new_ingred] = 1

#random for now
# recipe is list
def remove_ingredient(recipe):
    ingred = []

    for i in range(0, len(recipe)):
        if recipe[i] == 1:
            ingred.append(i)
    remove_ingred = random.sample(ingred, 1)[0]

    recipe[remove_ingred] = 0

#random for now, recipe is list
def substitute_ingredient(recipe):
    ingred = []
    no_ingred = []
    
    for i in range(0, len(recipe)):
        if recipe[i] == 1:
            ingred.append(i)
        else:
            no_ingred.append(i)

    remove_ingred = random.sample(ingred, 1)[0]
    add_ingred = random.sample(no_ingred, 1)[0]

    recipe[remove_ingred] = 0
    recipe[add_ingred] = 1

# Used to compare current generation of recipes to known recipes
# feature_known_recipse contains full features, known_ratings has ratings, correspond to recipe in feature_known_recipes
def compare_recipe_generation( feature_known_recipes, feature_current_recipes, known_ratings, num_ingred, gtbs):
    score_current = 0 # Avereage % competitions won against known recipes
    m = [] # keeping track of median % competitions won
    network_pairs = False
    compressed = True
    feature_compressed = False

    score_max = 0    #Max % score against known recipes
    recipe_rankings = [] # rankings for each current recipes

    num_known_recipes = len(feature_known_recipes)
    i = 0

    #Average/ mean score of current generation
    for current in feature_current_recipes:
        c = 0
        ratings = []
        for j in range(0,num_known_recipes):

            pair = salad_defs.make_recipe_pair(current, feature_known_recipes[j], num_ingred,
                                               network_pairs, compressed, feature_compressed)
            score = gtbs.predict(pair)
            score_current += score
            c += score

            if score == 1:
                ratings.append(known_ratings[j])

        # For each current recipe:
        median_rating = np.median(ratings)
        mean_rating = np.mean(ratings)
        percent_score = float(c) / num_known_recipes
        recipe_rankings.append( (percent_score, mean_rating, median_rating, i) ) #i is for recipe tracking
        
        m.append(float(c))
        
        if c > score_max:
            score_max = c
#            init_gen_loc = i
        i+=1
            
    num_comp = num_known_recipes * len(feature_current_recipes)
    percent_score = float(score_current)/num_comp

    median_score = np.median(m) / num_known_recipes #median of percent competitions won

    p_score_max = float(score_max)/ num_known_recipes
    
    return recipe_rankings , (percent_score, p_score_max, median_score)


def same_recipes(recipes):
    num_same = set()

    for i in range(0, len(recipes)):
        for j in range(i+1, len(recipes)):
            if recipes[i] == recipes[j]:
                num_same.add(i)
                num_same.add(j)
        
    return float(len(num_same))/len(recipes)
    
def best_score(feature_recipes, gtbs):
    pairs = salad_defs.build_recipe_pairs(matrix = feature_recipes)
    r = rank_recipes(pairs, gtbs)
    best = top_n_recipes(r, 1)
    for score, r in best:
        t = score

    return float(t)/len(feature_recipes)

#Return next generation of recipes, choosing top recipes from parents and children 
def build_next_gen_recipes(recipes, feature_recipes, feature_children_recipes, gtbs):
      
    #7: create next generation
    all_feature_recipes = feature_children_recipes + feature_recipes
    all_pairs = salad_defs.build_recipe_pairs(matrix = all_feature_recipes)
    all_score = rank_recipes(all_pairs, gtbs)
    top_recipes = top_n_recipes(all_score, len(recipes))

    tr = []
    fr = []
    for score, recipe in top_recipes:
        tr.append(all_feature_recipes[recipe][:len(recipes[0])])
        fr.append(all_feature_recipes[recipe])
    
    return tr,
#Choose top n unique recipes from a set of recipes, returns the recipe vector
def top_unique_n_recipes(recipe_score, recipes, num_recipes):

    pairs = [ (score, recipe) for (recipe, score) in recipe_score.iteritems() ]
    
    s = sorted(pairs, reverse = True)

    top_unique = []
    recipe_set = set()
    
    i = 0 #iterator
    while len(top_unique) < num_recipes:
        r = s[i][1] #recipe id
        t = tuple(recipes[r])
        if t not in recipe_set: #test to see if its items in list, and not the list pointer
            top_unique.append(recipes[r])
            recipe_set.add(t)

        i+=1

    return top_unique

#Diversity measurement, based on equation from paper "Measurement of Population Diversity"
#, by Ronald W. Morrison and Kenneth A. De Jong
def diversity_measure(recipes):
    population_size = len(recipes)

    #Find centroid
    m = np.array(recipes)
    centroid = np.sum(m, axis = 0) / float(population_size) 
    
    #Calculate measure
    dm = 0
    for recipe in m:
        for coord in range(0, len(recipe)):
            c = recipe[coord] - centroid[coord]
            dm += pow(c,2) 

    return dm/ float(len(recipes))

#From paper "Maintaining Diversity in Genetic Search" by Michael L. Mauldin
# Has to have distance from ALL recipes
# k, current_gen, total_gen are ints
# Returns recipes satisfying diversity requirement. The requirement is that a recipe has
# to satisfy the hamming distance for ALL recieps
def unique_recipes(recipes, k, current_gen, total_gen):

    unique = []
    
    bit_decrease = linear_bit_decrease(k, total_gen, current_gen)
    not_satisfy = set()
    for i in range(0, len(recipes)):
        if sum(recipes[i]) != 0: #Safety check
            if i not in not_satisfy:
                if satisfy_uniqueness(i, i+1, recipes, bit_decrease, not_satisfy):
                    unique.append(recipes[i])

    return unique

#Recursive function. Returns true if recipe satisfies hamming distance condition for all recipes
def satisfy_uniqueness(i, j, recipes, bit_decrease, not_satisfy):

    if j >= len(recipes):
        return True

    if hamming_distance(recipes[i], recipes[j]) > bit_decrease:
        return satisfy_uniqueness(i, j+1, recipes , bit_decrease, not_satisfy)
    else:
        not_satisfy.add(j)
        return False
    

# k = initial bit_length
# n = total number of generations/trial
# t = current gen/ trial
def linear_bit_decrease(k, n, t):
    return   math.ceil( k*(n - t)/ float(n) )
    
#From wikipedia page on Hamming distance
def hamming_distance(s1, s2):
    #Return the Hamming distance between equal-length sequences
    if len(s1) != len(s2):
        raise ValueError("Undefined for sequences of unequal length")
    
    return sum(ch1 != ch2 for ch1, ch2 in zip(s1, s2))

#NOTE: recipes are sorted, based on scoring from highest to lowest
# Filters recipes based on hamming distance diversity requirement. Proceeds similar to a
# crowding factor, by adding highest ranked recipes first, and then filtering out lower ranked
# recipes that are similar
def diversity_filter(recipe_rankings, recipes, k, current_gen, total_gen):
    diverse_rankings = []
    bit_decrease = linear_bit_decrease(k, total_gen, current_gen)

    
    for ranking in recipe_rankings:
    #Add highest ranked recipe to list first
        if not diverse_rankings:
            diverse_rankings.append(ranking)
    #For all other recipes
        else:
            j=0
            recipe = recipes[ ranking[3] ]
            if satisfy_uniqueness_version_2(recipe, j, diverse_rankings, recipes, bit_decrease):
                diverse_rankings.append(ranking)

    return diverse_rankings
                  
#For function diversity_filter
def satisfy_uniqueness_version_2(recipe, j, diverse_rankings, recipes, bit_decrease):

    if j >= len(diverse_rankings):
        return True
    
    diverse_recipe = recipes[ diverse_rankings[j][3] ]
    if hamming_distance(recipe, diverse_recipe) > bit_decrease:
        return satisfy_uniqueness_version_2(recipe, j+1 , diverse_rankings, recipes, bit_decrease)
    else:
        return False
