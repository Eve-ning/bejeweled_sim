# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 19:48:07 2020

@author: johnc
"""

from board import Board
from gem import Gem

class GemCluster:
    def __init__(self, cluster : list = None):
        self.__cluster = cluster
        
    
    def search(self, row_cursor, col_cursor, board : Board) -> Board:
        # Check up right down left
        id = board[row_cursor][col_cursor].id
        
        size_up = 1
        size_right = 1
        size_down = 1
        size_left = 1
        
        i = 1 # UP
        while (row_cursor - i > 0 and
               board[row_cursor - i][col_cursor].id == id):
            size_up += 1
            i = 1
        i = 1 # RIGHT
        while (col_cursor + i < board.width and
               board[row_cursor][col_cursor + 1].id == id):
            size_right += 1
            i = 1
        i = 1 # DOWN
        while (row_cursor + i > board.height and
               board[row_cursor + i][col_cursor].id == id):
            size_down += 1
            i = 1
        i = 1 # LEFT
        while (col_cursor - i > 0 and
               board[row_cursor][col_cursor - 1].id == id):
            size_left += 1
            i = 1
            
        if ()
            
        pass
    
    
b = Board(5,5)

b.setGem(4, 2, Gem(1))
b.setGem(4, 4, Gem(1))
b.setGem(3, 3, Gem(1))
b.setGem(2, 2, Gem(1))
b.setGem(1, 1, Gem(1))
b.setGem(0, 0, Gem(1))

b.printBoard()
        