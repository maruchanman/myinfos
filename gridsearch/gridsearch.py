# coding: utf-8

import numpy as np
from scipy import stats
from xgboost import XGBClassifier
from sklearn.grid_search import GridSearchCV, RandomizedSearchCV

def gridSearch():
    param_grid = {
        "max_depth": range(1, 11),
        "subsample": [x * 0.1 for x in range(5, 16)],
        "colsample_bytree": [x * 0.1 for x in range(5, 16)]
    }
    gs = GridSearchCV(XGBClassifier(), param_grid)
    return gs

def randomizedSearch():
    param_dist = {
        "max_depth": stats.randint(1,10),
        "subsample": stats.uniform(0.5, 1),
        "colsample_bytree": stats.uniform(0.5, 1)
    }
    rs = RandomizedSearchCV(XGBClassifier(), param_dist)
    return gs
