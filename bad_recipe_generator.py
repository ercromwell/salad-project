import pickle
import random
import centrality_measures as cm
import genetic_algorithm_defs as gad
import csv
import networkx as nx
import ingredient_networks as inet

    #compliment graph
file_name = 'compliment_graph_weighted_v11.pi'
load = open(file_name)
compliment_graph = pickle.load(load)
load.close()
list_of_ingredients = sorted(compliment_graph.nodes())
num_ingred = len(list_of_ingredients)

NUM_RECIPES = 100
recipe_lengths = [6,7,8,9,10,11,12]
r = []

for length in recipe_lengths:
    recipes = gad.generate_random_recipes(NUM_RECIPES, num_ingred, recipe_length = length)
    r+= recipes

file_name = 'bad_recipes_3.pi'
file_pi = open(file_name, 'w')
pickle.dump( r, file_pi)
file_pi.close()

writer = csv.writer(open(('bad_recipes_3_list.csv'), 'wb'))
for recipe in r:
    string = gad.get_ingredient_list(recipe, list_of_ingredients)
    writer.writerow([string])  

## # Create recipe vectors for bad recipes
## file_name = 'bad_recipe_rankings_2.txt'
## text_file = open(file_name)

## bad_recipe_rankings = []

## for line in text_file:
##     string = line.strip('\n')
##     bad_recipe_rankings.append( int(string))
    
## print len(bad_recipe_rankings)

## text_file.close()


## in_file_name = 'bad_recipes_2.pi'
## in_file = open(in_file_name)
## bad_recipes = pickle.load(in_file)
## in_file.close()

## print len(bad_recipes)
## print bad_recipes[1]

## bad_recipes_vectors = []
## br = []

## for recipe, ranking in zip(bad_recipes, bad_recipe_rankings):
    
##     if ranking > 0:
##         br.append(recipe)
##         bad_recipes_vectors.append([ranking,0,0]+recipe)

## print len(bad_recipes_vectors)
## print len(bad_recipes_vectors[0])


## rank_k = 60

## network_community = inet.create_network_community(compliment_graph, br, rank_k = rank_k)
## print len(network_community)
## print len(network_community[0])


## #combine previous bad recipes together

## file_name = 'feature_bad_recipes.pi'
## load = open(file_name)
## feature_bad_recipes = pickle.load(load)
## load.close()

## file_name = 'bad_recipe_network_community.pi'
## load = open(file_name)
## network_community_all = pickle.load(load)
## load.close()

## feature_bad_recipes += bad_recipes_vectors
## network_community_all += network_community

## print len(feature_bad_recipes)
## out_file = 'feature_bad_recipes_all.pi'
## file_pi = open(out_file, 'w')
## pickle.dump(feature_bad_recipes, file_pi)
## file_pi.close()

## out_file = 'bad_recipe_all_network_community.pi'
## file_pi = open(out_file, 'w')
## pickle.dump(network_community_all, file_pi)
## file_pi.close()


