'''Agents for moving through boards'''

from Board import Board, FLAT, HILL, FOREST, CAVE, FOUND, MISSING
import numpy as np

def rule1(board: Board) -> int:
    '''search cell with the highest chance of containing the target first. returns the number of searches'''
    searches = 0
    while True: #continue until target is found
        searches += 1 #one search per turn
        cell = board.bestContains()
        if board.explore(cell) == FOUND:
            break
        #otherwise, update probability of searched cell
        board.update_probability(cell)
    return searches

def rule2(board: Board):
    '''search cell with the highest chance of finding the target first (cells with lower false positive rates). returns the number of searches'''
    searches = 0
    while True: #continue until target is found
        searches += 1 #one search per turn
        cell = board.bestFind()
        if board.explore(cell) == FOUND:
            break
        #otherwise, update probability of searched cell
        board.update_probability(cell)
    return searches

def basicAgent1(board: Board) -> int:
    '''search cells with the highest chance of containing the target first. Move to neighbors only. Searching the current cell and moving to another cell both count as actions. Returns the number of actions taken.'''
    actions = 0
    best_cell = (-1,-1)
    curcell = board.bestContains() #Start on best cell
    while True: #continue until target is found
        actions += 1 #Exploring the cell is an action
        #Explore the cell
        if board.explore(curcell) == FOUND:
            break
        #Update probabilities
        board.update_probability(curcell)
        #Find the next smallest
        best_cell = board.bestContains()
        actions += board.manhattan(curcell, best_cell) #Add the actions of moving to the new location
        curcell = best_cell
    return actions

def basicAgent2(board: Board):
    '''search cells with the highest chance of finding the target first (cells with lower false positive rates). Move to neighbors only. Searching the current cell and moving to another cell both count as actions.'''
    actions = 0
    best_cell = (-1,-1)
    curcell = board.bestFind() #Start on best cell
    while True: #continue until target is found
        actions += 1 #Exploring the cell is an action
        #Explore the cell
        if board.explore(curcell) == FOUND:
            break
        #Update probabilities
        board.update_probability(curcell)
        #Find the next smallest
        best_cell = board.bestFind()
        actions += board.manhattan(curcell, best_cell) #Add the actions of moving to the new location
        curcell = best_cell
    return actions

def basicAgent3(board: Board):
    '''score each cell with (manhattan distance)/(probabily of finding target) and travel to the cell with the lowest score. Move to neighbors only. Searching the current cell and moving to another cell both count as actions'''
    actions = 0
    best_cell = (-1,-1)
    curcell = board.bestFind() #Start on best cell
    while True: #continue until target is found
        actions += 1 #Exploring the cell is an action
        #Explore the cell
        if board.explore(curcell) == FOUND:
            break
        #Update probabilities
        board.update_probability(curcell)
        #Find the next smallest
        best_cell = board.bestDist(curcell)
        actions += board.manhattan(curcell, best_cell) #Add the actions of moving to the new location
        curcell = best_cell
    return actions

def basicAgent4(board: Board):
    '''score each cell with (manhattan distance)/(probabily of finding target) and travel to the cell with the lowest score. Move to neighbors only. Searching the current cell and moving to another cell both count as actions'''
    actions = 0
    best_cell = (-1,-1)
    curcell = board.bestFind() #Start on best cell
    while True: #continue until target is found
        actions += 1 #Exploring the cell is an action
        #Explore the cell
        if board.explore(curcell) == FOUND:
            break
        #Update probabilities
        board.update_probability(curcell)
        #Find the next smallest
        best_cell = board.bestDistNumpy(curcell)
        actions += board.manhattan(curcell, best_cell) #Add the actions of moving to the new location
        curcell = best_cell
    return actions

def improvedAgent(board: Board):
    '''our agent, should beat the three basic agents. Possible design of an improved agent. Finds best cell in a small radius around the current location (local search)'''
    x = int(board.dim/5) #set box radius based on dim
    if x < 1:
        x = 1
    actions = 0
    best_cell = (-1,-1)
    curcell = board.bestFind()
    while True: #continue until target is found
        actions += 1 #take 1 action per turn
        if board.explore(curcell) == FOUND:
            break
        #otherwise, update probability of searched cell
        board.update_probability(curcell)
        best_cell = board.bestLocal(curcell,x)
        actions += board.manhattan(curcell, best_cell) #Add the actions
        curcell = best_cell
    return actions

def moveAnyAgent(board: Board):
    '''agent for a board with a moving target. Can move to any space on the board each turn. Use basicAgent1 strategy to search spaces until we get close to the target, then use local search. Return the number of searches.'''
    target_nearby = False
    searches = 0
    while True: #continue until target is found
        searches += 1 #one search per turn
        if target_nearby and searches > 1:
            cell = board.bestLocal(cell,5)
        else: #Should probably have a better algorithm for this
            cell = board.bestContains()
        found_target, target_nearby = board.exploreMove(cell) #explore current cell
        if found_target: #found target, stop
            break
        #otherwise, update probability of searched cell
        board.update_probability(cell)
    return searches

def moveCloseAgent(board: Board):
    '''agent for a board with a moving target. Can only move to neighbors of the current cell each turn. Use basicAgent3 strategy to find spaces until we get close to target, then use local search. Returns number of actions taken.'''
    target_nearby = False
    actions = 0
    best_cell = (-1,-1)
    curcell = board.bestFind()
    while True: #continue until target is found
        actions += 1 #take 1 action per turn
        found_target, target_nearby = board.exploreMove(curcell) #explore current cell
        if found_target: #found target, stop
            break
        #otherwise, update probability of searched cell
        board.update_probability(curcell)
        if curcell == best_cell: #find new best cell
            if target_nearby:
                best_cell = board.bestLocal(curcell,5)
            else:
                best_cell = board.bestDistNumpy(curcell)
        if target_nearby:
            best_cell = board.bestLocal(curcell,5)
        else:
            best_cell = board.bestDistNumpy(curcell)
        actions += board.manhattan(curcell, best_cell) #Add the actions of moving to the new location
        curcell = best_cell
    return actions
