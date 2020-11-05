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
        self._board = np.random.choice([FLAT,HILL,FOREST,CAVE], (dim, dim), True, [0.2,0.3,0.3,0.2])
        self.board = np.full((dim,dim),1/(dim**2)) #probability of each cell being the target
        self.target = (int(np.random.randint(dim)), int(np.random.randint(dim))) #position of the target
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
    
    def update_probability(self, pos: tuple) -> None:
        '''Update the board probabilities after exploring the cell'''
        if self._board[pos[0]][pos[1]] == FLAT:
            self.board[pos[0]][pos[1]] *= 0.1
        elif self._board[pos[0]][pos[1]] == HILL:
            self.board[pos[0]][pos[1]] *= 0.3
        elif self._board[pos[0]][pos[1]] == FOREST:
            self.board[pos[0]][pos[1]] *= 0.7
        else:
            self.board[pos[0]][pos[1]] *= 0.9
        return

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

    def manhattan(self, pos1: tuple, pos2: tuple) -> int:
        x = pos2[0] - pos1[0]
        y = pos2[1] - pos1[1]
        if x < 0:
            x = -x
        if y < 0:
            y = -y
        return x + y

    def moveTowards(self, pos1: tuple, pos2: tuple) -> tuple:
        '''finds the best neighbor of pos1 to take, if trying to move to pos2'''
        nb = self.getNeighbors(pos1)
        if len(nb) <= 0:
            return None #error
        hold = nb[0]
        least = self.manhattan(nb[0], pos2)
        for i in range(len(nb)-1):
            dist = self.manhattan(nb[i+1], pos2)
            if dist < least:
                least = dist
                hold = nb[i+1]
        return hold

    def bestContains(self) -> tuple:
        '''returns cell with best chance of containing the target'''
        min = -1
        hold = (-1,-1)
        for i in range(self.dim):
            for j in range(self.dim):
                if self.board[i][j] > min:
                    min = self.board[i][j]
                    hold = (i,j)
        return hold

    def bestFind(self) -> tuple:
        '''returns cell with best chance of finding the target'''
        min = -1
        hold = (-1,-1)
        for i in range(self.dim):
            for j in range(self.dim):
                terrian = self._board[i][j]
                if terrain == FLAT:
                    prob = 0.9
                elif terrain == HILL:
                    prob = 0.7
                elif terrain == FOREST:
                    prob = 0.3
                else:
                    prob = 0.1
                temp = self.board[i][j]*prob
                if temp > min:
                    min = temp
                    hold = (i,j)
        return hold

    def bestDist(self, pos) -> tuple:
        '''returns cell with best value of (manhattan dist)/(probability of target)'''
        min = -1
        hold = (-1,-1)
        for i in range(self.dim):
            for j in range(self.dim):
                if (i,j) == pos:
                    continue
                temp = self.manhattan(pos,(i,j))/self.board[i][j]
                if temp > min:
                    min = temp
                    hold = (i,j)
        return hold
