print(__doc__)

# Author: Peter Prettenhofer <peter.prettenhofer@gmail.com>
# Edited by Erol Cromwell for purpose of research
# License: BSD 3 clause
import pickle # added by Erol
import numpy as np
from matplotlib import pyplot as plt

from sklearn import ensemble
from sklearn.cross_validation import KFold
from sklearn.cross_validation import train_test_split


# Generate data (From recipe_pairs w/ cosine sim over 0.2)
load = open('recipe_pairs_over_cosine_similarity_threshold.pi')
recipe_pairs = pickle.load(load)
load.close()

print len(recipe_pairs)
y_load = open('y_result_vector_for_recipe_pairs.pi')
y_vector = pickle.load(y_load)
y_load.close()

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
params = {'n_estimators': 600, 'max_depth': 3,'subsample': 0.5,'random_state': 0}
clf = ensemble.GradientBoostingClassifier(**params)

clf.fit(X_train, y_train)
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


def cv_estimate(n_folds=3):
    cv = KFold(n=X_train.shape[0], n_folds=n_folds)
    cv_clf = ensemble.GradientBoostingClassifier(**params)
    val_scores = np.zeros((n_estimators,), dtype=np.float64)
    for train, test in cv:
        cv_clf.fit(X_train[train], y_train[train])
        val_scores += heldout_score(cv_clf, X_train[test], y_train[test])
    val_scores /= n_folds
    return val_scores


# Estimate best n_estimator using cross-validation
cv_score = cv_estimate(3)

# Compute best n_estimator for test data
test_score = heldout_score(clf, X_test, y_test)

# negative cumulative sum of oob improvements
cumsum = -np.cumsum(clf.oob_improvement_)

# min loss according to OOB
oob_best_iter = x[np.argmin(cumsum)]

# min loss according to test (normalize such that first loss is 0)
test_score -= test_score[0]
test_best_iter = x[np.argmin(test_score)]

# min loss according to cv (normalize such that first loss is 0)
cv_score -= cv_score[0]
cv_best_iter = x[np.argmin(cv_score)]

#Printing best iteration:
print 'Best iteration according to oob is: ' + str(oob_best_iter)
print 'Best iteration according to test data is: ' + str(test_best_iter)
print 'Best iteration accordign to cv is: ' + str(cv_best_iter)

# color brew for the three curves
oob_color = map(lambda x: x / 256.0, (190, 174, 212))
test_color = map(lambda x: x / 256.0, (127, 201, 127))
cv_color = map(lambda x: x / 256.0, (253, 192, 134))

# plot curves and vertical lines for best iterations
plt.plot(x, cumsum, label='OOB loss', color=oob_color)
plt.plot(x, test_score, label='Test loss', color=test_color)
plt.plot(x, cv_score, label='CV loss', color=cv_color)
plt.axvline(x=oob_best_iter, color=oob_color)
plt.axvline(x=test_best_iter, color=test_color)
plt.axvline(x=cv_best_iter, color=cv_color)

# add three vertical lines to xticks
xticks = plt.xticks()
xticks_pos = np.array(xticks[0].tolist() +
                      [oob_best_iter, cv_best_iter,test_best_iter])
xticks_label = np.array(map(lambda t: int(t), xticks[0]) +
                        ['OOB','CV', 'Test'])
ind = np.argsort(xticks_pos)
xticks_pos = xticks_pos[ind]
xticks_label = xticks_label[ind]
plt.xticks(xticks_pos, xticks_label)

plt.legend(loc='upper right')
plt.ylabel('normalized loss')
plt.xlabel('number of iterations')

plt.show()
