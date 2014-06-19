import pickle
import numpy as np
import matplotlib.pyplot as plt

load = open('feature_vector_matrix_over_5_reviews_cleaned_v5.pi')
matrix = pickle.load(load)
load.close()
lengths = []
rating = []
for i in range(0, len(matrix)):
    lengths.append(sum(matrix[i][3:]))
    rating.append(matrix[i][0])

bins = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]

#hist, bin_edges = np.histogram(lengths, bins)
#print hist
#print bins
#print float(sum(lengths))/len(lengths)

print np.median(lengths)







