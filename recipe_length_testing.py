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


recipe_lengths = [3,6,9,12,15,18]
num_recipes = 5000 #Number of initial random recipes to generate

for length in recipe_lengths:

#Will do testing for randomly generated, and random walk
#recipes = gad.generate_random_recipes(num_recipes, num_ingred, random_walk = True,compliment_graph = compliment_graph)

    recipes = gad.generate_random_recipes(num_recipes, num_ingred, recipe_length = length)
    
    feature_recipes =  gad.build_feature_recipes(recipes, compliment_graph, rank_k,
                                         start_ingred, end_ingred, cmv)

    recipe_rankings, scores = compare_recipes( feature_known_recipes, feature_recipes,
                                                         known_ratings, num_ingred, gtbs)

    max_mean = max( [ mean for (score, mean, med, q) in recipe_rankings] )
    max_median = max( [med for (score, mean, med, q) in recipe_rankings] )

    
    print 'For recipes of length %d,'%length
    print '    Average competitions won: %f' %scores[0]
    print '    Mean competitions won: %f' %scores[2]
    print '    Max competitions won: %f'%scores[1]
    print '    Max mean rating: %f' %max_mean
    print '    Max median rating: %f' %max_median



def compare_recipes( feature_known_recipes, feature_current_recipes, known_ratings, num_ingred, gtbs):
    score_current = 0 # Average % competitions won against known recipes
    m = [] # keeping track of median % competitions won
    network_pairs = False
    compressed = True
    feature_compressed = False

    score_max = 0    #Max % score against known recipes
    recipe_rankings = [] # rankings for each current recipes

    num_known_recipes = len(feature_known_recipes)
    defeats = [0]*num_known_recipes
    always_defeated_recipes = set()
    i = 0

    #Average/ mean score of current generation
    for current in feature_current_recipes:
        c = 0
        defeated_recipes = set()
        ratings = []
        for j in range(0,num_known_recipes):

            pair = salad_defs.make_recipe_pair(current, feature_known_recipes[j], num_ingred,
                                               network_pairs, compressed, feature_compressed)
            score = gtbs.predict(pair)
            score_current += score
            c += score

            if score == 1:
                ratings.append(known_ratings[j])
            else:
                defeats[j] +=1
                defeated_recipes.add(j)


        if i==0:
            always_defeated_recipes = always_defeated_recipes | defeated_recipes
        else:
            always_defeated_recipes = always_defeated_recipes & defeated_recipes
        # For each current recipe:
#        median_rating = np.median(ratings)
#        mean_rating = np.mean(ratings)
#        percent_score = float(c) / num_known_recipes
#        recipe_rankings.append( (percent_score, mean_rating, median_rating, i) ) #i is for recipe tracking
        
#        m.append(float(c))
        
#        if c > score_max:
#            score_max = c
#            init_gen_loc = i
        i+=1
            
#    num_comp = num_known_recipes * len(feature_current_recipes)
#    percent_score = float(score_current)/num_comp
#    median_score = np.median(m) / num_known_recipes #median of percent competitions won
#    p_score_max = float(score_max)/ num_known_recipes
# recipe_rankings , (percent_score, p_score_max, median_score), 
    return defeats, always_defeated_recipes
