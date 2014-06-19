from collections import deque
import centrality_measures as cm
import pickle

#pre = open('ingredient_co_occurence_graph_unweighted.dict', 'rb')
#graph = pickle.load(pre)
#pre.close()
test_graph = dict()
test_graph[1] = set([2,3])
test_graph[2] = set([1,3,])
test_graph[3] = set([1,2,7])
test_graph[4] = set([5,6])
test_graph[5] = set([4,6])
test_graph[6] = set([4,5,7])
test_graph[7] = set([3,6,8])
test_graph[8] = set([7, 9, 12])
test_graph[9] = set([8,10,11])
test_graph[10] = set([9,11])
test_graph[11] = set([9,10])
test_graph[12] = set([8,13,14])
test_graph[13] = set([12,14])
test_graph[14] = set([12,13])
#bc = cm.calculate_betweenness_centrality(test_graph)
dg = cm.calculate_degree_centrality(test_graph)

print dg
