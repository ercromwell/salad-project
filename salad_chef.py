# salad_chef.py
# Main script that runs genetic algorithm to create new salad recipe
# By: Erol Cromwell, 2014, DRI project

#0: Import , load any modules/files we need, such as the predictor, graphs and whatnot
import pickle
import random
import copy
import networkx as nx
from sklearn.ensemble import GradientBoostingClassifier
import centrality_measures as cm
import genetic_algorithm_defs as gad
import ingredient_networks as inet
import salad_defs
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt

    #compliment graph
file_name = 'compliment_graph_weighted_v11.pi'
load = open(file_name)
compliment_graph = pickle.load(load)
load.close()

    #gradient boosting learner
file_name = 'gtbs_v11_600_estimators_3_depth_rank_60.pi'
load = open(file_name)
load_ensemble = pickle.load(load)
load.close()
gtbs = load_ensemble[0][0]

num_recipes = 100 #Number of initial random recipes to generate

num_generations = 100 #Number of generations to produce

num_reproduce = num_recipes/2 #Number of times children are produced, (number of children = 2*num_reproduce)

rank_k = 60 #Whatever rank used in learner
list_of_ingredients = sorted(compliment_graph.nodes())
num_ingred = len(list_of_ingredients) #Official, for now
start_ingred = 0
end_ingred = num_ingred

#1: Generate random recipes
    #initial recipes set up like ingredient vectors
init_recipes = gad.generate_random_recipes(num_recipes, num_ingred, random_walk = True,compliment_graph = compliment_graph)
    
    #1a: Add centrality info, network community info to recipes
cmv = cm.centrality_measure_vec(compliment_graph) #To be kept outside loop

#For comparision use
feature_init_recipes = gad.build_feature_recipes(init_recipes, compliment_graph, rank_k,
                                                 start_ingred, end_ingred, cmv)
x = []
scores = []
init_gen_max = []
same = []
current_gen_max = []

#Create copy of initial recipe generation, use later for comparision, measurement
recipes = init_recipes
feature_recipes = feature_init_recipes
final_recipes = []
final_feature_recipes=[]

s = gad.compare_recipe_generation( feature_init_recipes, feature_recipes, num_ingred, gtbs)
x.append(0)
scores.append(s[0])
init_gen_max.append(s[1])
same.append(gad.same_recipes(init_recipes))
current_gen_max.append(gad.best_score(feature_init_recipes, gtbs))

#Loop for generations
for i in range(0, num_generations):
    print i

    #2: Create the recipe pairs, including any feature information such as centrality and network community
    recipe_pairs = salad_defs.build_recipe_pairs(matrix = feature_recipes)

    #3: Use predictor to find 'top' recipes.
        #3a: recipe scoring
    recipe_score = gad.rank_recipes(recipe_pairs, gtbs)

        #3b: probability interval for choosing parent recipe
    parent_probability = gad.create_parent_probabilty_interval(recipe_score)
    

    #4: Create children recipes using crossovers of parent recipes
    children_recipes = []
    
    for j in range(0, num_reproduce):
        
        prob_1 = random.random()
        parent_1 = gad.find_interval(prob_1, parent_probability)
        
        prob_2 = random.random()
        parent_2 = gad.find_interval(prob_2, parent_probability)
        
        #Make sure parent_2 is not parent_1
        while parent_2 == parent_1:
            prob_2 = random.random()
            parent_2 = gad.find_interval(prob_2, parent_probability)

        child_1, child_2 = gad.create_children(recipes[parent_1], recipes[parent_2], num_ingred)
        children_recipes.append(child_1)
        children_recipes.append(child_2)

    #5: Slight mutation to children recipes
    gad.mutations(children_recipes)

    #6 take top parents and children, label next generation
    feature_children_recipes = gad.build_feature_recipes(children_recipes, compliment_graph,
                                                     rank_k, start_ingred, end_ingred, cmv)
    recipes, feature_recipes = gad.build_next_gen_recipes(recipes, feature_recipes, feature_children_recipes, gtbs)

    #8 Compare next_gen to first generation
    s = gad.compare_recipe_generation(feature_init_recipes, feature_children_recipes, num_ingred, gtbs)
    x.append(i+1)
    scores.append(s[0])
    init_gen_max.append(s[1])
    same.append(gad.same_recipes(recipes))
    current_gen_max.append( gad.best_score(feature_children_recipes, gtbs) )
    
    #9: Save last generation
    if i == num_generations -1:
        final_recipes = copy.copy(recipes)
        feature_final_recipes = copy.copy(feature_recipes)



#10: Display final recipes, results of improvement

final_pairs = salad_defs.build_recipe_pairs(matrix = feature_final_recipes)

final_score = gad.rank_recipes(final_pairs, gtbs)
top_5 = gad.top_n_recipes(final_score, 5)
for r in top_5:
    print 'For recipe # %d, score is: %d'% (r[1], r[0])
    gad.print_ingredients(recipes[r[1]],list_of_ingredients)



plt.plot(x,scores, label = 'Mean % competitions won')
plt.plot(x, init_gen_max, label = 'Max score on initial')
plt.plot(x, same, label = 'Same')
plt.plot(x, current_gen_max, label = 'Max for current gen')

plt.legend(loc='upper right')
plt.xlabel('generation')
plt.ylabel('percent')
plt.axis([0 ,num_generations, 0, 1.5])

plt.show()
