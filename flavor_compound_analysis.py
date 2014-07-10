# Created July 3rd, 2014
# By: Erol Cromwell
# Used for analysi what ingredients we have in flavor compounf graph
import pickle
import networkx as nx
from collections import defaultdict


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

compound_sharing = 'ingredient_flavor_compounds_share.dict'
file_i = open(compound_sharing, 'rb')
ingredient_flavor_pair_dict = pickle.load(file_i)
file_i.close()


ingredients_in_flavor = []
not_in_flavor=[]
for ingredient in list_of_ingredients:
    if ingredient in flavor_ingredients:
        ingredients_in_flavor.append(ingredient)
    else:
        not_in_flavor.append(ingredient)

pairs = []
keys = ingredient_flavor_pair_dict.keys()
for i in range( 0, len(ingredients_in_flavor)-1 ):

    for j in range( i, len(ingredients_in_flavor) ):
        t1 = ( ingredients_in_flavor[i], ingredients_in_flavor[j] )
        t2 = ( t1[1], t1[0] )
        if t1 in keys or t2 in keys:
            pairs.append(t1)

        
print len(not_in_flavor)
print len(ingredients_in_flavor)
#print ingredients_in_flavor
print
num_total_pairs = len(ingredients_in_flavor) *  (len(ingredients_in_flavor)+1) /2
print num_total_pairs
print len(pairs)

        
