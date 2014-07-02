

    k= 4

    #6: Compare children to known recipes
    feature_children_recipes = gad.build_feature_recipes(children_recipes, compliment_graph,
                                                    rank_k, start_ingred, end_ingred, cmv)
    child_recipe_rankings, s =  gad.compare_recipe_generation( feature_known_recipes, feature_children_recipes,
                                                         known_ratings, num_ingred, gtbs)

    # From previous generation have: recipes, feature_recipes, recipe_rankings
    combined_recipes = recipes + children_recipes
    combined_feature_recipes = feature_recipes + feature_children_recipes
    combined_recipe_rankings = gad.combine_rankings(recipe_rankings, child_recipe_rankings)
    
    #7: Diversity check on children recipes, eliminating recipes that do not satisfy requirement
    sorted_rankings = sorted(combined_recipe_rankings, reverse = True) 


    recipe_rankings = gad.diversity_filter(sorted_rankings, combined_recipes, k, i, num_generations)[:num_recipes]
    #Select next generation of recipes

    recipes = [ combined_recipes[q] for (score, mean, med, q) in recipe_rankings]
    feature_recipes = [ combined_feature_recipes[q] for (score, mean, med, q) in recipe_rankings ]

def combine_rankings(recipe_rankings, child_recipe_rankings):
    num_parents = len(recipe_rankings)
    num_children = len(child_recipe_rankings)

    q = 0
    for ranking in recipe_rankings:
        ranking[3] = q
        q+=1

    for child_ranking in child_recipe_rankings:
        child_ranking[3] = q
        q+=1

    if q == num_parents + num_children - 1:
        print "Succesfull COMBINATION!!!!!!!!!!!!!!!!!!!!!!!"

    return recipe_rankings  + child_recipe_rankings
