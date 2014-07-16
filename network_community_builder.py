import networkx as nx
import pickle
import ingredient_networks as inet
import numpy as np
import matplotlib.pyplot as plt
import math

file_name = 'flavor_compound_network.pi'
load=open(file_name)
flavor_compound_network = pickle.load(load)
load.close()

load=open('feature_vector_matrix_over_5_reviews_cleaned_v11.pi')
feature_matrix = pickle.load(load)
load.close()

matrix = []
for vector in feature_matrix:
    matrix.append(vector[3:] )

ranks = [50,60,70,80,90,100]

for rank_k in ranks:
    nc = inet.create_network_community(flavor_compound_network, matrix, rank_k)
    print len(nc[0])
    
    file_name = 'flavor_network_community_' + str(rank_k)+'.pi'
    file_pi = open(file_name, 'w')
    pickle.dump(nc, file_pi)
    file_pi.close()

## # Analysis
## W = nx.adjacency_matrix(flavor_compound_network)
## W_norm = np.linalg.norm(W)

## #Using reduced version of SVD
## U, s, V, = np.linalg.svd(W, full_matrices = False)

## error_measure = []
## x_2 = range(1,319)
## for k in x_2:
##     s_approx = s[:k]
##     S_approx = np.diag(s_approx)
##     V_approx = V[:k]
##     U_approx = U[:, :k]

##     W_approx = np.dot(U_approx, np.dot(S_approx, V_approx))
##     error = np.linalg.norm(W_approx - W) / W_norm
##     error_measure.append(error)

## i = 0
## for value in s:
##     if value < math.pow(10,-3):
##         print i
##     i+=1
        
## x = range(0, s.shape[0] )
## plt.figure(1)
## plt.plot(x, s)
## plt.axis([0,100,0,5000])
 
## plt.figure(2)
## plt.plot(x_2, error_measure)
## plt.show()

