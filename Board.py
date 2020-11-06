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
        self._board_mask = np.ones((dim, dim)) #Probability that you successfully find if they are in the cell
        self._board_mask[self._board == FLAT] *= 0.9
        self._board_mask[self._board == HILL] *= 0.7
        self._board_mask[self._board == FOREST] *= 0.3
        self._board_mask[self._board == CAVE] *= 0.1
        searched = np.full((dim,dim),0) #count the number of times each cells has been searched

    def newTarget(self):
        ind = np.random.choice(1,dim**2)
        self.target = (ind//dim)(ind%dim)

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

    def exploreMove(self, pos: tuple) -> tuple:
        '''explore for moving targets, returns a tuple containing (found/missing target, bool of whether the target is within 5 manhattan distance)'''
        if pos[0] < 0 or pos[1] < 0 or pos[0] >= self.dim or pos[1] >= self.dim:
            return -1 #invalid
        if not self.target == pos:
            ret = 0
        else:
            terrain = self._board[pos[0]][pos[1]]
            if terrain == FLAT:
                ret = np.random.choice([0,1],1,False,[0.1,0.9])
            if terrain == HILL:
                ret = np.random.choice([0,1],1,False,[0.3,0.7])
            if terrain == FOREST:
                ret = np.random.choice([0,1],1,False,[0.7,0.3])
            else:
                ret = np.random.choice([0,1],1,False,[0.9,0.1])
        if ret == 0:
            target = np.random.choice(self.getNeighbors(target),1) #move target to random neighbor
            if self.manhattan(pos,target) > 5:
                return (0,False)
            return (0,True)
        return (1,True)

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
        max_pos = self.board.argmax()
        return max_pos//self.dim, max_pos % self.dim

    def bestFind(self) -> tuple:
        '''returns cell with best chance of finding the target'''
        temp = np.multiply(self.board, self._board_mask)
        max_pos = temp.argmax()
        return max_pos//self.dim, max_pos % self.dim

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

    def isvalid(self, pos):
        if pos[0] < 0 or pos[1] < 0:
            return False
        if pos[0] >= self.dim or pos[1] >= self.dim:
            return False
        return True

    def box(self, pos, x) -> set:
        '''returns an set of cells that are at most x spaces away from pos'''
        s = set()
        for i in range(x):
            for j in range(x):
                if x == 0 and y == 0:
                    continue
                if self.isvalid(pos+(i,j)):
                    s.add(pos+(i,j))
                if self.isvalid(pos+(-i,j)):
                    s.add(pos+(-i,j))
                if self.isvalid(pos+(i,-j)):
                    s.add(pos+(i,-j))
                if self.isvalid(pos+(-i,-j)):
                    s.add(pos+(-i,-j))
        return s

    def bestLocal(self, pos, x) -> tuple:
        '''returns cell with highest chance of being the target within a box of radius x around pos'''
        bx = self.box(pos, x)
        min = -1
        hold = (-1,-1)
        for p in bx:
            if self.board[p[0]][p[1]] > min:
                min = self.board[p[0]][p[1]]
                hold = p
        return hold
