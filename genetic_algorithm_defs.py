import random
import networkx
from collections import defaultdict

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

        #Find where walk lies in probability intervals
        next_ingred = -1 # represent ingredient location in interval
        location = 0 # current interval location
        while next_ingred < 0:
            #Check measure
            if location == len(neighbors):
                print 'You did not find the interval'
                return []

            if interval[location] <= walk and walk < interval[location+1]:
                next_ingred = location
            else:
                location += 1

        current_ingred = neighbors[next_ingred]
        add_ingred = list_of_nodes.index(current_ingred)
                
        if add_ingred not in set_nodes:
            ingredients.append(add_ingred)
            set_nodes.add(add_ingred)
            
        
      
    return ingredients

# Ranks parent recipes, create probability intervals to choose parents
def create_parent_probabilty_interval(recipe_pairs, gtbs):

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

    print recipe_score # temporary, for looking at
    
    total = sum(recipe_score.values())
    parent_prob = [0.0]
    for recipe, score in sorted(recipe_score.items()):
        parent_prob.append( float(score)/total  + parent_prob[recipe] )

    return parent_prob
        
def print_ingredients(recipe_vec, list_of_ingredients):
    list = []

    for i in range(0,len(recipe_vec)):
        if recipe_vec[i] == 1:
            list.append(list_of_ingredients[i])

    print list
