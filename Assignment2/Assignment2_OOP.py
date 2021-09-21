# -*- coding: utf-8 -*-
"""
Created on Sat Sep  4 22:55:20 2021

@author: Siwen Z
"""

class Backpack:
    ''' A Backpack object class - has a name, a color, max_size and a list of contents
    
        Attributes:
            name (str): the name of the owner
            color (str): the color of the backpack
            max_size (int): the maximum size of the contents list
            contents (list): the contents of the backpack.
    '''
    
    def __init__(self, name, color, max_size = 5): # constructor
        ''' Set the name and initialize an empty list of contents
            
            Paramters:
                name (str): the name of the owner
                color (str): the color of the backpack
                max_size (int): the maximum size of the contents list
        '''
    
        self.name = name
        self.color = color
        self.max_size = max_size
        self.contents = []
        
        
    def put(self, item):
        """Add 'item' to the backpack's list of contents. And it contains fewer than 6 elements by default"""
        if len(self.contents) < 5:
            self.contents.append(item)
        else:
            print("No room!")
        
        
    def take(self, item):
        """Remove 'item' from the backpack's list of contents."""
        self.contents.remove(item)
        
        
    def dump(self):
        """Reset the list of contents."""
        self.contents.clear()
        
        

class Jetpack(Backpack):
    """A Jetpack object class. Inherits from the Backpack class.
    A jetpack is used for exploring the sky.
    Attributes:
        name (str): the name of the jetpack's owner.
        color (str): the color of the jetpack.
        max_size (int): the maximum number of items that can fit inside.
        amount_fuel (int): the maximum amount of fuel
        contents (list): the contents of the jetpack.
    """

    def __init__(self, name, color, max_size = 2, amount_fuel = 10): # constructor
        ''' Set the name and initialize an empty list of contents
            
            Paramters:
                name (str): the name of the owner
                color (str): the color of the backpack
                max_size (int): the maximum size of the contents list and is set to 2 by default
                amount_fuel (int): the maximum amount of fuel set to 10 by default
        '''

        self.name = name
        self.color = color
        self.max_size = max_size
        self.amount_fuel = amount_fuel
        self.contents = []


    def fly(self, number): 
        """Count the fuel used by the owner and it will be run out of by 10 (gal) by default."""
        if number <= self.amount_fuel:
            self.amount_fuel = self.amount_fuel - number
        else:
            print("Not enough fuel!")
            
            
    def dump(self):
        """Reset the list of contents and the amount of fule."""
        self.contents.clear()
        self.amount_fuel.clear()

