# salad_chef.py
# Main script that runs genetic algorithm to create new salad recipe
# By: Erol Cromwell, 2014, DRI project

#0: Import , load any modules/files we need, such as the predictor, graphs and whatnot
import pickle
import networkx as nx
from sklearn.ensemble import GradientBoostingClassifier
import centrality_measures as cm
import genetic_algorithm_defs as gad
import ingredient_networks as inet
import salad_defs

    #compliment graph
file_name = 'compliment_graph_weighted.pi'
load = open(file_name)
compliment_graph = pickle.load(load)
load.close()

    #gradient boosting learner
file_name = 'gtbs_600_estimators_3_depth_rank_60.pi'
load = open(file_name)
load_ensemble = pickle.load(load)
load.close()
gtbs = load_ensemble[0][0]

num_recipes = 100 #Number of initial random recipes to generate

rank_k = 60 #Whatever rank used in learner
list_of_ingredients = sorted(compliment_graph.nodes())
num_ingred = len(list_of_ingredients) #Official, for now
start_ingred = 0
end_ingred = num_ingred
#1: Generate random recipes
recipes = gad.generate_random_recipes(num_recipes, num_ingred)  #initial recipes set up like ingredient vectors
    #1a: Add centrality info, network community info to recipes
cmv = cm.centrality_measure_vec(compliment_graph) #To be kept outside loop

network_community = inet.create_network_community(compliment_graph, recipes, rank_k = rank_k)

feature_recipes = []
for i in range(0,len(recipes)):   
    cv = cm.centrality_vector(recipes[i][start_ingred:end_ingred], cmv)
    feature_recipes.append(recipes[i] + cv + network_community[i])

#2: Create the recipe pairs, including any feature information such as centrality and network community
recipe_pairs = salad_defs.build_recipe_pairs(matrix = feature_recipes)

#3: Use predictor to find 'top' recipes.
# probability interval for choosing parent recipe
print "recipe rankings:"
parent_probability = gad.create_parent_probabilty_interval(recipe_pairs,gtbs)

i = 0
for r in recipes:
    print 'recipe #: %d'%i
    gad.print_ingredients(r[:end_ingred], list_of_ingredients)
    i+=1
    
print '\n'
print parent_probability

#4: Create children recipes using crossovers of parent recipes

#5: Slight mutation section
