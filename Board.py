'''Board representation'''

from random import choice

import numpy as np

FLAT = 0
HILL = 1
FOREST = 2
CAVE = 3

FOUND = 1
MISSING = 0

BLOCK = 999999999 #Arbitrary large value to prevent selection

class Board:
    '''Representation of the landscape'''

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
            self._known_cleared = np.zeros((dim, dim))

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

    def target_movement(self, update_cleared=True) -> None:
        '''Move the target when there is a new action'''
        neighbors = self.getNeighbors(self.target)
        if len(neighbors) > 0:
            self.target = choice(neighbors)
        if update_cleared:
            self.update_cleared_cells()
        return

    def update_cleared_cells(self) -> None:
        '''Update the cleared cells matrix upon another action'''
        self._known_cleared = np.maximum(np.zeros((self.dim, self.dim)), self._known_cleared - 1)
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
                    self._known_cleared[row][col] = 5 - self.manhattan(neighbor, pos) #Number of turns until the target can walk to the position
                return (False, False)
            return (False, True)
        return (True, True)
    
    def isNearby(self, pos: tuple, radius=5) -> None:
        '''Restrict search space to cells that are nearby'''
        far_cells = [(row, col) for row in range(self.dim) for col in range(self.dim) if (abs(row-pos[0]) + abs(col-pos[1])) > radius]
        for far_cell in far_cells:
            row, col = far_cell
            self._known_cleared[row][col] = max(self._known_cleared[row][col], self.manhattan(far_cell, pos)-(radius+1)) #Number of turns until the target can walk to the position
        return

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

    def bestContains(self) -> tuple:
        '''returns cell with best chance of containing the target'''
        max_pos = self.board.argmax()
        return max_pos//self.dim, max_pos % self.dim

    def bestContainsMoving(self) -> tuple:
        '''Returns cell with best chance out of cells that are not cleared'''
        search_board = self.board * (self._known_cleared == 0)
        max_pos = search_board.argmax()
        return max_pos//self.dim, max_pos % self.dim

    def bestFind(self) -> tuple:
        '''returns cell with best chance of finding the target'''
        temp = np.multiply(self.board, self._board_mask)
        max_pos = temp.argmax()
        return max_pos//self.dim, max_pos % self.dim
    
    def bestFindMoving(self) -> tuple:
        '''Returns cell with best chance out of cells that are not cleared'''
        search_board = np.multiply(self.board, self._board_mask) * (self._known_cleared == 0)
        max_pos = search_board.argmax()
        return max_pos//self.dim, max_pos % self.dim

    def bestDistNumpy(self, pos) -> tuple:
        x_target, y_target = pos
        col_diff, row_diff = np.abs(np.mgrid[-x_target:self.dim-x_target, -y_target:self.dim-y_target])
        distance_mask = col_diff + row_diff + 1
        scores = np.divide(distance_mask, self.board*self._board_mask)
        min_pos = scores.argmin()
        return min_pos // self.dim, min_pos % self.dim

    def bestDistMoving(self, pos) -> tuple:
        '''(Manhattan Distance)/(Probability) heuristic with moving target'''
        x_target, y_target = pos
        col_diff, row_diff = np.abs(np.mgrid[-x_target:self.dim-x_target, -y_target:self.dim-y_target])
        distance_mask = col_diff + row_diff + 1
        distance_mask = distance_mask * np.where(self._known_cleared == 0, 1, BLOCK) #Prevent those which have been cleared from being chosen
        scores = np.divide(distance_mask, self.board*self._board_mask)
        min_pos = scores.argmin()
        return min_pos // self.dim, min_pos % self.dim

    def bestWeightedDist(self, pos) -> tuple:
        '''Utilizes a similar manhattan dist/probability heuristic, but weighted'''
        x_target, y_target = pos
        col_diff, row_diff = np.abs(np.mgrid[-x_target:self.dim-x_target, -y_target:self.dim-y_target])
        distance_mask = col_diff + row_diff + 1
        distance_mask = np.maximum(np.ones((self.dim, self.dim)), distance_mask-5)
        scores = np.divide(distance_mask, self.board*self._board_mask)
        min_pos = scores.argmin()
        return min_pos // self.dim, min_pos % self.dim

    def bestWeightedDist2(self, pos) -> tuple:
        '''Utilizes a similar manhattan dist/probability heuristic, but weighted'''
        x_target, y_target = pos
        col_diff, row_diff = np.abs(np.mgrid[-x_target:self.dim-x_target, -y_target:self.dim-y_target])
        distance_mask = (col_diff + row_diff + 1) * 0.5
        distance_mask = np.maximum(np.ones((self.dim, self.dim)), distance_mask-5)
        scores = np.divide(distance_mask, self.board*self._board_mask)
        min_pos = scores.argmin()
        return min_pos // self.dim, min_pos % self.dim

    def bestLocal(self, pos, x:int) -> tuple:
        '''Rule 1 implementation - Returns cell with highest chance of containing target within radius x around pos'''
        #Generate all valid neighbors
        neighborhood = [(row, col) for row in range(max(0, pos[0]-x), min(self.dim, pos[0]+x+1)) for col in range(max(0, pos[1]-x), min(self.dim, pos[1]+x+1)) if (abs(row-pos[0]) + abs(col-pos[1])) <= x]
        return max(neighborhood, key = lambda y: self.board[y[0]][y[1]]) #Return index with max probability
    
    def bestLocalMoving(self, pos, x:int) -> tuple:
        '''Rule 1 implementation - Returns cell with highest chance of containing target within radius x around pos'''
        #Generate all valid neighbors
        neighborhood = [(row, col) for row in range(max(0, pos[0]-x), min(self.dim, pos[0]+x+1)) for col in range(max(0, pos[1]-x), min(self.dim, pos[1]+x+1)) if (abs(row-pos[0]) + abs(col-pos[1])) <= x]
        return max(neighborhood, key = lambda y: self.board[y[0]][y[1]] * (self._known_cleared[y[0]][y[1]] == 0)) #Return index with max probability

    def bestLocal2(self, pos, x:int) -> tuple:
        '''Rule 2 implementation - Returns cell with highest chance of finding target within radius x around pos'''
        #Generate all valid neighbors
        neighborhood = [(row, col) for row in range(max(0, pos[0]-x), min(self.dim, pos[0]+x+1)) for col in range(max(0, pos[1]-x), min(self.dim, pos[1]+x+1)) if (abs(row-pos[0]) + abs(col-pos[1])) <= x]
        return max(neighborhood, key = lambda y: self.board[y[0]][y[1]]*self._board_mask[y[0]][y[1]]) #Return index with max probability
    
    def bestLocal2Moving(self, pos, x:int) -> tuple:
        '''Rule 2 implementation - Returns cell with highest chance of finding target within radius x around pos'''
        #Generate all valid neighbors
        neighborhood = [(row, col) for row in range(max(0, pos[0]-x), min(self.dim, pos[0]+x+1)) for col in range(max(0, pos[1]-x), min(self.dim, pos[1]+x+1)) if (abs(row-pos[0]) + abs(col-pos[1])) <= x]
        return max(neighborhood, key = lambda y: self.board[y[0]][y[1]] * self._board_mask[y[0]][y[1]] * (self._known_cleared[y[0]][y[1]] == 0)) #Return index with max probability

    def bestLocal3(self, pos, x:int) -> tuple:
        '''Dist rule implementation - Returns cell with highest chance of finding target within radius x around pos'''
        #Generate all valid neighbors
        neighborhood = [(row, col) for row in range(max(0, pos[0]-x), min(self.dim, pos[0]+x+1)) for col in range(max(0, pos[1]-x), min(self.dim, pos[1]+x+1)) if (abs(row-pos[0]) + abs(col-pos[1])) <= x]
        return min(neighborhood, key = lambda y: ((self.manhattan(pos, y)+1) * (((self._known_cleared[y[0]][y[1]] != 0) * BLOCK) + 1))/(self.board[y[0]][y[1]]*self._board_mask[y[0]][y[1]])) #Return index with max probability