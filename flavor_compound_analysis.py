# Created July 3rd, 2014
# By: Erol Cromwell
# Used for analysis what ingredients we have in flavor compound graph
import pickle
import networkx as nx
from collections import defaultdict

def word_substitute_dictionary:
    d = dict()
    d['belgian_endive'] = 'chicory'
    d['crabmeat'] = 'crab'
    d['escarole'] = 'endive'


 #compliment graph
file_name = 'compliment_graph_weighted_v11.pi'
load = open(file_name)
compliment_graph = pickle.load(load)
load.close()

list_of_ingredients = sorted(compliment_graph.nodes())

flavor_list = 'list_of_ingredients_from_flavor.pi'
file_j = open(flavor_list)
flavor_ingredients = pickle.load(file_j)
file_j.close()
print len(flavor_ingredients)

compound_sharing = 'ingredient_flavor_compounds_share.dict'
file_i = open(compound_sharing, 'rb')
ingredient_flavor_pair_dict = pickle.load(file_i)
file_i.close()

flavor_compound_network = nx.Graph() #for flavor compound network

ingredients_in_flavor = []
not_in_flavor=[]
for ingredient in list_of_ingredients:
    if ingredient in flavor_ingredients:
        ingredients_in_flavor.append(ingredient)
    else:
        not_in_flavor.append(ingredient)

flavor_compound_network.add_nodes_from(list_of_ingredients)
print flavor_compound_network.number_of_nodes() 

pairs = []
keys = ingredient_flavor_pair_dict.keys()
for i in range( 0, len(ingredients_in_flavor)-1 ):
    for j in range( i, len(ingredients_in_flavor) ):
        t1 = ( ingredients_in_flavor[i], ingredients_in_flavor[j] )
        t2 = ( t1[1], t1[0] )
        if t1 in keys:
            pairs.append(t1)
            flavor_compound_network.add_edge( t1[0], t1[1], weight = int(ingredient_flavor_pair_dict[t1]) )
        elif t2 in keys:
            pairs.append(t1)
            flavor_compound_network.add_edge( t1[0], t1[1], weight = int(ingredient_flavor_pair_dict[t2]) )
            
print flavor_compound_network.number_of_edges()
print flavor_compound_network.edges()[1]
    
print '# ingredients not in flavor network: %d' %len(not_in_flavor)
#print not_in_flavor
print '# ingredients in flavor network: %d' %len(ingredients_in_flavor)
#print ingredients_in_flavor
print
num_total_pairs = len(ingredients_in_flavor) *  (len(ingredients_in_flavor)+1) /2
print num_total_pairs
print len(pairs)

file_name = 'flavor_compound_network.pi'
file_pi = open(file_name, 'w')
pickle.dump(flavor_compound_network, file_pi)
file_pi.close()

        
