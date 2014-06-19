import pickle
import math
import networkx as nx
import numpy as np

#Complement ingredient network with weighted edges using pointwise mutual information
def create_complement_network(ingredient_matrix, ingred_vec_order):

    num_recipes = len(ingredient_matrix)
    num_ingredients = len(ingredient_matrix[0])

    print 'number of recipes is: %d'%num_recipes
    print 'number of ingredients is: %d'%num_ingredients
    
    G = nx.Graph()

    #p[i] is set of recipes that contain ingredient i, used for frequencies
    p =[]
    #Constructing p
    for i in range(0, num_ingredients):
        set_of_recipes = set()
        
        for j in range(0, num_recipes):
            if ingredient_matrix[j][i] == 1:
                set_of_recipes.add(j)

        p.append(set_of_recipes)

    #check measure
    l=0
    for s in p: 
        if len(s) == 0:
            print "ingredient %d does not occur in any recipes" %l
        l+=1

    for a in range(0, num_ingredients):
        #G.add_node(a, name = ingred_vec_order[a])
        for b in range(a+1, num_ingredients):
            #G.add_node(b, name = ingred_vec_order[b])
            #intersection of sets
            intersect = p[a] & p[b]
            #Percentage of recipes that contain a and b
            percent_a_and_b = float(len(intersect))/num_recipes

            #Percentage of recipes that contain a
            percent_a = float(len(p[a])) / num_recipes
            #Percentage of recipes that contain b
            percent_b = float(len(p[b])) / num_recipes
            
            init =  percent_a_and_b / (percent_a*percent_b)
            
            if init > 1:
                pmi = math.log10(init)
                G.add_edge(ingred_vec_order[a],ingred_vec_order[b], weight = pmi)

    return G
            
# Create network community using SVD. Note: graph is a networkx Graph object
# matrix is ingredient matrix, only want to look at ingredient vectors
# rank_k is integer
def create_network_community(graph, matrix, rank_k = 0):

    W = nx.adjacency_matrix(graph)

    #Using reduced version of SVD
    U, s, V, = np.linalg.svd(W, full_matrices = False)

    if rank_k != 0:
        s = s[:rank_k]
        V = V[:rank_k]
        
    S =np.diag(s)

    inv_S = np.linalg.inv(S) #inverse of S

    network_community = []
    
    for recipe in matrix:
        ingredient_vec = np.array(recipe)
        ingredient_vec = np.reshape(ingredient_vec, (len(ingredient_vec),1))
        
        com_vec = np.dot(inv_S, np.dot(V, ingredient_vec))
        
        com_vec = np.reshape(com_vec, (1, len(com_vec)))
        com_vec = com_vec.tolist()[0]
        
        network_community.append(com_vec)


    return network_community

    
    
    





# Returns co_occurence network in form of an adjacency list, stored as a dictionary,
# where key is vertex, values are set of neighboring vertices
def create_ingredient_co_occurrence_network(filename, new_file):
    load = open(filename)
    ingredient_matrix = pickle.load(load)

    num_recipes = len(ingredient_matrix)
    num_ingredients = len(ingredient_matrix[0])

    #Graph is a dictionary, where key is the ingredient (a number), value is a set of
    # connecting vertices for ingredients. Edge exists between ingredients if
    # they occur in the same recipe
    ingredient_graph = dict()

    # Setting up graph
    for i in range(0, num_ingredients):
        s = set()
        ingredient_graph[i] = s

    #Add connecting vertices to graph for each vertice ( ingredient)
    for i in range(0, num_recipes):
        recipe = ingredient_matrix[i]
        ingredient_list = []

        for j in range(0, num_ingredients):
            ingredient = recipe[j]

            if ingredient == 1:
                ingredient_list.append(j)

        for item in ingredient_list:
            edges = [x for x in ingredient_list if x != item ] #Remove vertice from set
            ingredient_graph[item].update(edges)



    file_pi = open(new_file, 'w')
    pickle.dump(ingredient_graph, file_pi)
    

    
    
    
    


            
            

            
            
            
        
        
