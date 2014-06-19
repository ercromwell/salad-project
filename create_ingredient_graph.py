import pickle
import networkx as nx
import ingredient_networks as inet
import matplotlib.pyplot as plt
import numpy as np
file_name = 'feature_vector_matrix_over_5_reviews_cleaned_v5.pi'
load = open(file_name)
matrix = pickle.load(load)
load.close()

graph_file = 'compliment_graph_weighted.pi'
load = open(graph_file)
graph = pickle.load(load)
print len(graph.nodes())

ingredient_matrix = []

for i in range(0, len(matrix)):
    ingredient_matrix.append(matrix[i][3:])

W = nx.adjacency_matrix(graph)

list = [55,60,65, 70]

for k in list:
    
    network_community = inet.create_network_community(graph, ingredient_matrix, rank_k = k)

    print "Number of vectors is: %d"%len(network_community)
    print "Number of entries is: %d"%len(network_community[0])

    out_file = 'compliment_network_community_rank_'+str(k)+'.pi'
    file_pi = open(out_file, 'w')
    pickle.dump(network_community, file_pi)
    file_pi.close()


        
        
        
