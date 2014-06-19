import pickle
import numpy as np
import salad_defs
filename = 'feature_vector_matrix_over_5_reviews_cleaned.pi'
preload = open(filename)
matrix = pickle.load(preload)

print len(matrix[0])-3


cos_sim_pairs = []
y_vector = []
for i in range(0,len(matrix)):
    v1 = matrix[i][3:] #These are the ingredient matrices
    norm1 = np.linalg.norm(v1)

    if norm1 == 0:
        print "recipe number %d has no ingredients"%(i+1)
    else:       
        for j in range(i+1, len(matrix)):

            v2 = matrix[j][3:]
            norm2 = np.linalg.norm(v2)
            if norm2 !=0:
                dot = np.dot(v1,v2)
                cosine_measure = float(dot)/(norm1*norm2)

                if cosine_measure > 0.2:
                    compressed_pair = salad_defs.compress(v1, v2)
                    cos_sim_pairs.append(compressed_pair)

                    if matrix[i][0] > matrix[j][0]:
                        y_vector.append(1)
                    else:
                        y_vector.append(0)
                                
                    
print len(cos_sim_pairs)
print len(y_vector)
    
new_file = 'recipe_pairs_over_cosine_similarity_threshold.pi'
out_file = open(new_file, 'w')
pickle.dump(cos_sim_pairs, out_file)

other_file = 'y_result_vector_for_recipe_pairs.pi'
out = open(other_file,'w')
pickle.dump(y_vector, out)



out_file.close()
out.close()



#print "Number of  measures: %d" %len(cos_sim)
#bins = [ 0, 0.2, 0.4, 0.6, 0.8, 1]
#hist, bin_edges = np.histogram(cos_sim, bins)

#print hist
#print bin_edges

#print "Number of preptimes in histogram: %d" %hist.sum()

#new_file='histogram_data_rating_100_bins_over_5_ratings.txt'
#out_file=open(new_file, 'w')
#out_file.write(str(hist) + "\n" + str(bin_edges))
#out_file.close
#print "Histogram output to file: ", new_file


