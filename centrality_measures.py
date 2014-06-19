from collections import deque
import numpy as np
import networkx as nx

# graph is a networkx Graph objct, ingredient_vector is 0/1's, centrality_vectors is list of different centrality measures,
# where each is measure is a dictionary
def centrality_vector(ingredient_vector, centrality_vectors):
    cv = []
    for measure in centrality_vectors:
        m= []
        for key, value in sorted(measure.items()): #make sure ingredients are lined up w/ correct measure
            m.append(value)
        cv.append(np.dot(ingredient_vector, m))

    return cv

# Centrality measure vectors
def centrality_measure_vec(graph):
    measures = []
    bc = nx.betweenness_centrality(graph, weight = 'weight')
    measures.append(bc)

    dc = nx.degree_centrality(graph)
    measures.append(dc)

    pagerank = nx.pagerank(graph, weight = 'weight')
    measures.append(pagerank)

    ec = nx.eigenvector_centrality(graph)
    measures.append(ec)

    return measures

# Add centrality measures to the end of feature matrix
def add_centrality(matrix, graph, start_ingred, end_ingred):
    cmv = centrality_measure_vec(graph)

    new_matrix = []
    for recipe in matrix:
        cv = centrality_vector(recipe[start_ingred:end_ingred], cmv)
        new_matrix.append(recipe + cv)

    return new_matrix

   
    

#graph is a dicitonary, keys are vertices, values are connecting edges i.e., connecting vertices
def calculate_degree_centrality(graph):
    degree_centrality= []
    norm = len(graph)-1
    
    for key in graph:
        edges = graph[key]
        degree_centrality.append(float(len(edges))/norm)

    return degree_centrality



#Algorithm from paper 'A faster Algorithm for Betweenness Centrality", used for
# unweighted graphs
# 'graph 'is an adjacency list set up as a dictionary, where keys are the
#  vertices, and values is a set of adjacent vertices
def calculate_betweenness_centrality(graph):
    betweenness_measure = { key: 0.0 for key in graph}

    for vertex in graph:
        stack = []
        # P[s] is set of predecessors of vertex s on shortest paths from 'vertex'
        predecessors = {v: [] for v in graph}

        #sigma[s] is number of shortest paths from vertex s to 'vertex' 
        sigma = {v:0 for v in graph} 
        sigma[vertex] = 1

        # d[s] is minimum length of path from vertex s to 'vertex'
        d = {v: -1 for v in graph}
        d[vertex] = 0

        queue = deque()
        queue.append(vertex)

        # Using breadth-first search to categorize predecessor path and shortest path
        while queue: #while q is not empty
            v = queue.popleft()
            stack.append(v)

            neighbor_vertices = graph[v]

            for neighbor in neighbor_vertices:
                #Is 'neighbor' found for the first time?
                if d[neighbor] < 0:
                    queue.append(neighbor)
                    d[neighbor] = d[v] + 1

                #Shortest path to 'neighbor' via vector v?
                if d[neighbor] == (d[v] + 1):
                    sigma[neighbor]+=sigma[v]
                    predecessors[neighbor].append(v)
        
        # delta[s] is pair dependency of vertex s on 'vertex'
        delta = {v:0 for v in graph}
        #stack returns vertices in order of non-increasing distance from 'vector'
        while stack:
            w = stack.pop()
            
            for v in predecessors[w]:
                fraction = (float(sigma[v])/float(sigma[w]))
                add = 1 + delta[w]
                delta[v]= delta[v] + fraction*add
             
            if w != vertex: 
                betweenness_measure[w] += delta[w]

    num_v  = len(betweenness_measure)
    normal = ((num_v-1)*(num_v-2))
    print normal
    btc = dict()
    for key, value in betweenness_measure.items():
        btc[key] = float(value)/normal #do not need to divide/multiply by 2, both cancel out
        
        
    return btc

def calculate_cosine_similarity(vector1 , vector2):
    norm1 = np.linalg.norm(vector1)
    norm2 = np.linalg.norm(vector2)
   
    return cosd

    
