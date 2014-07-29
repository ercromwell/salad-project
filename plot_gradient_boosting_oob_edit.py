
# Author: Peter Prettenhofer <peter.prettenhofer@gmail.com>
# Edited by Erol Cromwell for purpose of research
# License: BSD 3 clause
import pickle # added by Erol
import numpy as np
from matplotlib import pyplot as plt
import centrality_measures as cm
from sklearn import ensemble
from sklearn.cross_validation import train_test_split
import salad_defs
load = open('feature_vector_matrix_over_5_reviews_cleaned_v11.pi')
matrix = pickle.load(load)
load.close()

num_ingred = len(matrix[0])-3
print num_ingred
start_ingred = 3
end_ingred = num_ingred + start_ingred

filename = 'compliment_graph_weighted_v11.pi'
load = open(filename)
graph = pickle.load(load)
load.close()

cmv = cm.centrality_measure_vec(graph)

filename = 'compliment_network_community_v11_rank_60.pi'
load = open(filename)
network_community = pickle.load(load)

for i in range(0,len(matrix)):   
    cv = cm.centrality_vector( matrix[i][start_ingred:end_ingred], cmv)
    network_community[i]  += cv



print "Constructing pairs..."
recipe_pairs, y_vector, X_under, y_under = salad_defs.get_pairs_cosine_threshold(matrix = matrix,
                                                                                 network_community = network_community,
                                                                                 num_ingredients = num_ingred,
                                                                                 ingredient_end = end_ingred,
                                                                                 network_pairs = True,
                                                                                 compressed = False)

print len(y_vector)
train_split = 4*int(float(len(recipe_pairs))/5.0)
print train_split

test_split = int(float(len(recipe_pairs))/5.0)
print test_split

X=[]
y=[]
X_final_test=[]
y_final_test=[]
arr = np.arange(len(y_vector))
print len(arr)
np.random.shuffle(arr)
for i in range(0, len(arr)):
    if i < train_split:
        X.append(recipe_pairs[i])
        y.append(y_vector[i])
    else:
        X_final_test.append(recipe_pairs[i])
        y_final_test.append(y_vector[i])


X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.75,random_state=9)
print len(X_train), len(y_train)

# Fit classifier with out-of-bag estimates
params = {'n_estimators': 1500, 'max_depth': 3,'subsample': 0.5,'random_state': 0}
clf = ensemble.GradientBoostingClassifier(**params).fit(X_train, y_train)


acc = clf.score(X_test, y_test)
print("Accuracy: {:.4f}".format(acc))
acc = clf.score(X_final_test, y_final_test)
print "Accuracy of 2nd test set is: %f" %acc

n_estimators = params['n_estimators']
x = np.arange(n_estimators) + 1


def heldout_score(clf, X_test, y_test):
   # """compute deviance scores on ``X_test`` and ``y_test``. """
    score = np.zeros((n_estimators,), dtype=np.float64)
    for i, y_pred in enumerate(clf.staged_decision_function(X_test)):
        score[i] = clf.loss_(y_test, y_pred)
    return score


# Compute best n_estimator for test data
test_score = heldout_score(clf, X_final_test, y_final_test)

# min loss according to test (normalize such that first loss is 0)
test_score -= test_score[0]
test_best_iter = x[np.argmin(test_score)]


#Printing best iteration:
print 'Best iteration according to test data is: ' + str(test_best_iter)

# color brew for the three curves
test_color = map(lambda x: x / 256.0, (127, 201, 127))

# plot curves and vertical lines for best iterations
plt.plot(x, test_score, label='Test loss', color=test_color)
plt.axvline(x=test_best_iter, color=test_color)

# add three vertical lines to xticks
xticks = plt.xticks()
xticks_pos = np.array(xticks[0].tolist() +
                      [ test_best_iter])
xticks_label = np.array(map(lambda t: int(t), xticks[0]) +
                        [ 'Test'])
ind = np.argsort(xticks_pos)
xticks_pos = xticks_pos[ind]
xticks_label = xticks_label[ind]
plt.xticks(xticks_pos, xticks_label)

plt.legend(loc='upper right')
plt.ylabel('normalized loss')
plt.xlabel('number of iterations')

plt.show()

#oob_best_iter, cv_best_iter
