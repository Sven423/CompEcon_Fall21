#import SS as ss
from SS import ss_solver
import numpy as np
import matplotlib.pyplot as plt


# set parameters
S = 80
beta = 0.8
sigma = 1.5
l_tilde = 1.0
b_param = .501
nu = 1.554
chi = np.ones(S)
A = 1.0
alpha = 0.3
delta = 0.1

params = alpha, delta, A, sigma, beta, S, chi, b_param, l_tilde, nu


# make initial guesses

r_guess = 0.1
guess_par = 0.01
bn_guesses = guess_par * np.ones((2*S-1), dtype=int)
# these initial guesses cannot be all zeros

r_ss, L_ss, K_ss, success, euler_errors = ss_solver(r_guess, bn_guesses, params)

print('The SS interest rate is ', r_ss, 'Did we find the solution?', success)
print('The euler error is ', euler_errors)


# attempts to plot
plt.figure()
plt.plot(c_ss, age)
plt.xlabel('Age')
plt.ylabel('Units of consumption')
plt.title('Steady-state distribution of consumptions and savings')
plt.show()
