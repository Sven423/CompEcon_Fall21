# -*- coding: utf-8 -*-
"""
Created on Fri Oct  8 13:30:00 2021

@author: Siwen Z
"""

# not sure why it has a warning but it works well
cd "C:\Users\f1060\OneDrive - University of South Carolina\2021 Fall\Computational module\Classes\Assignment5"

# import packages
import numpy as np
import pandas as pd
from geopy.distance import geodesic
from itertools import product
import scipy.optimize as opt
from scipy.optimize import differential_evolution


# read in data and work on some data cleaning
ps5data = pd.read_csv("radio_merger_data.csv")

# scale the population and dollars using ln()
ps5data["ln_population_target"] = np.log(ps5data["population_target"])
ps5data["ln_price"] = np.log(ps5data["price"])


# generate two dfs for buyers and targets
data_2007 = ps5data[ps5data["year"]==2007]
data_2008 = ps5data[ps5data["year"]==2008]

# get different dataframes for buyers and targets for each year
buyer_2007 = data_2007[[
    "year",
    "buyer_id",
    "buyer_lat",
    "buyer_long",
    "price",
    "num_stations_buyer",
    "corp_owner_buyer",
    "ln_price"
]]

target_2007 = data_2007[[
    "target_id",
    "target_lat",
    "target_long",
    "hhi_target",
    "population_target",
    "ln_population_target"
]]

buyer_2008 = data_2008[[
    "year",
    "buyer_id",
    "buyer_lat",
    "buyer_long",
    "price",
    "num_stations_buyer",
    "corp_owner_buyer",
    "ln_price"
]]

target_2008 = data_2008[[
    "target_id",
    "target_lat",
    "target_long",
    "hhi_target",
    "population_target",
    "ln_population_target"
]]



def objective_fn_1(parms):
    '''
    Parameters
    ----------
    parms: an array of alpha, beta (number)
    The parameters in the payoff function

    Returns
    -------
    -total_score: the opposite of the maximum score estimator because we will later minimize it

    '''
    
    alpha = parms[0]
    beta = parms[1]
    
    # because2007 and 2008 have the same index, we need to separately loop them in
    
    # count the number of iterations to make sure we are doing it correctly
    count = 0
    # this is the sum of all scores
    total_score = 0

    # to simplify the code later, lets get a payoff fn
    def payoff_fn_2007_1(b,t):
        # calcualte the distance first - no need to create a separate column for it
        distance = geodesic((buyer_2007["buyer_lat"][b], buyer_2007["buyer_long"][b]), (target_2007["target_lat"][t], target_2007["target_long"][t])).miles            
        # the whole payoff value
        payoff = (buyer_2007.at[b, "num_stations_buyer"] * target_2007.at[t, "ln_population_target"] 
                  + alpha * buyer_2007.at[b, "corp_owner_buyer"] * target_2007.at[t, "ln_population_target"]
                  + beta * distance)
        return payoff
    
    def payoff_fn_2008_1(b,t):
        # calcualte the distance first - no need to create a separate column for it
        distance = geodesic((buyer_2008["buyer_lat"][b], buyer_2008["buyer_long"][b]), (target_2008["target_lat"][t], target_2008["target_long"][t])).miles            
        # the whole payoff value
        payoff = (buyer_2008.at[b, "num_stations_buyer"] * target_2008.at[t, "ln_population_target"] 
                 + alpha * buyer_2008.at[b, "corp_owner_buyer"] * target_2008.at[t, "ln_population_target"]
                 + beta * distance)
        return payoff   


    # 2007
    
    for i in range(len(buyer_2007["buyer_id"])):
        for j in range(i + 1, len(buyer_2007["buyer_id"])):
            count += 1
            # if f(b,t) + f(b',t') > f(b',t) + f(b,t'), then add one
            if payoff_fn_2007_1(i, i) + payoff_fn_2007_1(j, j) > payoff_fn_2007_1(i, j) + payoff_fn_2007_1(j, i):
                total_score += 1
                
    # print(count)
    
    
    # 2008 - be careful of the index!!

    for i in range(45, len(buyer_2008["buyer_id"])):
        for j in range(i + 1, len(buyer_2008["buyer_id"])):
            # count += 1
            # if f(b,t) + f(b',t') > f(b',t) + f(b,t'), then add one
            if payoff_fn_2008_1(i, i) + payoff_fn_2008_1(j, j) > payoff_fn_2008_1(i, j) + payoff_fn_2008_1(j, i):
                total_score_ += 1
                
    return -total_score


# very similar idea - but we include the HHI info this time
def objective_fn_2(parms):
    '''
    Parameters
    ----------
    parms : an array of delta, alpha, beta, gamma (number)
    The parameters in the payoff function

    Returns
    -------
    -total_score: the opposite of the maximum score estimator because we will later minimize it

    '''
    
    # this way works too
    delta, alpha, beta, gamma = parms
    
    # because2007 and 2008 have the same index, we need to separately loop them in
    
    # count the number of iterations to make sure we are doing it correctly
    count = 0
    # this is the sum of all scores
    total_score = 0


    # to simplify the code later, lets get a payoff fn
    def payoff_fn_2007_2(b,t):
        # calcualte the distance first - no need to create a separate column for it
        distance = geodesic((buyer_2007["buyer_lat"][b], buyer_2007["buyer_long"][b]), (target_2007["target_lat"][t], target_2007["target_long"][t])).miles            
        # the whole payoff value
        payoff = delta * buyer_2007.at[b, "num_stations_buyer"] * target_2007.at[t, "ln_population_target"] 
        + alpha * buyer_2007.at[b, "corp_owner_buyer"] * target_2007.at[t, "ln_population_target"]
        + beta * distance
        + gamma * target_2007.at[t, "hhi_target"]
        return payoff
        
    def payoff_fn_2008_2(b,t):
        # calcualte the distance first - no need to create a separate column for it
        distance = geodesic((buyer_2008["buyer_lat"][b], buyer_2008["buyer_long"][b]), (target_2008["target_lat"][t], target_2008["target_long"][t])).miles            
        # the whole payoff value
        payoff = delta * buyer_2008.at[b, "num_stations_buyer"] * target_2008.at[t, "ln_population_target"] 
        + alpha * buyer_2008.at[b, "corp_owner_buyer"] * target_2008.at[t, "ln_population_target"]
        + beta * distance
        + gamma * target_2008.at[t, "hhi_target"]
        return payoff


    # 2007
    
    for i in range(len(buyer_2007["buyer_id"])):
        for j in range(i + 1, len(buyer_2007["buyer_id"])):
            count += 1
            # if f(b,t) + f(b',t') > f(b',t) + f(b,t'), then add one
            if payoff_fn_2007_2(i, i) + payoff_fn_2007_2(j, j) > payoff_fn_2007_2(i, j) + payoff_fn_2007_2(j, i):
                total_score += 1
          
    # 2008

    for i in range(45, len(buyer_2008["buyer_id"])):
        for j in range(i + 1, len(buyer_2008["buyer_id"])):
            # count += 1
            # if f(b,t) + f(b',t') > f(b',t) + f(b,t'), then add one
            if payoff_fn_2008_2(i, i) + payoff_fn_2008_2(j, j) > payoff_fn_2008_2(i, j) + payoff_fn_2008_2(j, i):
                total_score += 1

    return -total_score



# Try to use Nelder-Mead method to get the optimum - it takes ages though

# initial guess of alpha and beta
guess_1 = (1,1)
guess = (0.5, 1, 1, -0.5)
bnds = [(-1000,1000),(-1000,1000)]

result = opt.minimize(objective_fn_1, x0 = guess_1, method='Nelder-Mead', tol=1e-15)
result = opt.minimize(objective_fn_2, x0 = guess, method='Nelder-Mead', tol=1e-15)
print(result)

# Try to use differential evolution method but failed - how to use it? Please show us
result = opt.differential_evolution(objective_fn_2, bnds, x0 = guess)
