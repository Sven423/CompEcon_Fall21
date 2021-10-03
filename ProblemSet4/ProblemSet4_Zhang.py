# -*- coding: utf-8 -*-
"""
Created on Sat Sep 25 16:12:09 2021

@author: Siwen Z
"""

# import some packages
import pandas as pd
import numpy as np

import scipy.stats as stats
import statsmodels.api as sm
import scipy.optimize as optimize


# read in the data
dtafile = 'PS4_data.dta'
ps4_data = pd.read_stata(dtafile)
ps4_data.tail() # see some observations

# select only male lead between 25 - 60 years & wages > 7/perhour
male_head_age_wage = ps4_data[(ps4_data["hsex"] == 1) 
                              & (ps4_data["age"] > 25) 
                              & (ps4_data["age"] < 60)
                              & (ps4_data["hlabinc"] / ps4_data["hannhrs"] > 7)]
male_head_age_wage.head()

# create varibles
male_head_age_wage = pd.get_dummies(male_head_age_wage, columns=["hrace"], drop_first=True)
# I dont have hispanic here

# take the ln of the wage
male_head_age_wage["ln_hlabinc"] = np.log(male_head_age_wage["hlabinc"])


# estimate the MLE for 1971, 1980, 1990 and 2000 seperately - so different subsets
ps4_1971 = male_head_age_wage[male_head_age_wage['year'] == 1971]
ps4_1980 = male_head_age_wage[male_head_age_wage['year'] == 1980]
ps4_1990 = male_head_age_wage[male_head_age_wage['year'] == 1990]
ps4_2000 = male_head_age_wage[male_head_age_wage['year'] == 2000]

# for each subsets, I estimate the MLE followed with a OLS for a check.

############## 1970s

# get some variables for the fn
y = ps4_1971["ln_hlabinc"]
educ = ps4_1971["hyrsed"]
age = ps4_1971["age"]
age_s = ps4_1971["age"] ** 2
black = ps4_1971["hrace_2.0"] 
other_race = ps4_1971["hrace_3.0"] 

# the LL fn we use - assume normal dist.
def log_lik(par_vec):
    # If the standard deviation prameter is negative, return a large value:
    if par_vec[6] < 0:
        return(1e8)
    
    # The likelihood function values:
    loc1 = par_vec[0] + par_vec[1] * educ + par_vec[2] * age + par_vec[3] * age_s + par_vec[4] * black + par_vec[5] * other_race, 
    scale1 = par_vec[6]
    
    log_likelihood = -np.sum(stats.norm.logpdf(ps4_1971["ln_hlabinc"], loc = loc1, scale = scale1))
    #This is similar to calculating the likelihood for Y - XB   
    return(log_likelihood)

# initila guess
x0 = [7, 0.07, 0.1, -0.001, -0.22, -0.02, 1]

# optimizers - different methods may work differently a bit
opt_res = optimize.minimize(log_lik, x0, method='Nelder-Mead')
print(opt_res)


# OLS estimation for a check
X = ps4_1971[["hyrsed", "age", "age_s","hrace_2.0","hrace_3.0"]]
X = sm.add_constant(X) # add a constant in!
reg1 = sm.OLS(y,X, missing='drop')
results = reg1.fit().summary()
print(results)


# things are similar for other years - we may be able to write a loop

############## 1980

# get some variables for the fn
y = ps4_1980["ln_hlabinc"]
educ = ps4_1980["hyrsed"]
age = ps4_1980["age"]
age_s = ps4_1980["age"] ** 2
black = ps4_1980["hrace_2.0"] 
other_race = ps4_1980["hrace_3.0"] 

# the LL fn we use - assume normal dist.
def log_lik(par_vec):
    # If the standard deviation prameter is negative, return a large value:
    if par_vec[6] < 0:
        return(1e8)
    
    # The likelihood function values:
    loc1 = par_vec[0] + par_vec[1] * educ + par_vec[2] * age + par_vec[3] * age_s + par_vec[4] * black + par_vec[5] * other_race, 
    scale1 = par_vec[6]
    
    log_likelihood = -np.sum(stats.norm.logpdf(ps4_1980["ln_hlabinc"], loc = loc1, scale = scale1))
    #This is similar to calculating the likelihood for Y - XB   
    return(log_likelihood)

# initila guess
x0 = [7.5, 0.07, 0.1, -0.001, -0.25, 0.012, 1]

# optimizers - different methods may work differently a bit
opt_res = optimize.minimize(log_lik, x0, method='Nelder-Mead')
print(opt_res)


# OLS estimation for a check
X = ps4_1980[["hyrsed", "age", "age_s","hrace_2.0","hrace_3.0"]]
X = sm.add_constant(X) # add a constant in!
reg1 = sm.OLS(y,X, missing='drop')
results = reg1.fit().summary()
print(results)


############## 1990

# get some variables for the fn
y = ps4_1990["ln_hlabinc"]
educ = ps4_1990["hyrsed"]
age = ps4_1990["age"]
age_s = ps4_1990["age"] ** 2
black = ps4_1990["hrace_2.0"] 
other_race = ps4_1990["hrace_3.0"] 

# the LL fn we use - assume normal dist.
def log_lik(par_vec):
    # If the standard deviation prameter is negative, return a large value:
    if par_vec[6] < 0:
        return(1e8)
    
    # The likelihood function values:
    loc1 = par_vec[0] + par_vec[1] * educ + par_vec[2] * age + par_vec[3] * age_s + par_vec[4] * black + par_vec[5] * other_race, 
    scale1 = par_vec[6]
    
    log_likelihood = -np.sum(stats.norm.logpdf(ps4_1990["ln_hlabinc"], loc = loc1, scale = scale1))
    #This is similar to calculating the likelihood for Y - XB   
    return(log_likelihood)

# initila guess
x0 = [7.6, 0.11, 0.07, -0.001, -0.25, 0.001, 1]

# optimizers - different methods may work differently a bit
opt_res = optimize.minimize(log_lik, x0, method='Nelder-Mead')
print(opt_res)


# OLS estimation for a check
X = ps4_1990[["hyrsed", "age", "age_s","hrace_2.0","hrace_3.0"]]
X = sm.add_constant(X) # add a constant in!
reg1 = sm.OLS(y,X, missing='drop')
results = reg1.fit().summary()
print(results)



############## 2000

# get some variables for the fn
y = ps4_2000["ln_hlabinc"]
educ = ps4_2000["hyrsed"]
age = ps4_2000["age"]
age_s = ps4_2000["age"] ** 2
black = ps4_2000["hrace_2.0"] 
other_race = ps4_2000["hrace_3.0"] 

# the LL fn we use - assume normal dist.
def log_lik(par_vec):
    # If the standard deviation prameter is negative, return a large value:
    if par_vec[6] < 0:
        return(1e8)
    
    # The likelihood function values:
    loc1 = par_vec[0] + par_vec[1] * educ + par_vec[2] * age + par_vec[3] * age_s + par_vec[4] * black + par_vec[5] * other_race, 
    scale1 = par_vec[6]
    
    log_likelihood = -np.sum(stats.norm.logpdf(ps4_2000["ln_hlabinc"], loc = loc1, scale = scale1))
    #This is similar to calculating the likelihood for Y - XB   
    return(log_likelihood)

# initila guess
x0 = [6.5, 0.11, 0.11, -0.001, -0.33, -0.08, 1]

# optimizers - different methods may work differently a bit
opt_res = optimize.minimize(log_lik, x0, method='Nelder-Mead')
print(opt_res)


# OLS estimation for a check
X = ps4_2000[["hyrsed", "age", "age_s","hrace_2.0","hrace_3.0"]]
X = sm.add_constant(X) # add a constant in!
reg1 = sm.OLS(y,X, missing='drop')
results = reg1.fit().summary()
print(results)

