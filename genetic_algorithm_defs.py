import random
import networkx
from collections import defaultdict
import ingredient_networks as inet
import centrality_measures as cm
import salad_defs

# Generates random recipes for fitness function to evaluate
# Need to establish what the length of the recipes generated should be, look into average length of recipe
# Use initial length of 8
# DO i just randomly choose ingredients, or choose based on some weight, probability??????
# length_range is touple and or list, first entry is lower bound, second boundary is upper bound
def generate_random_recipes( num_recipes, num_ingred, random_walk = False, compliment_graph=[]):
    recipe_list = []

    #intiial starting length for recipes, mean length of recipes
    recipe_length = 8
    
    for i in range(0, num_recipes):

        # Creating ingredient list using random walk
        if random_walk:
            ingredients = random_graph_walk(compliment_graph, num_ingred, recipe_length)
        #Randomly generating ingredient list
        else:
            ingredients = random.sample(range(0,num_ingred), recipe_length)


        
        ingred_vec = [0]*num_ingred
        for ingred in ingredients:
            ingred_vec[ingred] = 1
    
        recipe_list.append(ingred_vec)

    return recipe_list

#Returns  list of ingredients by doing a random walk on the compliment graph
def random_graph_walk(compliment_graph, num_ingred, recipe_length):
    start = random.randint(0,num_ingred-1)
    
    list_of_nodes = sorted(compliment_graph.nodes())
    current_ingred = list_of_nodes[start] #string

    #Set to make sure we use each ingredient only once
    set_nodes = set()
    set_nodes.add(start)

    #list of ingredients 
    ingredients = [start]
    
    #Generating ingredient list
    while len(ingredients) < 8:

        #Create probabilites for random walk
        neighbors = compliment_graph.neighbors(current_ingred)
        interval = [0.0] #interval will be probability intervals
        for n in neighbors:
            w = compliment_graph[current_ingred][n]['weight']
            interval.append(w)

        total = sum(interval)

        #Create probability intervals
        for i in range(1, len(interval)):
            interval[i] = interval[i]/total + interval[i-1]

        # Random walk
        walk = random.random()

        next_ingred = find_interval(walk, interval)

        current_ingred = neighbors[next_ingred]
        add_ingred = list_of_nodes.index(current_ingred)
                
        if add_ingred not in set_nodes:
            ingredients.append(add_ingred)
            set_nodes.add(add_ingred)
            
        
      
    return ingredients
# Rank recipes against each other, score is number of competitions a recipe wins
def rank_recipes(recipe_pairs, gtbs):
    recipe_score = defaultdict(int)

    #First two entries represent which recipes compose pair, denoted by an integer
    for pair in recipe_pairs:
        first = pair[0]
        second = pair[1]
        
        p = gtbs.predict(pair[2:])

        if p == 1:
            recipe_score[first] += 1
        else:
            recipe_score[second] += 1

    return recipe_score

# Create probability intervals to choose parents, based on scores
def create_parent_probabilty_interval(recipe_score):
    
    total = sum(recipe_score.values())
    parent_prob = [0.0]
    for recipe, score in sorted(recipe_score.items()):
        parent_prob.append( float(score)/total  + parent_prob[recipe] )

    return parent_prob

#Print ingredients in recipe
def print_ingredients(recipe_vec, list_of_ingredients):
    list = []

    for i in range(0,len(recipe_vec)):
        if recipe_vec[i] == 1:
            list.append(list_of_ingredients[i])

    print list

#Find where walk lies in probability intervals, choosing parent
def find_interval(random_num, prob_interval):
    interval = -1 
    location = 0 # current interval location
    while interval < 0:
            #Check measure
            if location == len(prob_interval)-1:
                print 'You did not find the interval'

            if  random_num < prob_interval[location+1]:
                interval = location
            else:
                location += 1

    return interval

# Create children recipes given two recipes, by splitting somewhere randomly
def create_children(recipe_1, recipe_2, num_ingred):
    split = random.randint(1 ,num_ingred-1) #forced crossover

    child_1 = recipe_1[:split] + recipe_2[split:]
    child_2 = recipe_2[:split] + recipe_1[split:]

    return child_1, child_2

def build_feature_recipes(recipes, compliment_graph, rank_k, start_ingred, end_ingred, cmv):

    network_community = inet.create_network_community(compliment_graph, recipes, rank_k = rank_k)

    feature_recipes = []
    for i in range(0,len(recipes)):   
        cv = cm.centrality_vector(recipes[i][start_ingred:end_ingred], cmv)
        feature_recipes.append(recipes[i] + cv + network_community[i])

    return feature_recipes

# returns top n ranked recipes
def top_n_recipes(recipe_score, n):

    pairs = [ (v,k) for (k,v) in recipe_score.iteritems() ]
    
    s = sorted(pairs, reverse = True)

    top = s[:n]

    return top
            
    
# Returns bottom n ranked recipes
def bottom_n_recipes(recipe_score, n):
    pairs = [ (v,k) for (k,v) in recipe_score.iteritems() ]

    s = sorted(pairs)

    bottom = s[:n]

    return bottom

# Random(for now) mutations to children recipes
def mutations(children_recipes):

    mutation_chance = 0.05
    prob_add = 0.3333
    prob_remove = 0.6666
    prob_sub = 1
    
    for child in children_recipes:
        
        mutate = random.random()

        if mutate < mutation_chance: # mutation occurs
            t = random.random()
            if t <= prob_add:
                add_ingredient(child)
            elif t > prob_add and t <= prob_remove:
                remove_ingredient(child)
            else:
                substitute_ingredient(child)            


#random for now, recipe is lsit aka mutable
def add_ingredient(recipe):

    no_ingred = []
    for i in range(0, len(recipe)):
        if recipe[i] == 0:
            no_ingred.append(i)

    new_ingred = random.sample(no_ingred, 1)[0]

    recipe[new_ingred] = 1

#random for now
# recipe is list
def remove_ingredient(recipe):
    ingred = []

    for i in range(0, len(recipe)):
        if recipe[i] == 1:
            ingred.append(i)
    remove_ingred = random.sample(ingred, 1)[0]

    recipe[remove_ingred] = 0

#random for now, recipe is list
def substitute_ingredient(recipe):
    ingred = []
    no_ingred = []
    
    for i in range(0, len(recipe)):
        if recipe[i] == 1:
            ingred.append(i)
        else:
            no_ingred.append(i)

    remove_ingred = random.sample(ingred, 1)[0]
    add_ingred = random.sample(no_ingred, 1)[0]

    recipe[remove_ingred] = 0
    recipe[add_ingred] = 1

# Used to compare current generation of recipes to initial starting population of recipes
def compare_recipe_generation( feature_init_recipes, feature_current_recipes, num_ingred, gtbs):
    score_current = 0
    
    network_pairs = False
    compressed = True
    feature_compressed = False

    init_gen_max = 0    #Score of current generation recipes against initial generation recipes
    init_gen_loc = 0
    i = 0

    #Average/ mean score of current generation
    for current in feature_current_recipes:
        c = 0
        for init in feature_init_recipes:

            pair = salad_defs.make_recipe_pair(current, init, num_ingred,
                                               network_pairs, compressed, feature_compressed)
            score = gtbs.predict(pair)
            score_current+=score
            c += score

        #score_current += c
        if c > init_gen_max:
            init_gen_max = c
            init_gen_loc = i
        i+=1
            
    num_comp = len(feature_init_recipes) * len(feature_current_recipes)

    percent_score = float(score_current)/num_comp


    #Top scoring recipe in current generation (% competitions won), include its score in initial generation
    
    

    #Top % score current gen recipes in initial generaton, plus its % score in current gen
    init_gen_max_p = float(init_gen_max)/ len(feature_init_recipes)
    
    return [percent_score, init_gen_max_p]


def same_recipes(recipes):
    num_same = set()

    for i in range(0, len(recipes)):
        for j in range(i+1, len(recipes)):
            if recipes[i] == recipes[j]:
                num_same.add(i)
                num_same.add(j)
        
    return float(len(num_same))/len(recipes)
    
def best_score(feature_recipes, gtbs):
    pairs = salad_defs.build_recipe_pairs(matrix = feature_recipes)
    r = rank_recipes(pairs, gtbs)
    best = top_n_recipes(r, 1)
    for score, r in best:
        t = score

    return t

#Return next generation of recipes
def build_next_gen_recipes(recipes, feature_recipes, feature_children_recipes, gtbs):

      
    #7: create next generation
    all_feature_recipes = feature_children_recipes + feature_recipes
    all_pairs = salad_defs.build_recipe_pairs(matrix = all_feature_recipes)
    all_score = rank_recipes(all_pairs, gtbs)
    top_recipes = top_n_recipes(all_score, len(recipes))

    tr = []
    fr = []
    for score, recipe in top_recipes:
        tr.append(all_feature_recipes[recipe][:len(recipes[0])])
        fr.append(all_feature_recipes[recipe])
    
    return tr, fr


      

        
    
