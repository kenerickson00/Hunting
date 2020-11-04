'''Agents for moving through boards'''

from Board import Board, FLAT, HILL, FOREST, CAVE, FOUND, MISSING
import numpy as np

def basicAgent1(board: Board) -> int:
    '''search cells with the highest chance of containing the target first. Move to neighbors only. Searching the current cell and moving to another cell both count as actions. Returns the number of actions taken'''
    actions = 0
    best_cell = (-1,-1)
    curcell = (-1,-1)
    while True: #continue until target is found
        actions += 1 #take 1 action per turn
        if curcell = (-1,-1): #first turn, choose random cell
            curcell = np.random.choice(board.dim,2,True)
            nb = board.getNeighbors(curcell)
            if len(nb) > 0: #all cells are equal probability, so choose a neighbor
                best_cell = nb[0]
        elif not curcell == best_cell:
            curcell = board.moveTowards(curcell, best_cell)
            continue #move towards best cell
        b = board.explore(curcell) #explore current cell
        if b: #found target, stop
            break
        #otherwise, update probability of searched cell
        if board._board[curcell[0]][curcell[1]] == FLAT:
            board.board[curcell[0]][curcell[1]] = board.board[curcell[0]][curcell[1]]*0.1
        elif board._board[curcell[0]][curcell[1]] == HILL:
            board.board[curcell[0]][curcell[1]] = board.board[curcell[0]][curcell[1]]*0.3
        elif board._board[curcell[0]][curcell[1]] == FOREST:
            board.board[curcell[0]][curcell[1]] = board.board[curcell[0]][curcell[1]]*0.7
        else:
            board.board[curcell[0]][curcell[1]] = board.board[curcell[0]][curcell[1]]*0.9
        if curcell == best_cell: #find new best cell
            best_cell = board.bestContains()
    return actions

def basicAgent2(board: Board):
    '''search cells with the highest chance of finding the target first (cells with lower false positive rates). Move to neighbors only. Searching the current cell and moving to another cell both count as actions'''
    return

def basicAgent3(board: Board):
    '''score each cell with (manhattan distance)/(probabily of finding target) and travel to the cell with the lowest score. Move to neighbors only. Searching the current cell and moving to another cell both count as actions'''
    return

def improvedAgent(board: Board):
    '''our agent, should beat the three basic agents'''
    return

def moveAnyAgent(board: Board):
    '''agent for a board with a moving target. Can move to any space on the board each turn.'''
    return

def moveCloseAgent(board: Board):
    '''agent for a board with a moving target. Can only move to neighbors of the current cell each turn.'''
    return
