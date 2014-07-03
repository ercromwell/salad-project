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

    # known recipes
load = open('feature_vector_matrix_over_5_reviews_cleaned_v11.pi')
known_matrix = pickle.load(load)
load.close()

    #compliment graph
file_name = 'compliment_graph_weighted_v11.pi'
load = open(file_name)
compliment_graph = pickle.load(load)
load.close()

list_of_ingredients = sorted(compliment_graph.nodes())

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


recipe_lengths = [9]
num_recipes = 100 #Number of initial random recipes to generate
recipes =[]
for length in recipe_lengths:

#Will do testing for randomly generated, and random walk
    recipes = gad.generate_random_recipes(num_recipes, num_ingred, random_walk = True,
                                          compliment_graph = compliment_graph, recipe_length = length)

   # recipes = gad.generate_random_recipes(num_recipes, num_ingred, recipe_length = length)
    
    feature_recipes =  gad.build_feature_recipes(recipes, compliment_graph, rank_k,
                                         start_ingred, end_ingred, cmv)

    recipe_rankings, scores = gad.compare_recipe_generation( feature_known_recipes, feature_recipes,
                                                         known_ratings, num_ingred, gtbs)
    ms_recipe = max( [(score, q) for (score, mean, med, q) in recipe_rankings] )
    max_mean = max( [ (mean, q) for (score, mean, med, q) in recipe_rankings] )
    
    max_median = max( [ (med, q) for (score, mean, med, q) in recipe_rankings] )

    
    print 'For recipes of length %d,'%length
    print '    Average competitions won: %f' %scores[0]
    gad.print_ingredients(recipes[ms_recipe[1]], list_of_ingredients)
    print '    Mean competitions won: %f' %scores[2]
    print '    Max competitions won: %f'%scores[1]
    print
    print '    Max mean rating: %f' %max_mean[0]
    gad.print_ingredients(recipes[max_mean[1]] ,list_of_ingredients)
    print
    print '    Max median rating: %f' %max_median[0]
    gad.print_ingredients(recipes[max_median[1]] ,list_of_ingredients)

    

