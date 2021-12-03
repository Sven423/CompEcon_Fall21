# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
"""
@author: SiwenZ
"""

# ProblemSet 8 - investment decision question

# import packages
# Import packages
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
from scipy.optimize import fminbound
import scipy.optimize as opt

import functions as fn


# 1. set parameters and create grid space

beta = 0.95
sigma = 1.0
r = 1.1 # it is a total return for a portfolio, I 

'''
------------------------------------------------------------------------
Create Grid for State Space    
------------------------------------------------------------------------
lb_s      = scalar, lower bound of the grid
ub_s      = scalar, upper bound of the grid 
size_s    = integer, number of grid points in state space
s_grid    = vector, size_s x 1 vector of grid points 
------------------------------------------------------------------------
'''
lb_s = 0.4 
ub_s = 2.0 
size_s = 500  # Number of grid points
s_grid = np.linspace(lb_s, ub_s, size_s)


# 2. value fn iteration and extract the optimal solution

'''
------------------------------------------------------------------------
Value Function Iteration    
------------------------------------------------------------------------
VFtol     = scalar, tolerance required for value function to converge
VFdist    = scalar, distance between last two value functions
VFmaxiter = integer, maximum number of iterations for value function
V         = vector, the value functions at each iteration
Vmat      = matrix, the value for each possible combination of c and c'
Vstore    = matrix, stores V at each iteration 
VFiter    = integer, current iteration number
V_params  = tuple, contains parameters to pass into Bellman operator: beta, sigma
TV        = vector, the value function after applying the Bellman operator
PF        = vector, indicies of choices of c' for all c 
VF        = vector, the "true" value function
------------------------------------------------------------------------
'''

VFtol = 1e-5
VFdist = 7.0 
VFmaxiter = 5000 
V = np.zeros(size_s)#true_VF # initial guess at value function
Vstore = np.zeros((size_s, VFmaxiter)) #initialize Vstore array

VFiter = 1 
V_params = (beta, sigma)


while VFdist > VFtol and VFiter < VFmaxiter:
    Vstore[:, VFiter] = V
    TV, optI = fn.bellman_operator(V, s_grid, V_params)
    VFdist = (np.absolute(V - TV)).max()  # check distance
    print('Iteration ', VFiter, ', distance = ', VFdist)
    V = TV
    VFiter += 1

if VFiter < VFmaxiter:
    print('Value function converged after this many iterations:', VFiter)
else:
    print('Value function did not converge')            


VF = V # solution to the functional equation

# 3. do some visualizations
# Plot value function 
plt.figure()
plt.plot(s_grid[1:], VF[1:])
plt.xlabel('Initial saving')
plt.ylabel('Value Function')
plt.title('Value Function - stochastic investment decision')
plt.show()

#Plot optimal investment rule as a function of initial saving amount
plt.figure()
fig, ax = plt.subplots()
ax.plot(s_grid[1:], optI[1:], label='Investment')
# Now add the legend with some customizations.
legend = ax.legend(loc='upper left', shadow=False)
# Set the fontsize
for label in legend.get_texts():
    label.set_fontsize('large')
for label in legend.get_lines():
    label.set_linewidth(1.5)  # the legend line width
plt.xlabel('Initial saving')
plt.ylabel('Optimal Investment')
plt.title('Policy Function, investment - stochastic investment decision')
plt.show()