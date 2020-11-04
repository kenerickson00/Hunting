'''Agents for moving through boards'''

from Board import Board, FLAT, HILL, FOREST, CAVE, FOUND, MISSING

def basicAgent1():
    '''search cells with the highest chance of containing the target first. Move to neighbors only. Searching the current cell and moving to another cell both count as actions'''
    return

def basicAgent2():
    '''search cells with the highest chance of finding the target first (cells with lower false positive rates). Move to neighbors only. Searching the current cell and moving to another cell both count as actions'''
    return

def basicAgent3():
    '''score each cell with (manhattan distance)/(probabily of finding target) and travel to the cell with the lowest score. Move to neighbors only. Searching the current cell and moving to another cell both count as actions'''
    return

def improvedAgent():
    '''our agent, should beat the three basic agents'''
    return

def moveAnyAgent():
    '''agent for a board with a moving target. Can move to any space on the board each turn.'''
    return

def moveCloseAgent():
    '''agent for a board with a moving target. Can only move to neighbors of the current cell each turn.'''
    return
