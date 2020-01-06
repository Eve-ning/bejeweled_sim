# -*- coding: utf-8 -*-
"""
Created on Sat Jan  4 23:36:50 2020

@author: johnc
"""

class Gem:
    def __init__(self, id):
        self.__id = id
        self.__mark = False
        
    @property
    def id(self):
        return self.__id
    
    @id.setter
    def id(self, value):
        self.__id = value
        
    # Mark is a flag use to indicate the gem for destruction
    @property
    def mark(self):
        return self.__mark
    
    @mark.setter
    def mark(self, value):
        self.__mark = value
    

        