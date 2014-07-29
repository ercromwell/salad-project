# Created July 3rd, 2014
# By: Erol Cromwell
# Used for analysis what ingredients we have in flavor compound graph
import pickle
import networkx as nx
from collections import defaultdict
import numpy as np
from scipy import stats
def word_substitute_dictionary():
    d = dict(belgian_endive = 'chicory', crabmeat = 'crab', escarole = 'endive',
             honeydew_melon = 'honeydew', green_onion = 'scallion', garlic_clove = 'garlic',
             ginger_root = 'ginger', artichoke_heart = 'artichoke', corn_kernel = 'corn',
             red_bell_pepper = 'bell_pepper', orange_bell_pepper = 'bell_pepper',
             yellow_bell_pepper = 'bell_pepper', delicious_apple = 'apple',
             granny_smith_apple = 'apple', green_apple = 'apple', red_apple = 'apple',
             red_delicious_apple = 'apple', tart_apple = 'apple', butter_lettuce = 'lettuce',
             green_lettuce = 'lettuce', iceberg_lettuce = 'lettuce', red_lettuce = 'lettuce',
             romaine_lettuce = 'lettuce', green_cabbage = 'cabbage', napa_cabbage = 'cabbage',
             red_cabbage = 'cabbage', english_cucumber = 'cucumber', baby_pea = 'pea',
             baking_potato = 'potato', cannellini_bean = 'kidney_bean', cayenne_pepper = 'guinea_pepper',
             celery_rib = 'celery', cherry_tomato = 'tomato', baby_spinach = 'dried_spinach',
             kernel_corn = 'corn', grape_tomato = 'tomato', green_bean = 'snap_bean',
             green_grape = 'grape', red_grape = 'grape', black_olive = 'olive',
             green_olive = 'olive', kalamata_olive = 'olive', mandarin_orange = 'orange',
             mustard_powder = 'mustard', mustard_seed = 'mustard', green_chile_pepper = 'capsicum_annuum',
             red_chile_pepper = 'capsicum_annuum', jalapeno_pepper = 'capsicum_annuum',
             pineapple_juice = 'pineapple', pine_nut = 'nut', poppy_seed = 'seed',
             red_onion = 'onion',  sweet_onion = 'onion',  white_onion = 'onion',
             yellow_onion = 'onion', red_potato = 'potato', russet_potato = 'potato',
             red_pepper = 'pepper', spinach = 'dried_spinach', sugar_snap_pea = 'pea',
             vanilla_extract = 'vanilla', white_rice = 'rice', yellow_squash = 'squash',
             white_tuna = 'tuna', dill_weed = 'dill', green_pea = 'pea', roma_tomato = 'tomato',
             wax_bean = 'bean')
    return d


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

word_sub = word_substitute_dictionary()
word_sub_keys = word_sub.keys()

ingredients_in_flavor = []
not_in_flavor=[]
for ingredient in list_of_ingredients:
    if ingredient in word_sub_keys:
        sub_ingred = word_sub[ingredient]
    else:
        sub_ingred = ingredient
    
    if sub_ingred in flavor_ingredients:
        ingredients_in_flavor.append(ingredient)
    else:
        not_in_flavor.append(ingredient)

flavor_compound_network.add_nodes_from(list_of_ingredients)
print flavor_compound_network.number_of_nodes() 

pairs = 0
keys = ingredient_flavor_pair_dict.keys()
for i in range( 0, len(ingredients_in_flavor)-1 ):
    actual_ingred_1 = ingredients_in_flavor[i]
    
    if actual_ingred_1 in word_sub_keys:
        sub_ingred_1 = word_sub[ actual_ingred_1 ]
    else:
        sub_ingred_1 = actual_ingred_1

    for j in range( i, len(ingredients_in_flavor) ):
        actual_ingred_2 = ingredients_in_flavor[j]

        if actual_ingred_2 in word_sub_keys:
            sub_ingred_2 = word_sub[ actual_ingred_2 ]
        else:
            sub_ingred_2 = actual_ingred_2
            
        t1 = ( sub_ingred_1, sub_ingred_2 )
        t2 = ( t1[1], t1[0] )
        if t1 in keys:
            pairs +=1
            flavor_compound_network.add_edge( actual_ingred_1, actual_ingred_2,
                                              weight = int(ingredient_flavor_pair_dict[t1]) )
        elif t2 in keys:
            pairs +=1
            flavor_compound_network.add_edge( actual_ingred_1, actual_ingred_2,
                                               weight = int(ingredient_flavor_pair_dict[t2]) )
            
print flavor_compound_network.number_of_edges()
print flavor_compound_network.edges(data= True)[1]

#adding generic edges to ingredients not in original flavor network
mode = 1

for ingredient in not_in_flavor:
    for other_ingred in list_of_ingredients:
        if other_ingred is not ingredient:
            flavor_compound_network.add_edge(ingredient, other_ingred, weight = mode)
print flavor_compound_network.number_of_edges()

print '# ingredients not in flavor network: %d' %len(not_in_flavor)
#print not_in_flavor
print '# ingredients in flavor network: %d' %len(ingredients_in_flavor)
#print ingredients_in_flavor
print
num_total_pairs = len(list_of_ingredients) *  (len(list_of_ingredients)-1) /2
print num_total_pairs
#print pairs

file_name = 'flavor_compound_network_v2_mode.pi'
file_pi = open(file_name, 'w')
pickle.dump(flavor_compound_network, file_pi)
file_pi.close()


## file_name = 'flavor_compound_network_v2.pi'
## load = open(file_name)
## flavor_compound_network = pickle.load(load)
## load.close()

## edge_weights = [ w['weight'] for (node, neigh, w) in flavor_compound_network.edges_iter(data = True)]
## mean = float(sum(edge_weights)) / flavor_compound_network.number_of_edges()
## median = np.median(edge_weights)
## mode = stats.mode(edge_weights, axis = None)
## print mean
## print median
## print mode

        
