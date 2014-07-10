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

file_name = 'bad_recipe_rankings.txt'
load = open(file_name)
bad_recipe_rankings = []
for line in load:
    string = line.strip('\n')
    bad_recipe_rankings.append( int(string))
    
print len(bad_recipe_rankings)

load.close()


in_file_name = 'bad_recipes.pi'
in_file = open(in_file_name)
bad_recipes = pickle.load(in_file)
in_file.close()

print len(bad_recipes)
print bad_recipes[1]

bad_recipes_vectors = []
br = []

for recipe, ranking in zip(bad_recipes, bad_recipe_rankings):
    
    if ranking > 0:
        br.append(recipe)
        bad_recipes_vectors.append([ranking,0,0]+recipe)

print len(bad_recipes_vectors)
print len(bad_recipes_vectors[0])


rank_k = 60

network_community = inet.create_network_community(compliment_graph, br, rank_k = rank_k)
print len(network_community)
print len(network_community[0])

out_file = 'bad_recipe_network_community.pi'
file_pi = open(out_file, 'w')
pickle.dump(network_community, file_pi)
file_pi.close()


out_file = 'feature_bad_recipes.pi'
file_pi = open(out_file, 'w')
pickle.dump(bad_recipes_vectors, file_pi)
file_pi.close()




