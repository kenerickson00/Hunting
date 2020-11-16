'''Agents for moving through boards'''

from Board import Board, FLAT, HILL, FOREST, CAVE, FOUND, MISSING
import numpy as np

def rule1(board: Board, moving_target=False) -> int:
    '''search cell with the highest chance of containing the target first. returns the number of searches'''
    searches = 0
    while True: #continue until target is found
        searches += 1 #one search per turn
        cell = board.bestContains()
        if board.explore(cell) == FOUND:
            break
        if moving_target:
            board.target_movement(update_cleared=False)
        #otherwise, update probability of searched cell
        board.update_probability(cell)
    return searches

def rule2(board: Board, moving_target=False) -> int:
    '''search cell with the highest chance of finding the target first (cells with lower false positive rates). returns the number of searches'''
    searches = 0
    while True: #continue until target is found
        searches += 1 #one search per turn
        cell = board.bestFind()
        if board.explore(cell) == FOUND:
            break
        if moving_target:
            board.target_movement(update_cleared=False)
        #otherwise, update probability of searched cell
        board.update_probability(cell)
    return searches

def basicAgent1(board: Board, moving_target=False) -> int:
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
        if moving_target:
            board.target_movement(update_cleared=False)
        curcell = best_cell
    return actions

def basicAgent2(board: Board, moving_target=False) -> int:
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
        if moving_target:
            board.target_movement(update_cleared=False)
        curcell = best_cell
    return actions

def basicAgent3(board: Board) -> int:
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

def basicAgent4(board: Board, moving_target=False) -> int:
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
        if moving_target:
            board.target_movement(update_cleared=False)
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

def improvedAgent2(board: Board):
    '''A modified version of agent 3 that utilizes a weighted distance heuristic'''
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
        best_cell = board.bestWeightedDist(curcell)
        actions += board.manhattan(curcell, best_cell) #Add the actions of moving to the new location
        curcell = best_cell
    return actions

def improvedAgent3(board: Board):
    '''A modified version of agent 3 that utilizes a weighted distance heuristic'''
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
        best_cell = board.bestWeightedDist2(curcell)
        actions += board.manhattan(curcell, best_cell) #Add the actions of moving to the new location
        curcell = best_cell
    return actions

def improvedAgent4(board: Board, moving_target=False) -> int:
    '''A modified version of agent 3 that searches each cell multiple times in a row'''
    actions = 0
    best_cell = (-1,-1)
    curcell = board.bestFind() #Start on best cell
    while True: #continue until target is found
        #Explore the cell
        tries = 2
        #tries = board._board[curcell[0]][curcell[1]] + 2
        for i in range(tries):
            actions += 1 #Exploring the cell is an action
            if board.explore(curcell) == FOUND:
                return actions
            #Update probabilities
            board.update_probability(curcell)
        #Find the next smallest
        best_cell = board.bestDistNumpy(curcell)
        actions += board.manhattan(curcell, best_cell) #Add the actions of moving to the new location
        if moving_target:
            board.target_movement(update_cleared=False)
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
            cell = board.bestContainsMoving()
        found_target, target_nearby = board.exploreMove(cell) #explore current cell
        board.target_movement() #Target walks
        if found_target: #found target, stop
            break
        #otherwise, update probability of searched cell
        board.update_probability(cell)
    return searches

def moveCloseAgent(board: Board):
    '''agent for a board with a moving target. Can only move to neighbors of the current cell each turn. Use basicAgent3 strategy to find spaces until we get close to target, then use local search. Returns number of actions taken.'''
    target_nearby = False
    actions = 0
    curcell = board.bestFind()
    best_cell = curcell
    while True: #continue until target is found
        actions += 1 #take 1 action per turn
        found_target, target_nearby = board.exploreMove(curcell) #explore current cell
        board.target_movement() #Target walks
        if found_target: #found target, stop
            break
        #otherwise, update probability of searched cell
        board.update_probability(curcell)
        if target_nearby:
            best_cell = board.bestLocal(curcell,5)
        elif best_cell == curcell: #Find new cell to travel to
            best_cell = board.bestDistMoving(curcell)
        curcell = board.moveTowards(curcell, best_cell) #Walk towards
        actions += 1 #Walking action
        # num_walk_actions = board.manhattan(curcell, best_cell)
        # actions += num_walk_actions #Add the actions of moving to the new location
        # for _ in range(num_walk_actions): #Allow the target to walk for each action we take
        #     board.target_movement()
    return actions

def moveCloseAgent2(board: Board):
    '''agent for a board with a moving target. Can only move to neighbors of the current cell each turn. Use basicAgent3 strategy to find spaces until we get close to target, then use local search. Returns number of actions taken.'''
    target_nearby = False
    actions = 0
    curcell = board.bestFind()
    best_cell = curcell
    while True: #continue until target is found
        actions += 1 #take 1 action per turn
        if best_cell == curcell:
            found_target, target_nearby = board.exploreMove(curcell) #explore current cell
        board.target_movement() #Target walks
        if found_target: #found target, stop
            break
        #otherwise, update probability of searched cell
        if best_cell == curcell:
            board.update_probability(curcell)
            if target_nearby:
                best_cell = board.bestLocal(curcell,5)
            elif best_cell == curcell: #Find new cell to travel to
                best_cell = board.bestDistMoving(curcell)
        curcell = board.moveTowards(curcell, best_cell) #Walk towards
        actions += 1 #Walking action
        # num_walk_actions = board.manhattan(curcell, best_cell)
        # actions += num_walk_actions #Add the actions of moving to the new location
        # for _ in range(num_walk_actions): #Allow the target to walk for each action we take
        #     board.target_movement()
    return actions

def moveCloseAgent3(board: Board):
    '''agent for a board with a moving target. Can only move to neighbors of the current cell each turn. Use basicAgent3 strategy to find spaces until we get close to target, then use local search. Returns number of actions taken.'''
    target_nearby = False
    actions = 0
    best_cell = (-1,-1)
    curcell = board.bestFind()
    while True: #continue until target is found
        actions += 1 #take 1 action per turn
        found_target, target_nearby = board.exploreMove(curcell) #explore current cell
        board.target_movement() #Target walks
        if found_target: #found target, stop
            break
        #otherwise, update probability of searched cell
        board.update_probability(curcell)
        if target_nearby:
            best_cell = board.bestLocal(curcell,5)
        else:
            best_cell = board.bestDistMoving(curcell)
        num_walk_actions = board.manhattan(curcell, best_cell)
        actions += num_walk_actions #Add the actions of moving to the new location
        for _ in range(num_walk_actions): #Allow the target to walk for each action we take
            board.target_movement()
        curcell = best_cell
    return actions

def moveRule1(board: Board) -> int:
    '''Search cell with highest chance of containing the target on board with a moving target'''
    searches = 0
    target_nearby = False
    cell = board.bestContainsMoving()
    while True: #continue until target is found
        searches += 1 #one search per turn
        if target_nearby:
            board.isNearby(cell)
        cell = board.bestContainsMoving()
        found_target, target_nearby = board.exploreMove(cell)
        if found_target:
            break
        board.target_movement(update_cleared=False) #Target walks
        #otherwise, update probability of searched cell
        board.update_probability(cell)
    return searches

def moveRule2(board: Board) -> int:
    '''Search cell with highest chance of finding the target on board with a moving target'''
    searches = 0
    target_nearby = False
    cell = board.bestFindMoving()
    while True: #continue until target is found
        searches += 1 #one search per turn
        if target_nearby:
            board.isNearby(cell)
        cell = board.bestFindMoving()
        found_target, target_nearby = board.exploreMove(cell)
        if found_target:
            break
        board.target_movement(update_cleared=False) #Target walks
        #otherwise, update probability of searched cell
        board.update_probability(cell)
    return searches

def moveAgent1(board: Board) -> int:
    '''Agent 1 that utilizes additional information'''
    target_nearby = False
    actions = 0
    curcell = board.bestContainsMoving()
    best_cell = curcell
    while True: #continue until target is found
        actions += 1 #take 1 action per turn
        found_target, target_nearby = board.exploreMove(curcell) #explore current cell
        # print(len(np.argwhere(board._known_cleared == 0)))
        if found_target: #found target, stop
            break
        if board._known_cleared[board.target[0]][board.target[1]] != 0:
            if board._known_cleared[board.target[0]][board.target[1]] != 1:
                print("BIGGG ERROR")
            print("ERROR")
            print(board.target)
            print(board._known_cleared)
        board.target_movement() #Target walks
        #otherwise, update probability of searched cell
        board.update_probability(curcell)
        if target_nearby:
            board.isNearby(curcell)
        best_cell = board.bestContainsMoving()
        actions += board.manhattan(curcell, best_cell) #Walking action
        curcell = best_cell
    return actions

def moveAgent2(board: Board) -> int:
    '''Agent 2 that utilizes additional information'''
    target_nearby = False
    actions = 0
    curcell = board.bestFindMoving()
    best_cell = curcell
    while True: #continue until target is found
        actions += 1 #take 1 action per turn
        found_target, target_nearby = board.exploreMove(curcell) #explore current cell
        if found_target: #found target, stop
            break
        if board._known_cleared[board.target[0]][board.target[1]] != 0:
            if board._known_cleared[board.target[0]][board.target[1]] != 1:
                print("BIGGG ERROR")
            print("ERROR")
            print(board.target)
            print(board._known_cleared)
        board.target_movement() #Target walks
        #otherwise, update probability of searched cell
        board.update_probability(curcell)
        if target_nearby:
            board.isNearby(curcell)
        best_cell = board.bestFindMoving()
        actions += board.manhattan(curcell, best_cell) #Walking action
        curcell = best_cell
    return actions

def moveAgent3(board: Board) -> int:
    '''Agent 3 that utilizes additional information'''
    target_nearby = False
    actions = 0
    curcell = board.bestFindMoving() #Use for initial cell
    best_cell = curcell
    while True: #continue until target is found
        actions += 1 #take 1 action per turn
        found_target, target_nearby = board.exploreMove(curcell) #explore current cell
        if found_target: #found target, stop
            break
        if board._known_cleared[board.target[0]][board.target[1]] != 0:
            if board._known_cleared[board.target[0]][board.target[1]] != 1:
                print("BIGGG ERROR")
            print("ERROR")
            print(board.target)
            print(board._known_cleared)
        board.target_movement() #Target walks
        #otherwise, update probability of searched cell
        board.update_probability(curcell)
        if target_nearby:
            board.isNearby(curcell)
        best_cell = board.bestDistMoving(curcell)
        actions += board.manhattan(curcell, best_cell) #Walking action
        curcell = best_cell
    return actions

def moveAgent4(board: Board) -> int:
    '''Improved agent that utilizes additional information'''
    target_nearby = False
    actions = 0
    curcell = board.bestFindMoving() #Use for initial cell
    best_cell = curcell
    found = False
    while True: #continue until target is found
        tries = 2
        for _ in range(tries):
            actions += 1 #take 1 action per turn
            found_target, target_nearby = board.exploreMove(curcell) #explore current cell
            if found_target: #found target, stop
                found = True
                break
            if board._known_cleared[board.target[0]][board.target[1]] != 0:
                if board._known_cleared[board.target[0]][board.target[1]] != 1:
                    print("BIGGG ERROR")
                print("ERROR")
                print(board.target)
                print(board._known_cleared)
            board.target_movement() #Target walks
            #otherwise, update probability of searched cell
            board.update_probability(curcell)
        if found:
            break
        if target_nearby:
            board.isNearby(curcell)
        best_cell = board.bestDistMoving(curcell)
        actions += board.manhattan(curcell, best_cell) #Walking action
        curcell = best_cell
    return actions

def moveAgent5(board: Board) -> int:
    '''Pick a random cell that is valid'''
    target_nearby = False
    actions = 0
    valid = np.argwhere(board._known_cleared == 0)
    curcell = tuple(valid[int(np.random.choice(len(valid), 1)[0])])
    best_cell = curcell
    while True: #continue until target is found
        actions += 1 #take 1 action per turn
        found_target, target_nearby = board.exploreMove(curcell) #explore current cell
        if found_target: #found target, stop
            break
        board.target_movement() #Target walks
        #otherwise, update probability of searched cell
        board.update_probability(curcell)
        if target_nearby:
            board.isNearby(curcell)
        valid = np.argwhere(board._known_cleared == 0)
        best_cell = tuple(valid[int(np.random.choice(len(valid), 1)[0])])
        actions += board.manhattan(curcell, best_cell) #Walking action
        curcell = best_cell
    return actions
