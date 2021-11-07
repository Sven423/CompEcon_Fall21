# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 21:14:00 2021

@author: siwenz
"""
# imports
from sklearn import tree
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import KFold
from sklearn.model_selection import train_test_split
from sklearn.model_selection import RandomizedSearchCV

from sklearn.tree import export_text
from sklearn.ensemble import BaggingRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

cd "C:\Users\f1060\OneDrive - University of South Carolina\2021 Fall\Computational module\Classes"
# read in the data
data_file_path = os.path.join('Assignment6', 'biden.csv')
ps6data = pd.read_csv(data_file_path)


# create y and X to reference later
y = ps6data['biden'].values
X_var_names = ['female', 'age', 'educ', 'dem', 'rep']
X = ps6data[X_var_names].values


# question 1
# split sample into two parts
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=25)

# Fit a decision tree on the full data
regtree = tree.DecisionTreeRegressor(max_depth=3, min_samples_leaf=5)
biden_tree = regtree.fit(X_train, y_train)
# print out text representation of the tree
r = export_text(biden_tree, feature_names=X_var_names)
print(r)

# plot the tree
fig, axes = plt.subplots(nrows = 1,ncols = 1,figsize = (4,4), dpi=300)
tree.plot_tree(biden_tree,
           feature_names = X_var_names, 
           filled = True);

# calculate the test-data tree MSE
MSE = mean_squared_error(y, biden_tree.predict(X))
print('The SSE of a tree of depth ', biden_tree.get_depth(), ' and ',
      biden_tree.get_n_leaves(), ' leaves = ', MSE)


# question 2

# paramaters
from scipy.stats import randint as sp_randint
param_dist = { "max_depth":[3, 10],
            "min_samples_split":sp_randint(2, 20),
            "min_samples_leaf":sp_randint(2, 20)}

# start tuning
clf = RandomizedSearchCV(biden_tree, param_dist, n_iter=100, n_jobs=-1, cv=5, 
                         random_state=25, scoring="neg_mean_squared_error")
tunedTree = clf.fit(X_train, y_train)
# return the optimal parameters and MSE
tunedTree.best_params_
tunedTree.best_score_


# question 3

# now try a Random Forest model and set some parameters
biden_treeRF = RandomForestRegressor(
                max_depth=3,  # set max depth of tree
                n_estimators=100,
                max_features=3, # the number of features to consider when looking for the best split
                bootstrap=True,
                n_jobs=-1,
                oob_score=True,
                min_samples_split=10,
                min_samples_leaf=5,
                random_state=25)
biden_treeRF.fit(X_train, y_train)

# set the parameters
param_dist_rf={"n_estimators":[10, 200],
            "max_depth":[3, 10],
            "min_samples_split":sp_randint(2, 20),
            "min_samples_leaf":sp_randint(2, 20),
            "max_features":sp_randint(1, 5)}

# start tuning
clf = RandomizedSearchCV(biden_treeRF, param_dist_rf, n_iter=100, n_jobs=-1, cv=5, 
                         random_state=25, scoring="neg_mean_squared_error")
tunedTreeRF = clf.fit(X_train, y_train)
# return the optimal parameters and MSE
tunedTreeRF.best_params_
tunedTreeRF.best_score_
