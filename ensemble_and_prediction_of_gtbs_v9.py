# Based on code by: Jonah Galeota-Sprung, 2012
# Edited by: Erol Cromwell, 2014
# This version used for compliment network communities and flavor network communities
# Including bad recipes
# Created: July 16th, 2014

from sklearn.ensemble import GradientBoostingClassifier
import pickle
import math
from random import randint
from sklearn import tree
import salad_defs
from sklearn.cross_validation import train_test_split
from sys import argv
import numpy as np
import networkx as nx
import centrality_measures as cm

script , isTree, num = argv

isLoaded = False

num_learners = int(num)
load = open('feature_vector_matrix_over_5_reviews_cleaned_v11.pi')
matrix = pickle.load(load)
load.close()

load = open('feature_bad_recipes_all.pi')
bad_recipe_matrix = pickle.load(load)
load.close()

matrix+= bad_recipe_matrix

num_ingred = len(matrix[0])-3
start_ingred = 3
end_ingred = num_ingred + start_ingred

filename = 'flavor_compound_network_v2_mean.pi'
load = open(filename)
flavor_graph = pickle.load(load)
load.close()

cmv_flavor = cm.centrality_measure_vec(flavor_graph)

filename = 'flavor_network_community_v2_mean_rank_80.pi'
load = open(filename)
flavor_network_community = pickle.load(load)

load = open('bad_recipe_all_flavor_network_community_mean_80.pi')
bad_fnc = pickle.load(load)
load.close()

flavor_network_community += bad_fnc

filename = 'compliment_graph_weighted_v11.pi'
load = open(filename)
compliment_graph = pickle.load(load)
load.close()

cmv_compliment = cm.centrality_measure_vec(compliment_graph)

filename = 'compliment_network_community_v11_rank_60.pi'
load = open(filename)
compliment_network_community = pickle.load(load)

load = open('bad_recipe_all_compliment_network_community.pi')
bad_cnc = pickle.load(load)
load.close()

compliment_network_community += bad_cnc

network_community = []
for i in range(0,len(matrix)):   
    cv_flavor = cm.centrality_vector( matrix[i][start_ingred:end_ingred], cmv_flavor)
    cv_compliment = cm.centrality_vector( matrix[i][start_ingred:end_ingred], cmv_compliment)
    network_community.append( flavor_network_community[i] + cv_flavor +
                              compliment_network_community[i] + cv_compliment)
    
print len(network_community[0])



print "Constructing pairs..."
recipe_pairs, y_vector, X_under, y_under = salad_defs.get_pairs_cosine_threshold_version_2(matrix = matrix,
                                                                                 network_community = network_community,
                                                                                 network_pairs = True,
                                                                                 compressed = False)

print len(y_vector)
print len(recipe_pairs[0])
split = 4*int(float(len(recipe_pairs))/5.0)
test_split = int(float(len(recipe_pairs))/5.0)
print split


X_train, X_test, y_train, y_test = train_test_split(recipe_pairs, y_vector, train_size=0.6,random_state=0)



def make_one_learner(subset_size, split, t, X, y): #subset_size is number of pairs, t is for only testing purposes
    
    #root = int(math.sqrt(subset_size))
    
    # build vectors
   # arr = np.arange(split)
   # np.random.shuffle(arr)
   # q = 0 #random number
    #X=[]
    #y=[]
    #for q in arr: #build random set
       # q = randint(0, split) #For reference for Erol: This is where 'split' is used
    #    X.append(recipe_pairs[q])
     #   y.append(y_vector[q])

    
    #X , y = salad_defs.build_feature_vectors(subset, isCompress , root , 0 , len(subset), degree_centrality, bc_list)

    if isTree:
        #for trees
        clf = tree.DecisionTreeClassifier().fit(X,y), #to be used for bagging
    else:
        #For gradietn boosting
        #clf = GradientBoostingClassifier(n_estimators=100, max_depth=1, random_state=0).fit(X, y) # for boosting
        clf = GradientBoostingClassifier(n_estimators= 600, max_depth= 3,subsample= 0.5, random_state= 0).fit(X, y)
    # for seeing feature importance
    fi = clf[0].feature_importances_
    print fi
    l = len(fi)
    for feature, loc in sorted( zip(fi, range(0,l)), reverse = True)[:20]:#Know most important features
        print "feature: %d, importance: %f"%(loc, feature)

    skew = float(sum(y))/len(y)
    print "For tree %d the skew is: %f " %(t, skew)
   
    return clf

in_subset_size = 300*299  #trained on; actual only sqrt unique recipes
#num_learners = 1 #set to x to test bagging method for x trees, 
ensemble = []
t = 1
 #Comment by Erol: For loop is used for bagging trees
for n in range(0,num_learners):
    print t
    learner = make_one_learner(in_subset_size, split, t, X_train, y_train)
    #print learner
    ensemble.append(learner)
    t += 1 
   
# Testing section
#test_range= len(features) - split # Size of test recipes

#Xtest, ytest = salad_defs.build_feature_vectors(features , isCompress, test_range , split , len(features), degree_centrality, bc_list)
half = len(X_test)/2
Xtest1 =X_test[:half]
ytest1=y_test[:half]

print "From over 0.2"
salad_defs.show_things(ensemble, Xtest1 , ytest1, isTree, isLoaded)

print "Once again, over 0.2"
Xtest2 = X_test[half:]
ytest2=y_test[half:]

salad_defs.show_things(ensemble, Xtest2 , ytest2, isTree, isLoaded)


print "From under 0.2"
both_bad, both_allrep, bad_and_allrep = salad_defs.analysis_pairs(ensemble, X_under , y_under)

print "For pairs both with bad recipes, amount: %d , accuracy: %f"%both_bad
print "For pairs both with allrecipes, amount: %d , accuracy: %f"%both_allrep
print "For pairs bad and allrecipes, amount: %d , accuracy: %f"%bad_and_allrep

#s = learner[0].score(Xtest,ytest) 
#print 'score of learner is: ' + str(s)
#percent = salad_defs.predict_bagged_score(ensemble, Xtest , ytest ,isTree)
#print "Accuracy of learner is : %f" %percent

    
#pickle it!
name = 'gtbs_600_iter_depth_3_flavor_and_compliment_network_community_v2.pi'
file_pi = open(name, 'w') 
pickle.dump(ensemble, file_pi) #that was such a stupid mistake!!!!!
