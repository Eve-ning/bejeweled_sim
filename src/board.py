# -*- coding: utf-8 -*-
"""
Created on Sat Jan  4 21:25:01 2020

@author: johnc
"""

from gem import Gem
import random
import copy

class Board:
    def __init__(self, height, width, id_list, blank_id = 0, DEBUG = False):
        # Note that 0 != '0'
        self.board = None
        self.__height = height
        self.__width = width
        self.__blank_id = blank_id
        self.__id_list = id_list
        self.__DEBUG = DEBUG
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
        self.board = [[Gem(self.__blank_id) for i in range(self.__width)]
                                            for i in range(self.__height)]
        
    def randomizeBoard(self):
        for row in self.board:
            for gem in row:
                gem.id = random.choice(self.__id_list)
        
        
    def printBoard(self):
        for row in self.board:
            for gem in row:
                print(gem.id, end = " ")
            print("\t", end = " ")
            for gem in row:
                print('O' if gem.mark else 'X', end = " ")
            print(end = "\n")

    def getBoard(self):
        return self.board

    def getGem(self, row, col, clip = True):
        if (clip):
            row = 0 if row < 0 else row
            row = self.__height - 1 if row >= self.__height else row
            col = 0 if col < 0 else col
            col = self.__width - 1 if col >= self.__width else col
        return self.board[row][col]
    def setGem(self, row, col, gem, clip = True):
        if (clip):
            row = 0 if row < 0 else row
            row = self.__height - 1 if row >= self.__height else row
            col = 0 if col < 0 else col
            col = self.__width - 1 if col >= self.__width else col
        self.board[row][col] = gem
        
    def fall(self):
        # This function makes the gems fall
        
        # The function checks every gem if there's a blank space under them
        # if so, then move them down
        # This is also the reason why there's [1]
        
        for i in range(self.__height): # [1]
            for row in range(self.__height - 1):
                for col in range(self.__width):
                    gem_from = self.getGem(row, col)
                    gem_to = self.getGem(row + 1, col)
                    if (gem_from.id != self.__blank_id and \
                        gem_to.id == self.__blank_id):
                        # Create new Gem
                        self.setGem(row + 1, col, self.getGem(row, col))
                        # Remove old Gem (create blank gem)
                        self.setGem(row, col, Gem(self.__blank_id))
        
    def fill_random(self):
        # This algorithm fills all blank_ids
        # Note that it's regardless of if it's after or before fall()
        for row in self.board:
            for gem in row:
                if (gem.id == self.__blank_id):
                    gem.id = random.choice(self.__id_list)
        
    def matchAlgorithm(self, scan_size = 3):
        # This is the master algorithm on how the gems should match
        count_list = []
        n = 1
        while (True):
            count = self.markScan(scan_size)
            if (len(count) > 0):
                if (self.__DEBUG):
                    print("[" + str(n) + "]")
                    self.printBoard()
                    print()
                n += 1
                self.markDestroy()
                self.fall()
                self.fill_random()
                count_list.append(count)
            else:
                if (self.__DEBUG):
                    print("[" + str(n) + " END]")
                    self.printBoard()
                    print()
                break
        return count_list
        
    # Marks a specific Gem                
    def mark(self, row, col, value = True):
        self.board[row][col].mark = value
    
    def unmarkAll(self):
        for row in self.board:
            for gem in row:
                gem.mark = False
    
    def markScan(self, scan_size):
        # Slides a nx1 scan to check if there are gems that can be marked
        # A marked gem is part of a match
        
        self.unmarkAll()
        
        def markScanWide(row, col, scan_size):
            mark_id = self.board[row][col].id
            for scan_i in range(1, scan_size): 
                # Checks if 2nd~ scan Gem matches
                if (self.getGem(row, col + scan_i).id != mark_id):
                    return False
            return True
        
        # Slide a wide scan
        #  2 1 2
        # [1 1 1]
        #  2 1 2 
        for row in range(self.__height):
            for col in range(self.__width - scan_size + 1):
                if (self.board[row][col].id != self.__blank_id and
                    markScanWide(row, col, scan_size)):
                    for scan_i in range(scan_size):
                        self.mark(row, col + scan_i)
                        
        def markScanTall(row, col, scan_size):
            mark_id = self.board[row][col].id
            for scan_i in range(1, scan_size): 
                # Checks if 2nd~ scan Gem matches
                if (self.getGem(row + scan_i, col).id != mark_id):
                    return False
            return True

        # Slide a tall scan
        #  2 [1] 2
        #  1 [1] 1
        #  2 [1] 2                 
        for row in range(self.__height - scan_size + 1):
            for col in range(self.__width):
                if (self.board[row][col].id != self.__blank_id and 
                    markScanTall(row, col, scan_size)):
                    for scan_i in range(scan_size):
                        self.mark(row + scan_i, col)   
        
        return self.markCount()
                        
    # Out: [ID, X, Y, Count]
    def markCount(self) -> list:
        # Saves current board status to reset marks on line [1]
        board_save = copy.deepcopy(self.board) 
        
        def markCountCrawl(row, col, id):
            # This function recursively calls itself and counts how many marked
            # and matching ids there are (up, right, down, left)
            
            self.mark(row, col, False) # Unmark those that are counted
            
            if (self.getGem(row + 1, col).id == id and
                self.getGem(row + 1, col).mark):
                self.__markCountCrawlVal += 1
                markCountCrawl(row + 1, col, id)
                
            if (self.getGem(row, col + 1).id == id and
                self.getGem(row, col + 1).mark):
                self.__markCountCrawlVal += 1
                markCountCrawl(row, col + 1, id)
                    
            if (self.getGem(row - 1, col).id == id and
                self.getGem(row - 1, col).mark):
                self.__markCountCrawlVal += 1
                markCountCrawl(row - 1, col, id)
                
            if (self.getGem(row, col - 1).id == id and
                self.getGem(row, col - 1).mark):
                self.__markCountCrawlVal += 1
                markCountCrawl(row, col - 1, id)
            return self.__markCountCrawlVal
        
        list_out = []
        for row in range(self.__height):
            for col in range(self.__width):
                if (self.getGem(row, col).mark):
                    self.__markCountCrawlVal = 1
                    id = self.getGem(row, col).id
                    list_out.append([id, row, col, markCountCrawl(row, col, id)])
        
        self.board = board_save # [1]
        
        return list_out
    
    def markDestroy(self):
        
        for row in range(self.__height):
            for col in range(self.__width):
                if (self.board[row][col].mark):
                    self.board[row][col].id = self.__blank_id
                    self.board[row][col].mark = False
    
b = Board(10,10, ['+', '|', '-', '*'], ' ', True)
b.randomizeBoard()

t= b.matchAlgorithm()
