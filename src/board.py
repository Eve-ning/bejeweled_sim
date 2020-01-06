# -*- coding: utf-8 -*-
"""
Created on Sat Jan  4 21:25:01 2020

@author: johnc
"""

from gem import Gem
import random

class Board:
    def __init__(self, height, width):
        self.board = None
        self.__height = height
        self.__width = width
        self.createBoard()
        
    @property
    def height(self):
        return self.__height
    
    @height.setter
    def height(self, value):
        self.__height = value
        
    @property
    def width(self):
        return self.__width
    
    @width.setter
    def width(self, value):
        self.__width = value
        
    def createBoard(self):
        self.board = [[Gem(0) for i in range(self.__height)]
                              for i in range(self.__width)]
        
    def randomizeBoard(self, id_list):
        for row in self.board:
            for gem in row:
                gem.id = random.choice(id_list)
        
    def printBoard(self):
        for row in self.board:
            for gem in row:
                print(gem.id, end = " ")
            print(end = "\n")
            
    def printMark(self):
        for row in self.board:
            for gem in row:
                print('O' if gem.mark else 'X', end = " ")
            print(end = "\n")

    def getGem(self, row, column):
        return self.board[row][column]
    def setGem(self, row, column, gem):
        self.board[row][column] = gem
        
    def fall(self, blank_id = 0):
        # This function makes the gems fall
        
        # The function checks every gem if there's a blank space under them
        # if so, then move them down
        # This is also the reason why there's [1]
        
        for i in range(self.__height): # [1]
            for row_i in range(self.__height - 1):
                for col_i in range(self.__width):
                    gem_from = self.board[row_i][col_i]
                    gem_to = self.board[row_i + 1][col_i]
                    if (gem_from.id != blank_id and \
                        gem_to.id == blank_id):
                        # Create new Gem
                        self.board[row_i + 1][col_i] = \
                            self.board[row_i][col_i]
                        # Remove old Gem (create blank gem)
                        self.board[row_i][col_i] = Gem(blank_id)
        
    # Marks a specific Gem                
    def mark(self, row, column, value = True):
        self.board[row][column].mark = value

    def markScanRight(self, row, column, scan_size):
        mark_id = self.board[row][column].id
        for scan_i in range(1, scan_size): 
            # Checks if 2nd~ scan Gem matches
            if (self.board[row][column + scan_i].id != mark_id):
                return False
        return True
    
    def markScanDown(self, row, column, scan_size):
        mark_id = self.board[row][column].id
        for scan_i in range(1, scan_size): 
            # Checks if 2nd~ scan Gem matches
            if (self.board[row + scan_i][column].id != mark_id):
                return False
        return True
    
    def markAll(self, scan_size):
        # Slides a nx1 scan to check if there are gems that can be marked
        
        # Slide a wide scan
        #  0 0 0
        # [0 0 0]
        #  0 0 0 
        for row in range(self.__height):
            for column in range(self.__width - scan_size + 1):
                if (self.markScanRight(row, column, scan_size)):
                    for scan_i in range(scan_size):
                        self.board[row][column + scan_i].mark = True
        # Slide a tall scan
        #  0 [0] 0
        #  0 [0] 0
        #  0 [0] 0                 
        for row in range(self.__height - scan_size + 1):
            for column in range(self.__width):
                if (self.markScanDown(row, column, scan_size)):
                    for scan_i in range(scan_size):
                        self.board[row + scan_i][column].mark = True
                        
b = Board(10,10)
b.randomizeBoard([1,2,3])
b.printBoard()
print()
b.markAll(3)
b.printMark()