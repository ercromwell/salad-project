# Used to test if bias in learner towards recipes with more ingredients

import pickle
import random
import networkx as nx
from sklearn.ensemble import GradientBoostingClassifier
import centrality_measures as cm
import genetic_algorithm_defs as gad
import ingredient_networks as inet
import salad_defs
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np

def compare_recipes( feature_known_recipes, feature_current_recipes, known_ratings, num_ingred, gtbs):
    score_current = 0 # Average % competitions won against known recipes
    network_pairs = False
    compressed = True
    feature_compressed = False

    num_known_recipes = len(feature_known_recipes)
    wins = [0]*num_known_recipes
    defeated_recipes = set()
    successful_recipes = set()

    cutoff_losing = len(feature_current_recipes) * 0.1
    cutoff_winning =  len(feature_current_recipes) - cutoff_losing
    for j in range(0,num_known_recipes):
        
        for current in feature_current_recipes:

            pair = salad_defs.make_recipe_pair( feature_known_recipes[j],current, num_ingred,
                                               network_pairs, compressed, feature_compressed)
            score = gtbs.predict(pair)
            if score == 1:
                wins[j] +=1


        if wins[j] < cutoff_losing:
            defeated_recipes.add(j)

        if wins[j] > cutoff_winning:
            successful_recipes.add(j)
                
    return wins, defeated_recipes, successful_recipes

    # known recipes
load = open('feature_vector_matrix_over_5_reviews_cleaned_v11.pi')
known_matrix = pickle.load(load)
load.close()

    #compliment graph
file_name = 'compliment_graph_weighted_v11.pi'
load = open(file_name)
compliment_graph = pickle.load(load)
load.close()
    # known network communities
filename = 'compliment_network_community_v11_rank_60.pi'
load = open(filename)
network_community = pickle.load(load)

    #gradient boosting learner
file_name = 'gtbs_v11_600_estimators_3_depth_rank_60.pi'
load = open(file_name)
load_ensemble = pickle.load(load)
load.close()
gtbs = load_ensemble[0][0]


rank_k = 60 #Whatever rank used in learner
list_of_ingredients = sorted(compliment_graph.nodes())
num_ingred = len(list_of_ingredients) #Official, for now
start_ingred = 0
end_ingred = num_ingred

    # Add centrality info, network community info to recipes
cmv = cm.centrality_measure_vec(compliment_graph) #To be kept outside loop

feature_known_recipes = []
known_ratings = []
for i in range(0,len(known_matrix)):
    if sum(known_matrix[i][3:]) > 0:
        cv = cm.centrality_vector( known_matrix[i][3:], cmv)
        feature_known_recipes.append(known_matrix[i][3:] + cv + network_community[i])
        known_ratings.append(known_matrix[i][0])

length = 9
num_recipes = 500 #Number of initial random recipes to generate

cutoff = num_recipes *0.1
losing_recipes = set()
winning_recipes = set()
num_runs = 10

for i in range(0,num_runs):
    print i
    recipes = gad.generate_random_recipes(num_recipes, num_ingred, recipe_length = length)
    
    feature_recipes =  gad.build_feature_recipes(recipes, compliment_graph, rank_k,
                                         start_ingred, end_ingred, cmv)

    wins, defeated_recipes, successful_recipes = compare_recipes( feature_known_recipes,feature_recipes,
                                                                  known_ratings,num_ingred, gtbs)

    if i ==0:
        losing_recipes = losing_recipes | defeated_recipes
        winning_recipes = winning_recipes | successful_recipes
    else:
        losing_recipes = losing_recipes & defeated_recipes
        winning_recipes = winning_recipes & successful_recipes

losing_rating = []
winning_rating = []
for r in losing_recipes:
    losing_rating.append( known_ratings[r])

for r in winning_recipes:
    winning_rating.append( known_ratings[r] )
    
print 'On average, # recipes winning 90 percent: %d'%len(winning_recipes)
print winning_recipes
print winning_rating

print '\nOn average, # recipes losing 90 percent: %d'%len(losing_recipes)
print losing_recipes
print losing_rating
#x = range(0, len(known_ratings))
#l = len(known_ratings)
#d = 200
#width =0.5
#plt.figure(1)
#plt.bar(x[:d], defeats[:d],width, color = 'y')
#plt.bar(x[:d], wins[:d], width,color = 'b', bottom = defeats[:d])
#plt.scatter(x, wins, s=15)
#plt.xlabel('recipe')
#plt.ylabel('# of wins')

#plt.show()
    
    

    

    




