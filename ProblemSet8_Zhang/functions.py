
# import packages
# Import packages
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
from scipy.optimize import fminbound
import scipy.optimize as opt


beta = 0.95
sigma = 1.0
r = 1.1 # it is a total return for a portfolio, I 
shock = "bad"


def utility(s, I, t, sigma):
    """
    CRRA, ocnstant relative RA, utility function
    """

    if t == 1:
        c = s - I
    else:
        sprime = r * I
        c = sprime
    if sigma == 1:
        U = np.log(c)
    else:
        U = (c ** (1 - sigma)) / (1 - sigma)
    return U 


def uncertainty(shock):
    '''
    this function return the magnitutude of the shock and probability for two results (a list) from a certain shock happened in the first period
    If the shock is positive, it takes a parameter "good"; if the shock is negative, it takes a parameter "bad"
    '''
    prob_matrix = np.matrix([[1.2, 0.7, 0.3],[0.8, 0.4, 0.6]])
    # this matrix shows that the market is expected to be more bullish
    # the first column shows the magnitude of the shock; the last two columns are prob
    
    if shock == "good":
        return [prob_matrix.item((0,0)), prob_matrix.item((0,1)), prob_matrix.item((0,2))]
    else:
        return [prob_matrix.item((1,0)), prob_matrix.item((1,1)), prob_matrix.item((1,2))]
    
    
# code the Bellman operator function to help with VFI later:
def bellman_operator(V, s_grid, params):
    '''
    The approximate Bellman operator, which computes and returns the
    updated value function TV on the grid points.  An array to store
    the new set of values TV is optionally supplied (to avoid having to
    allocate new arrays at each iteration).  If supplied, any existing data in 
    Tw will be overwritten.
    '''
    beta, sigma = params
    
    # Apply cubic interpolation to V
    V_func = interpolate.interp1d(s_grid, V, kind='cubic', fill_value='extrapolate')

    # Initialize array for operator and policy function
    TV = np.empty_like(V)
    optI = np.empty_like(TV)

    # here I define my value function
    for i, s in enumerate(s_grid):
        def objective(I):
            value = - uncertainty(shock)[0] * utility(s, I, 0, sigma) 
            - beta * (uncertainty(shock)[1] * V_func(I) + uncertainty(shock)[2] * V_func(I))
            return value
        Iprime_star = fminbound(objective, 1e-6, s - 1e-6)
        optI[i] = Iprime_star
        TV[i] = - objective(Iprime_star)
    return TV, optI



        