from collections import deque
import centrality_measures as cm
import numpy as np

# matrix : the feature vector matrix( has ratings, num-reviews, preptime in front)
# network_community : network_community vectors, if constructing pairs using them
# network_pairs : whether constructing pairs using the network community. Set to false if not using network community
# number_ingredients : length of ingredient vector
# ingredient_end : where ingredient vector ends in feature vector, with respect ot matrix
# feature_compress : whether to compress feature measures, such as centrality or color. If including no features, set to false
# compressed : whether to compress ingredient/network vectors

def get_pairs_cosine_threshold(matrix = [], network_community = [], network_pairs = False, num_ingredients = 319,
                               ingredient_end =322, feature_compressed = False, compressed = True ):
    
    cos_sim_pairs_over = []
    y_vector_over = []

    cos_sim_pairs_under = []
    y_vector_under = []
    l=0
    for i in range(0,len(matrix)):

        v1 = matrix[i][3:ingredient_end]
            
        norm1 = np.linalg.norm(v1)

        if norm1 == 0:
            print "recipe number %d has no ingredients"%(i+1)
        else:       
            for j in range(i+1, len(matrix)):

                v2 = matrix[j][3:ingredient_end]
              
                norm2 = np.linalg.norm(v2)
                
                if norm2 !=0:
                    dot = np.dot(v1,v2)
                    cosine_measure = float(dot)/(norm1*norm2)
                    
                    #making recipe pair, determined whether using matrix or network community
                    if network_pairs:
                        recipe_pair = make_recipe_pair(network_community[i], network_community[j], len(network_community[j])-4
                                                       , network_pairs, compressed, feature_compressed)
                    else:
                        recipe_pair = make_recipe_pair(matrix[i][3:], matrix[j][3:], num_ingredients, network_pairs,
                                                       compressed, feature_compressed,)

                    if l == 0:
                        print len(recipe_pair)
                        l=3
                    if cosine_measure <= 0.2: #For getting pairs less than 0.2 similarity
                        if matrix[i][0] > matrix[j][0]:
                            y_vector_under.append(1)
                            cos_sim_pairs_under.append(recipe_pair)
                        elif matrix[i][0] < matrix[j][0]:
                            y_vector_under.append(0)
                            cos_sim_pairs_under.append(recipe_pair)
                    else: #For getting paurs above 0.2 similarity
                        if matrix[i][0] > matrix[j][0]:
                            cos_sim_pairs_over.append(recipe_pair)
                            y_vector_over.append(1)
                        elif matrix[i][0] < matrix[j][0]:
                            cos_sim_pairs_over.append(recipe_pair)
                            y_vector_over.append(0)
                        
    return cos_sim_pairs_over, y_vector_over, cos_sim_pairs_under, y_vector_under

# Makes recipe pair to feed to learner
def make_recipe_pair(recipe1, recipe2, num_ingred, network_pairs, compressed, feature_compressed):
    if compressed:
        if feature_compressed:
            recipe_pair = compress(recipe1, recipe2, num_ingred, network_pairs)
        else:
            recipe_pair = compress(recipe1[:num_ingred], recipe2[:num_ingred], num_ingred, network_pairs) + recipe1[num_ingred:] + recipe2[num_ingred:]
    else:
        recipe_pair = recipe1[:num_ingred] + recipe2[:num_ingred] + recipe1[num_ingred:] + recipe2[num_ingred:]
    
    return recipe_pair
        
#Compress feature vectors
def compress(recipe1, recipe2, num_ingred, network_pairs):
    compressed= []

    if network_pairs:
        for i in range(0, num_ingred):
            compressed.append(recipe1[i]-recipe2[i])
    else:
        for i in range(0, num_ingred):
            if recipe1[i] == recipe2[i]:
                compressed.append(recipe1[i] + recipe2[i])
            else:
                compressed.append(recipe1[i] - recipe2[i])

    for j in range(num_ingred, len(recipe1)):
        compressed.append(recipe1[j]-recipe2[j])
  
    
    return compressed



#This excludes the features rating, numreviews, prep time
#For use in salad_chef.py, specifically, to build recipe pairs to give to ensemble for testing
# pairs have i,j attached to front to track which pairs are which
def build_recipe_pairs(matrix = [], num_ingredients = 319, feature_compressed = False,
                        compressed = True ):

    pairs =[]
    network_pairs = False

    for i in range(0,len(matrix)):
        for j in range(i+1, len(matrix)):              
                   
            recipe_pair = make_recipe_pair(matrix[i], matrix[j], num_ingredients,
                                           network_pairs , compressed,
                                           feature_compressed,)
            pairs.append([i]+[j]+recipe_pair)
                        
    return pairs


# Shows mean accuracy and exact accuracy of bagged trees in ensemble,
# using test features Xtest and ytest
def show_things(ensemble, Xtest, ytest , isTree, isLoaded):
    t=1
    for e in ensemble:
        #Mean accuracy of trees
        if isTree:
            x = e[0].score(Xtest,ytest)
        else:
            if isLoaded:
                x = e[0].score(Xtest, ytest)
            else:
                x = e.score(Xtest , ytest)
        print "score of tree %d: %s" %(t,str(x))
        
        t+=1
    return

#Returns accuracy of bagged trees, used for multiple bagged trees/learners
def predict_bagged_score(ensemble , Xtest , ytest , isTree):
    cutoff = len(ensemble)/2
    y_predict = []
    
    for vector in Xtest:
        total = 0
        for e in ensemble:
            if isTree:
                p = e[0].predict(vector)
            else:
                p = e.predict(vector)
            total = total + p
        output = total > cutoff

        y_predict.append(output)

    accuracy = 0

    for i in range(0, len(y_predict)):
        prediction = y_predict[i]
        exact = ytest[i]
        if exact == prediction:
            accuracy+=1
        
    percent = float(accuracy) / float(len(y_predict))
            
    return percent


