# -*- coding: utf-8 -*-
"""
Created on Sat Sep  4 16:58:14 2021

@author: Siwen Z
"""

import numpy as np


# Problem1 in Standardlib file: Write a function that accepts a list L and returns the minimum, maximum, and average of the entries of L (in that order). Can you implement this function in a single line?
def min_max_mean(x = []):
    return [min(x), max(x), sum(x) / len(x)]

min_max_mean([1, 2, 3])


# Problem2 in Standardlib file: decide if they are mutable or not:
int1 = 1
int2 = int1
int1 = 2
int1 == int2 # false - so int is immutable

str1 = '1'
str2 = str1
str1 = '2'
str1 == str2 # false - so str is also immutable

list1 = [1,2,3,4]
list2 = list1
list1[2] = 0
list1 == list2 # true - so list is mutable

tup1 = (1,2,3,4)
tup2 = tup1
tup1[2] = 0 # no - tuple does not support the changes - immutable

set1 = {1,2,3,4}
set2 = set1
set1[0] = 0 # no - set does not support the changes - immutable


# Problem3 in Standardlib file: create and import a module:

import Assignment2_calculator as calculator  

def two_sides_ofaTriangle(a,b):
    if a > 0: 
        hypotenuse = calculator.sqrt(calculator.sum_two(a, b) ** 2 - 2 * calculator.product_two(a, b))
        return f"Yes, they can be two sides of a triangle! And the length of the hypotenuse is {hypotenuse}"
        # return a number and a string
    else:
        return "Sorry, they couldn't work out!"

two_sides_ofaTriangle(2,4)


# Problem1 in Numpy file: matrix multiplication
def matrix_multiplication(x = [], y = []):
    x1 = np.array(x)
    y1 = np.array(y)
    return np.dot(x1, y1)

matrix_multiplication([[3, -1, 4],[1, 5, -9]], [[2, 6, -5, 3], [5, -8, 9, 7], [9, -3, -2, -3]])


# Problem2 in Numpy file: matrix calculation
def matrix_calculation(x = []):
    x1 = np.array(x)
    x2 = np.dot(x1, x1)
    return -np.dot(x2, x1) + 9 * np.dot(x1, x1) - 15 * x1

matrix_calculation([[3, 1, 4], [1, 5, 9], [ -5, 3, 1]])
# why the anwser is not right? - because np.dot only takes two arguments!


# Problem5 in Numpy file: numpy stacking
def matrix_stacking(A = [], B = [], C = []):
    A1 = np.array(A)
    B1 = np.array(B)
    C1 = np.array(C)
    # S_mat = np.block(((np.zeros((3, 3)), A1, B1), (np.transpose(A1), np.zeros((2, 2)), np.zeros((3, 2))), (np.eye(3), np.zeros((3, 2)), C1)))
    S_mat = np.block([[np.zeros((3, 3)), A1, B1], [np.transpose(A1), np.zeros((2, 2)), np.zeros((3, 2))], [np.eye(3), np.zeros((3, 2)), C1]])
    return S_mat
# block fn can only use lists! NO TUPLES - but not working either: ValueError: all the input array dimensions for the concatenation axis must match exactly, but along dimension 0, the array at index 0 has size 3 and the array at index 1 has size 

matrix_stacking([[0, 2, 4], [1, 3, 5]], [[3, 0, 0], [3, 3, 0], [3, 3, 3]], [[-2, 0, 0], [0, -2, 0], [0, 0, -2]])
# what went wrong?


# Problem1 in OOP file: expand the class

from Assignment2_OOP import Backpack
my_backpack = Backpack('Siwen', 'Green')
type(my_backpack)

print(my_backpack.name, my_backpack.color, my_backpack.contents)    

for i in range(5):    
    my_backpack.put('i')

my_backpack.put("5")
my_backpack.contents # works!
my_backpack.dump() # works!


''' TESTING the backpack class:
def test_backpack():
    testpack = Backpack("Barry", "black")
 # Instantiate the object.

    if testpack.name != "Barry":
 # Test an attribute.
        print("Backpack.name assigned incorrectly")
    for item in ["pencil", "pen", "paper", "computer"]:
        testpack.put(item)
 # Test a method.
    print("Contents:", testpack.contents)
'''

# Problem2 in OOP file: Inherited class

from Assignment2_OOP import Jetpack
my_jetpack = Jetpack('Siwen', 'Green')
type(my_jetpack) # yes it is working!

my_jetpack.fly(10)
my_jetpack.amount_fuel # right!

    