import numpy as np


# eqn 5 - this equation does not need to change
def get_L(n_s):
    '''
    Function to compute agg labor supply
    '''
    L = n_s.sum()
    return L


# eqn 6 - this equation does not need to change
def get_K(b):
    '''
    Function to compute agg capital supply
    '''
    K = b.sum()
    return K


# eqn 3 - this equation does not need to change
def get_r(K, L, params):
    '''
    Compute the interest rate from the firm's FOC
    '''
    alpha, delta, A = params
    r = alpha * A * (L/K) ** (1 - alpha) - delta
    return r


# find r as a fn of K/L to plug into eqn 4 to imply w - this equation does not need to change
def get_w(r, params):
    '''
    Solve for the w that is consistant with r from the
    firm's FOC
    '''
    alpha, delta, A = params
    w = (1 - alpha) * A * ((alpha * A) / (r + delta)) ** (alpha / (1 - alpha))
    return w


# u(c) is equation 4.8 in Chapter 4 - this equation does not need to change either!
def mu_c_func(c, sigma):
    '''
    Marginal utility of consumption
    '''
    mu_c = c ** -sigma
    return mu_c


# this equation does not need to change
def get_c(r, w, b_s, b_sp1, n_s):
    '''
    Find consumption using the budget constraint
    and the choice of savings (b_sp1)
    '''
    c = (1 + r) * b_s + w * n_s - b_sp1
    return c

# this equation is the RHS of Equ (4.9)
def mu_n_func(chi, b_param, l_tilde, n_s, nu, S):
    '''
    Marginal utility of n
    '''
    mu_n = -(chi * (b_param/l_tilde) * [(n_s/l_tilde) ** (nu-1)] * (np.ones((S,), dtype=int) - [(n_s/l_tilde) ** nu]) ** [(1-nu)/nu])
    # I use the minus sign here
    return mu_n


# to make sure all FOCs of the household decision hold
def hh_foc(r, w, bn_list, params):
    '''
    Define the household first order conditions
    '''
    sigma, beta, S, chi, b_param, l_tilde, nu = params
    bn_list = np.full((2*S-1), 1e-8, dtype=int)
    # this line is needed to specify that bn_list is a list 
    # I also change 0 to a small number here - may not matter at all
    
    b_s = bn_list[0:S]
    b_s[0] = 0
    b_sp1 = bn_list[0:S]
    b_sp1[-1] = 0
    # I think here we should use [0:S] - similar to what we did in the class
    
    n_s = bn_list[S-1:2*S]
    # same here
    
    c = get_c(r[0], w, b_s, b_sp1, n_s)
    # here i dont know why here the r is a list of 159 so I use a [] here
    mu_c = mu_c_func(c, sigma)
    mu_n = mu_n_func(chi, b_param, l_tilde, n_s, nu, S)
    euler_error = mu_c[:-1] - beta * (1+r[0:S-1]) * mu_c[1:]
    # and ideally we need to have 79 euler equations here 
    # another error and I fixed it - but why is r here is a list?
    euler_error_2 = w * mu_c + mu_n
    # and ideally we need to have 80 euler equations here
    # here we should use + (but if the mu_n is positive then a minus sign is correct)
    
    euler_error_2 = euler_error_2[0,]
    euler_error_list = [*euler_error, *euler_error_2]
    # here we are combining these two lists
    return euler_error_list


