import pickle

file_name = 'feature_vector_matrix_cleaned.pi'
open_file = open(file_name)
matrix = pickle.load(open_file)
print len(matrix)
length = len(matrix)

edited_matrix = []

for vector in matrix:
    if vector[1] >= 5:
       # print vector[1]
        edited_matrix.append(vector)

print len(edited_matrix)

out_file_name = 'feature_vector_matrix_over_5_reviews_cleaned.pi'
file_pi = open(out_file_name, 'w')
pickle.dump(edited_matrix, file_pi)
