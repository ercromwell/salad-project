import pickle
import random
import centrality_measures as cm
import genetic_algorithm_defs as gad
import csv
import networkx as nx
import ingredient_networks as inet



filename = 'flavor_compound_network_v2_mean.pi'
load = open(filename)
flavor_graph = pickle.load(load)
load.close()

file_name = 'feature_bad_recipes_all.pi'
load = open(file_name)
feature_matrix = pickle.load(load)
load.close()

matrix = []
for recipe in feature_matrix:
    matrix.append(recipe[3:])

print len(matrix[0])

flavor_nc = inet.create_network_community(flavor_graph, matrix, rank_k = 80)

out_file = 'bad_recipe_all_flavor_network_community_mean_80.pi'
file_pi = open(out_file, 'w')
pickle.dump(flavor_nc, file_pi)
file_pi.close()
