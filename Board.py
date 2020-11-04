'''Board representation'''

import numpy as np

FLAT = 0
HILL = 1
FOREST = 2
CAVE = 3

FOUND = 1
MISSING = 0

class Board:

    def __init__(self, dim: int):
        self.dim = dim
        terrain = np.random.choice([FLAT,HILL,FOREST,CAVE], dim**2, False, [0.2,0.3,0.3,0.2])
        i = 0
        j = 0
        for el in terrain:
            self._board[i][j] = el
            i += 1
            if i >= self.dim:
                i = 0
                j += 1
        self.board = np.full((dim,dim),1/(dim**2)) #probability of each cell being the target
        ind = np.random.choice(1,dim**2)
        target = (ind//dim)(ind%dim) #position of the target
        searched = np.full((dim,dim),0) #count the number of times each cells has been searched

    def explore(self, pos: tuple) -> int:
        if pos[0] < 0 or pos[1] < 0 or pos[0] >= self.dim or pos[1] >= self.dim:
            return -1 #invalid
        if not self.target == pos:
            return MISSING
        terrain = self._board[pos[0]][pos[1]]
        if terrain == FLAT:
            return np.random.choice([0,1],1,False,[0.1,0.9])
        if terrain == HILL:
            return np.random.choice([0,1],1,False,[0.3,0.7])
        if terrain == FOREST:
            return np.random.choice([0,1],1,False,[0.7,0.3])
        if terrain == CAVE:
            return np.random.choice([0,1],1,False,[0.9,0.1])
        return -1 #should never reach here

    def getNeighbors(self, pos: tuple) -> list:
        '''returns a list of all valid neighbors given a position on the board'''
        r = pos[0]
        c = pos[1]
        if r < 0 or c < 0 or r >= self.dim or c >= self.dim:
            return []
        if r == 0:
            if c == 0:
                return [(r+1,c),(r,c+1)]
            elif c == self.dim-1:
                return [(r+1,c),(r,c-1)]
            return [(r+1,c),(r,c+1),(r,c-1)]
        if r == self.dim-1:
            if c == 0:
                return [(r-1,c),(r,c+1)]
            elif c == self.dim-1:
                return [(r-1,c),(r,c-1)]
            return [(r-1,c),(r,c+1),(r,c-1)]
        return [(r+1,c),(r-1,c),(r,c+1),(r,c-1)]
