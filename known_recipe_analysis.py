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

def compare_recipes( feature_known_recipes, feature_current_recipes, known_ratings, num_ingred, gtbs,
                     network_pairs = False, compressed = True, feature_compressed = False):
    score_current = 0 # Average % competitions won against known recipes

    num_known_recipes = len(feature_known_recipes)

    gain = [0]*len(feature_current_recipes) #measurement testing out
    loss = [0]*len(feature_current_recipes)
    comps_won =[0]*len(feature_current_recipes)
    new_measure = [0]*len(feature_current_recipes)
    
    wins = [0]*num_known_recipes
    defeated_recipes = set()
    successful_recipes = set()
    cutoff_losing = len(feature_current_recipes) * 0.1
    cutoff_winning =  len(feature_current_recipes) - cutoff_losing
    for j in range(0,num_known_recipes):
        
        for k in range(0, len(feature_current_recipes)):

            pair = salad_defs.make_recipe_pair( feature_known_recipes[j],feature_current_recipes[k], num_ingred,
                                               network_pairs, compressed, feature_compressed)
            score = gtbs.predict(pair)
            if score == 1:
                wins[j] +=1
                #loss[k] -= 1.0/known_ratings[j]
                new_measure[k] += known_ratings[j] - 5

            else:
                #gain[k] += known_ratings[j]
                comps_won[k]+=1
                new_measure[k] += known_ratings[j]


        if wins[j] < cutoff_losing:
            defeated_recipes.add(j)

        if wins[j] > cutoff_winning:
            successful_recipes.add(j)

    #new_measure = [ (g/5.0 + 5.0*l)/num_known_recipes for (g,l) in zip(gain, loss) ]
    new_measure = [ nm / (5.0*num_known_recipes) for nm in new_measure]
   
    comps_won = [ i/ float(num_known_recipes) for i in comps_won]
    return wins, defeated_recipes, successful_recipes, (new_measure, comps_won)

    # known recipes
load = open('feature_vector_matrix_over_5_reviews_cleaned_v11.pi')
known_matrix = pickle.load(load)
load.close()

load = open('feature_bad_recipes_all.pi')
bad_recipe_matrix = pickle.load(load)
load.close()

known_matrix+= bad_recipe_matrix


    #compliment graph
file_name = 'compliment_graph_weighted_v11.pi'
load = open(file_name)
compliment_graph = pickle.load(load)
load.close()

cmv = cm.centrality_measure_vec(compliment_graph) #To be kept outside loop

    # known network communities
load = open('compliment_network_community_v11_rank_60.pi')
network_community = pickle.load(load)
load.close()

load = open('bad_recipe_all_compliment_network_community.pi')
bad_nc = pickle.load(load)
load.close()

network_community += bad_nc

#Flavor network
load = open( 'flavor_compound_network_v2_mean.pi')
flavor_graph = pickle.load(load)
load.close()

cmv_flavor = cm.centrality_measure_vec(flavor_graph)

#Flavor community
filename = 'flavor_network_community_v2_mean_rank_80.pi'
load = open(filename)
flavor_network_community = pickle.load(load)

load = open('bad_recipe_all_flavor_network_community_mean_80.pi')
bad_fnc = pickle.load(load)
load.close()

flavor_network_community += bad_fnc

    #gradient boosting learner
file_name = 'gtbs_600_iter_depth_3_flavor_and_compliment_network_community_v2.pi'
load = open(file_name)
load_ensemble = pickle.load(load)
load.close()
gtbs = load_ensemble[0][0]


list_of_ingredients = sorted(compliment_graph.nodes())
num_ingred = len(list_of_ingredients) #Official, for now
start_ingred = 0
end_ingred = num_ingred

    # Add centrality info, network community info to recipes

feature_known_recipes = []
known_ratings = []
for i in range(0,len(known_matrix)):
    if sum(known_matrix[i][3:]) > 0:
        cv = cm.centrality_vector( known_matrix[i][3:], cmv)
        cv_flavor = cm.centrality_vector( known_matrix[i][3:], cmv_flavor)
        feature_known_recipes.append(flavor_network_community[i] + cv_flavor +
                                     network_community[i] + cv)
        known_ratings.append(known_matrix[i][0])
        
recipe_lengths = [7,8,9]
NUM_RECIPES = 600 #Number of initial random recipes to generate

cutoff = NUM_RECIPES *0.1
losing_recipes = set()
winning_recipes = set()
num_runs = 1
wins = []

new_measure = []
comps_won = []
recipes = []
for length in recipe_lengths:
    recipes += gad.generate_random_recipes(NUM_RECIPES, num_ingred, recipe_length = length)

print len(recipes)
rank_k = 60 #Whatever rank used in learner
feature_recipes_compliment =  gad.build_feature_recipes(recipes, compliment_graph, rank_k,
                                         start_ingred, end_ingred, cmv, network = True)

print len(feature_recipes_compliment[0])
flavor_rank_k = 80
feature_recipes_flavor = gad.build_feature_recipes(recipes, flavor_graph, flavor_rank_k,
                                                   start_ingred, end_ingred, cmv_flavor, network = True)
print len(feature_recipes_flavor[0])

feature_recipes = [flavor + compliment for (flavor, compliment) in
                   zip(feature_recipes_flavor, feature_recipes_compliment) ]
print len(feature_recipes[0])


wins, defeated_recipes, successful_recipes, nm = compare_recipes( feature_known_recipes, feature_recipes,known_ratings,num_ingred, gtbs, network_pairs = True, compressed = False)

i==0
if i ==0:
    losing_recipes = losing_recipes | defeated_recipes
    winning_recipes = winning_recipes | successful_recipes
else:
    losing_recipes = losing_recipes & defeated_recipes
    winning_recipes = winning_recipes & successful_recipes


new_measure = nm[0]
comps_won = nm[1]


## losing_rating = []
## winning_rating = []
## for r in losing_recipes:
##     losing_rating.append( known_ratings[r])

## for r in winning_recipes:
##     winning_rating.append( known_ratings[r] )
    
## print 'On average, # known recipes winning 90 percent: %d'%len(winning_recipes)
## print winning_recipes
## print 'ratings'
## print winning_rating

## print '\nOn average, # known recipes losing 90 percent: %d'%len(losing_recipes)
## print losing_recipes
## print 'ratings:'
## print losing_rating

print 'max score: %f'%(float(sum(known_ratings)) / (5 * len(known_ratings) ) )

## x = range(0, len(known_ratings))
## print 'random recipes with 90% wins:'
## for recipe, wins in zip(recipes,comps_won):
##     if wins >=0.9:
##         print 'score: %f'%wins
##         gad.print_ingredients(recipe, list_of_ingredients)

for score, recipe, comp in sorted( zip(new_measure, recipes, comps_won), reverse = True)[:20]:
    print 'score: %f. comps won: %f'%(score,comp)
    gad.print_ingredients(recipe, list_of_ingredients)
    

plt.figure(1)
plt.scatter(comps_won, new_measure)
plt.xlabel('% comps won')
plt.ylabel('new_measure')
plt.axis([0, 1, -1, 1 ])

plt.figure(2)
x = range(0, len(new_measure))
plt.scatter(x, new_measure)
plt.xlabel('random_recipe')
plt.ylabel('new_measure')

plt.show()
