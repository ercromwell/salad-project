# salad_chef.py
# Main script that runs genetic algorithm to create new salad recipe
# By: Erol Cromwell, 2014, DRI project
 # for commitng purpsoes
#0: Import , load any modules/files we need, such as the predictor, graphs and whatnot
import pickle
import random
import copy
import networkx as nx
from sklearn.ensemble import GradientBoostingClassifier
import centrality_measures as cm
import genetic_algorithm_defs as gad
import ingredient_networks as inet
import salad_defs
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt

    # known recipes
load = open('feature_vector_matrix_over_5_reviews_cleaned_v11.pi')
known_matrix = pickle.load(load)
load.close()

    #compliment graph
file_name = 'compliment_graph_weighted_v11.pi'
load = open(file_name)
compliment_graph = pickle.load(load)
load.close()
    # known network communities
filename = 'compliment_network_community_v11_rank_60.pi'
load = open(filename)
network_community = pickle.load(load)

    #gradient boosting learner
file_name = 'gtbs_v11_600_iterations_depth_3_rank_60_network_community.pi'
load = open(file_name)
load_ensemble = pickle.load(load)
load.close()
gtbs = load_ensemble[0][0]

NUM_RECIPES = 100 #Number of initial random recipes to generate

NUM_GENERATIONS = 40 #Number of generations to produce

NUM_REPRODUCE = 250 #Number of times children are produced, (number of children = 2*num_reproduce)

RANK_K = 60 #Whatever rank used in learner

list_of_ingredients = sorted(compliment_graph.nodes())
NUM_INGRED = len(list_of_ingredients) #Official, for now
START_INGRED = 0
END_INGRED = NUM_INGRED

    # Add centrality info, network community info to recipes
cmv = cm.centrality_measure_vec(compliment_graph) #To be kept outside loop

feature_known_recipes = []
known_ratings = []
for i in range(0,len(known_matrix)):
    if sum(known_matrix[i][3:]) > 0:
        cv = cm.centrality_vector( known_matrix[i][3:], cmv)
        feature_known_recipes.append(network_community[i] + cv)
        known_ratings.append(known_matrix[i][0])

print len(known_ratings), len(feature_known_recipes)

#1: Generate random recipes
    #initial recipes set up like ingredient vectors
recipes = gad.generate_random_recipes(NUM_RECIPES, NUM_INGRED, random_walk = True,compliment_graph = compliment_graph)
    

    #1a: Create feature initial recipes
feature_recipes = gad.build_feature_recipes(recipes, compliment_graph, RANK_K,
                                         START_INGRED, END_INGRED, cmv, network = True)


#2: Measurements for initial population, comparing to known recipes (those from alrecipes.com)
recipe_rankings, s = gad.compare_recipe_generation( feature_known_recipes, feature_recipes,
                                                         known_ratings, NUM_INGRED, gtbs,
                                                         network_pairs = True, compressed = False)
x = [0]
scores = [ s[0] ]
score_max = [ s[1] ]
#current_gen_max.append(max(recipe_rankings)[0])
diverse = [ gad.diversity_measure(recipes) ]
median_score = [ s[2] ]

max_median = [ max( [med for (score, mean, med, q) in recipe_rankings] ) ] #Max median ratings beat
max_mean = [ max( [ mean for (score, mean, med, q) in recipe_rankings] ) ] #Max mean ratings beat

if NUM_GENERATIONS == 0:
    x.append(1)
    scores.append(s[0])
    score_max.append( s[1] )    #current_gen_max.append(max(recipe_rankings)[0])
    diverse.append( diverse[0])
    median_score.append(s[2])

    max_median.append(max_median[0] )
    max_mean.append( max_mean[0] )


#testing
print sum(  [ score for (score, mean, med, q) in recipe_rankings ] )
#Loop for generations
for i in range(0, NUM_GENERATIONS):
    print i

    #3: Create parent probabily interval.
    recipe_score = [ score for (score, mean, med, q) in recipe_rankings ] 
    
    parent_probability = gad.create_parent_probabilty_interval(recipe_score)

    #4: Create children recipes using crossovers of parent recipes
    children_recipes = []
    
    for j in range(0, NUM_REPRODUCE):
        
        prob_1 = random.random()
        parent_1 = gad.find_interval(prob_1, parent_probability)
        
        prob_2 = random.random()
        parent_2 = gad.find_interval(prob_2, parent_probability)
        
        #Make sure parent_2 is not parent_1
        while parent_2 == parent_1:
            prob_2 = random.random()
            parent_2 = gad.find_interval(prob_2, parent_probability)

        child_1, child_2 = gad.create_children(recipes[parent_1], recipes[parent_2], NUM_INGRED)

        #5: Slight mutation to children recipes
        #gad.mutations(child_1)
        #gad.mutations(child_2)
        children_recipes.append(child_1)
        children_recipes.append(child_2)
        
    gad.mutations(children_recipes)
    
        #This method only takes top 100 children to use as next generation
    #6: Compare children to known recipes
    k = 6
    feature_children_recipes = gad.build_feature_recipes(children_recipes, compliment_graph,
                                                    RANK_K, START_INGRED, END_INGRED, cmv, network = True)
    child_recipe_rankings, s =  gad.compare_recipe_generation( feature_known_recipes, feature_children_recipes,
                                                         known_ratings, NUM_INGRED, gtbs,
                                                         network_pairs = True, compressed = False)

    # From previous generation have: recipes, feature_recipes, recipe_rankings
    combined_recipes = recipes + children_recipes
    combined_feature_recipes = feature_recipes + feature_children_recipes
    combined_recipe_rankings = gad.combine_rankings(recipe_rankings, child_recipe_rankings)
    
    #7: Diversity check on children and parent recipes, eliminating recipes that do not satisfy requirement
    sorted_rankings = sorted(combined_recipe_rankings, reverse = True) 
    recipe_rankings = gad.diversity_filter(sorted_rankings, combined_recipes, k, i, NUM_GENERATIONS, NUM_RECIPES)

    #Select next generation of recipes

    recipes = [ combined_recipes[q] for (score, mean, med, q) in recipe_rankings]
    feature_recipes = [ combined_feature_recipes[q] for (score, mean, med, q) in recipe_rankings ]

         #Add measurements
    x.append(i+1)
    scores.append(s[0])
    score_max.append(s[1])
    #current_gen_max.append(recipe_rankings[0][0])
    diverse.append(gad.diversity_measure(recipes))
    median_score.append(s[2])

    max_median.append( max( [med for (score, mean, med, q) in recipe_rankings] ) )
    max_mean.append( max( [mean for (score, mean, med, q) in recipe_rankings] ) )



#10: Display final recipes, results of improvement

top_recipes = recipes[:5]
top_scores = [ score for (score, mean, med, q) in recipe_rankings][:5]
top_list = zip(top_scores, top_recipes)
i=0
for score, recipe in top_list:
    print 'For recipe # %d, score is: %f'% (i, score)
    gad.print_ingredients(recipe,list_of_ingredients)
    i+=1

plt.figure(1)
plt.plot(x,scores, label = 'Mean % comps won')
plt.plot(x, score_max, label = 'Max % comps won')
#plt.plot(x, current_gen_max, label = 'Max for current gen')
plt.plot(x, median_score, label = 'Median % comps')
plt.legend(loc='upper left')
#plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

plt.xlabel('generation')
plt.ylabel('percent')
plt.axis([0 ,NUM_GENERATIONS, 0, 1.5])

plt.figure(2)
plt.subplot(1,2,1)
plt.plot(x, max_median, label = 'max median')
plt.plot(x, max_mean, label = 'max mean')
plt.legend(loc='lower right')
plt.axis([0 ,NUM_GENERATIONS, 3.5, 5])
plt.xlabel('generation')
plt.ylabel('percent')

plt.subplot(1,2,2)
plt.plot(x, diverse, label = 'Diversity')
plt.legend(loc='upper left')


plt.show()

