import salad_defs
import numpy as np
import pickle

filename = 'gtbs_recipe_pairs_over_cos_threshold.pi'
load = open(filename)
ensemble = pickle.load(load)
load.close()
print filename, ' loaded'

filename = 'feature_vector_matrix_over_5_reviews_cleaned.pi'
preload = open(filename)
matrix = pickle.load(preload)
preload.close()
print filename, ' loaded'

Xtest, ytest = salad_defs.get_pairs_under_cosine_threshold(matrix)
print 'have pairs'
isTree = False
isLoaded = True
salad_defs.show_things(ensemble, Xtest, ytest, isTree, isLoaded)


