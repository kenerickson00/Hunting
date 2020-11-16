'''Run the various agents

Valid Arguments:
    python3 runner.py <Board Dimension> <Count Movement> <Moving Target>
    - Maze dimension: [1, inf)
    - Count Movement: 0 (False) / 1 (True)
    - Moving Target: 0 (False) / 1 (True)

    If "Count Movement" is false, then Rule 1 and 2 will be run. If it is true, Agent 1, Agent 2, Agent 3, and the Improved Agent will be run.
    
    If Moving Target is false, then part 1 of the assignment will be executed. If it is true, part 2 will be executed.
'''
import time
import sys

from Agent import rule1, rule2, basicAgent1, basicAgent2, basicAgent3, improvedAgent, moveRule1, moveRule2, moveAgent1, moveAgent2, moveAgent3, moveImprovedAgent
from Board import Board


def runner():
    args = sys.argv[1:]
    #Check number argument validity
    if len(args) != 3:
        print("Invalid number of arguments, " + str(len(args)) + " given, need 3")
        return

    dim = int(args[0])
    count_movement = int(args[1])
    moving_target = int(args[2])

    if dim <= 0:
        raise Exception("Invalid board dimension")
    if count_movement not in (0, 1):
        raise Exception("Count Movement should be 0/1")
    if moving_target not in (0, 1):
        raise Exception("Moving Target should be 0/1")

    if moving_target == 0: #Part 1
        if count_movement == 0: #Rule 1 and Rule 2
            start = time.time()
            r1_actions = rule1(Board(dim))
            end = time.time()
            print(f"Rule 1 Actions: {r1_actions}")
            print(f"Rule 1 Time: {end-start}")
            
            start = time.time()
            r2_actions = rule2(Board(dim))
            end = time.time()
            print(f"Rule 2 Actions: {r2_actions}")
            print(f"Rule 2 Time: {end-start}")

        else: #Agent 1, Agent 2, Agent 3, and Improved Agent
            start = time.time()
            a1_actions = basicAgent1(Board(dim))
            end = time.time()
            print(f"Agent 1 Actions: {a1_actions}")
            print(f"Agent 1 Time: {end-start}")

            start = time.time()
            a2_actions = basicAgent2(Board(dim))
            end = time.time()
            print(f"Agent 2 Actions: {a2_actions}")
            print(f"Agent 2 Time: {end-start}")

            start = time.time()
            a3_actions = basicAgent3(Board(dim))
            end = time.time()
            print(f"Agent 3 Actions: {a3_actions}")
            print(f"Agent 3 Time: {end-start}")

            start = time.time()
            a4_actions = improvedAgent(Board(dim))
            end = time.time()
            print(f"Improved Agent Actions: {a4_actions}")
            print(f"Improved Agent Time: {end-start}")

    else: #Part 2
        if count_movement == 0: #Rule 1 and Rule 2
            start = time.time()
            r1_actions = rule1(Board(dim, moving_target=True), moving_target=True)
            end = time.time()
            print(f"Rule 1 Actions: {r1_actions}")
            print(f"Rule 1 Time: {end-start}")

            start = time.time()
            mr1_actions = moveRule1(Board(dim, moving_target=True))
            end = time.time()
            print(f"Modifed Rule 1 Actions: {mr1_actions}")
            print(f"Modifed Rule 1 Time: {end-start}")

            start = time.time()
            r2_actions = rule2(Board(dim, moving_target=True), moving_target=True)
            end = time.time()
            print(f"Rule 2 Actions: {r2_actions}")
            print(f"Rule 2 Time: {end-start}")

            start = time.time()
            mr2_actions = moveRule2(Board(dim, moving_target=True))
            end = time.time()
            print(f"Modifed Rule 2 Actions: {mr2_actions}")
            print(f"Modifed Rule 2 Time: {end-start}")

        else: #Agent 1, Agent 2, Agent 3, and Improved Agent
            start = time.time()
            a1_actions = basicAgent1(Board(dim, moving_target=True), moving_target=True)
            end = time.time()
            print(f"Agent 1 Actions: {a1_actions}")
            print(f"Agent 1 Time: {end-start}")

            start = time.time()
            ma1_actions = moveAgent1(Board(dim, moving_target=True))
            end = time.time()
            print(f"Modified Agent 1 Actions: {ma1_actions}")
            print(f"Modified Agent 1 Time: {end-start}")

            start = time.time()
            a2_actions = basicAgent2(Board(dim, moving_target=True), moving_target=True)
            end = time.time()
            print(f"Agent 2 Actions: {a2_actions}")
            print(f"Agent 2 Time: {end-start}")

            start = time.time()
            ma2_actions = moveAgent2(Board(dim, moving_target=True))
            end = time.time()
            print(f"Modified Agent 2 Actions: {ma2_actions}")
            print(f"Modified Agent 2 Time: {end-start}")

            start = time.time()
            a3_actions = basicAgent3(Board(dim, moving_target=True), moving_target=True)
            end = time.time()
            print(f"Agent 3 Actions: {a3_actions}")
            print(f"Agent 3 Time: {end-start}")

            start = time.time()
            ma3_actions = moveAgent3(Board(dim, moving_target=True))
            end = time.time()
            print(f"Modified Agent 3 Actions: {ma3_actions}")
            print(f"Modified Agent 3 Time: {end-start}")

            start = time.time()
            a4_actions = improvedAgent(Board(dim, moving_target=True), moving_target=True)
            end = time.time()
            print(f"Improved Agent Actions: {a4_actions}")
            print(f"Improved Agent Time: {end-start}")

            start = time.time()
            ma4_actions = moveImprovedAgent(Board(dim, moving_target=True))
            end = time.time()
            print(f"Modified Improved Agent Actions: {ma4_actions}")
            print(f"Modified Improved Agent Time: {end-start}")


if __name__ == "__main__":
    runner()
