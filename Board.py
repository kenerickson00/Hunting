'''Board representation'''

import numpy as np
from random import choice

FLAT = 0
HILL = 1
FOREST = 2
CAVE = 3

FOUND = 1
MISSING = 0

class Board:

    def __init__(self, dim: int, copy_board=None, copy_target=None, moving_target=False):
        self.dim = dim
        if copy_board is None:
            self._board = np.random.choice([FLAT,HILL,FOREST,CAVE], (dim, dim), True, [0.2,0.3,0.3,0.2])
            self.target = (int(np.random.randint(dim)), int(np.random.randint(dim))) #position of the target
        else:
            self._board = copy_board
            self.target = copy_target
        self.board = np.full((dim,dim),1/(dim**2)) #probability of each cell being the target
        self._board_mask = np.ones((dim, dim)) #Probability that you successfully find if they are in the cell
        self._board_mask[self._board == FLAT] *= 0.9
        self._board_mask[self._board == HILL] *= 0.7
        self._board_mask[self._board == FOREST] *= 0.3
        self._board_mask[self._board == CAVE] *= 0.1
        if moving_target:
            self._known_cleared = np.ones((dim, dim))

    #Not used
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
    
    def target_movement(self) -> None:
        '''Move the target when there is a new action'''
        neighbors = self.getNeighbors(self.target)
        if len(neighbors) > 0:
            self.target = choice(neighbors)
        self.update_cleared_cells()
        return
    
    def update_cleared_cells(self) -> None:
        '''Update the cleared cells matrix upon another action'''
        self._known_cleared = np.maximum(np.ones((self.dim, self.dim)), self._known_cleared - 1)
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
            elif terrain == HILL:
                ret = np.random.choice([0,1],1,False,[0.3,0.7])
            elif terrain == FOREST:
                ret = np.random.choice([0,1],1,False,[0.7,0.3])
            else:
                ret = np.random.choice([0,1],1,False,[0.9,0.1])
        if ret == 0:
            if self.manhattan(pos, self.target) > 5:
                #Prevent these cells from being visited again soon, poor python implementation - hopefully can find a proper numpy implementation
                neighborhood = [(row, col) for row in range(max(0, pos[0]-5), min(self.dim, pos[0]+6)) for col in range(max(0, pos[1]-5), min(self.dim, pos[1]+6)) if (abs(row-pos[0]) + abs(col-pos[1])) <= 5]
                for neighbor in neighborhood:
                    row, col = neighbor
                    self._known_cleared[row][col] = 6 - self.manhattan(neighbor, pos) #Number of turns until the target can walk to the position
                return (False, False)
            return (False, True)
        return (True, True)

    def getNeighbors(self, pos: tuple) -> list:
        '''returns a list of all valid neighbors given a position on the board'''
        row, col = pos
        neighbors = []
        if row != 0:
            neighbors.append((row-1, col))
        if row != self.dim-1:
            neighbors.append((row+1, col))
        if col != 0:
            neighbors.append((row, col-1))
        if col != self.dim-1:
            neighbors.append((row, col+1))
        return neighbors

    def manhattan(self, pos1: tuple, pos2: tuple) -> int:
        x = pos2[0] - pos1[0]
        y = pos2[1] - pos1[1]
        if x < 0:
            x = -x
        if y < 0:
            y = -y
        return x + y

    #Not used
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

    def bestContainsMoving(self) -> tuple:
        '''Returns cell with best chance out of cells that are not cleared'''
        search_board = self.board * (self._known_cleared == 1)
        max_pos = search_board.argmax()
        return max_pos//self.dim, max_pos % self.dim

    def bestFind(self) -> tuple:
        '''returns cell with best chance of finding the target'''
        temp = np.multiply(self.board, self._board_mask)
        max_pos = temp.argmax()
        return max_pos//self.dim, max_pos % self.dim

    def bestDist(self, pos) -> tuple:
        '''returns cell with best value of (manhattan dist)/(probability of target)'''
        min = 99999999
        hold = (-1,-1)
        for i in range(self.dim):
            for j in range(self.dim):
                if (i,j) == pos:
                    continue
                if self.board[i][j] != 0:
                    temp = (self.manhattan(pos,(i,j))+1)/self.board[i][j]
                if temp < min:
                    min = temp
                    hold = (i,j)
        return hold

    def bestDistNumpy(self, pos) -> tuple:
        x_target, y_target = pos
        col_diff, row_diff = np.abs(np.mgrid[-x_target:self.dim-x_target, -y_target:self.dim-y_target])
        distance_mask = col_diff + row_diff + 1
        scores = np.divide(distance_mask, self.board)
        min_pos = scores.argmin()
        return min_pos // self.dim, min_pos % self.dim
    
    def bestDistMoving(self, pos) -> tuple:
        '''(Manhattan Distance)/(Probability) heuristic with moving target'''
        x_target, y_target = pos
        col_diff, row_diff = np.abs(np.mgrid[-x_target:self.dim-x_target, -y_target:self.dim-y_target])
        distance_mask = col_diff + row_diff + 1
        distance_mask = distance_mask * np.where(self._known_cleared == 1, self._known_cleared, 99999) #Prevent those which have been cleared from being chosen
        scores = np.divide(distance_mask, self.board)
        min_pos = scores.argmin()
        return min_pos // self.dim, min_pos % self.dim
    
    def bestWeightedDist(self, pos) -> tuple:
        '''Utilizes a similar manhattan dist/probability heuristic, but weighted'''
        x_target, y_target = pos
        col_diff, row_diff = np.abs(np.mgrid[-x_target:self.dim-x_target, -y_target:self.dim-y_target])
        distance_mask = col_diff + row_diff + 1
        distance_mask = np.maximum(np.ones((self.dim, self.dim)), distance_mask-5)
        scores = np.divide(distance_mask, self.board)
        min_pos = scores.argmin()
        return min_pos // self.dim, min_pos % self.dim

    def bestWeightedDist2(self, pos) -> tuple:
        '''Utilizes a similar manhattan dist/probability heuristic, but weighted'''
        x_target, y_target = pos
        col_diff, row_diff = np.abs(np.mgrid[-x_target:self.dim-x_target, -y_target:self.dim-y_target])
        distance_mask = (col_diff + row_diff + 1) * 0.5
        distance_mask = np.maximum(np.ones((self.dim, self.dim)), distance_mask-5)
        scores = np.divide(distance_mask, self.board)
        min_pos = scores.argmin()
        return min_pos // self.dim, min_pos % self.dim

    #Not used
    def isvalid(self, pos):
        if pos[0] < 0 or pos[1] < 0:
            return False
        if pos[0] >= self.dim or pos[1] >= self.dim:
            return False
        return True

    #Not used
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
        #Generate all valid neighbors
        neighborhood = [(row, col) for row in range(max(0, pos[0]-x), min(self.dim, pos[0]+x+1)) for col in range(max(0, pos[1]-x), min(self.dim, pos[1]+x+1)) if (abs(row-pos[0]) + abs(col-pos[1])) <= x]
        return max(neighborhood, key = lambda y: self.board[y[0]][y[1]]) #Return index with max probability
