#Class that represents the state of the problem
class State:

    def __init__(self,n):
        #A table that contains all the block that sit directly on the table
        self.table = []
        #A table that dictates if a block has aonother block sitting on it
        #E.x If B sits on A: on[0] = 1 given that A->0, B->1, C->2 etc
        self.on = [None] * n

def main():
    n = 3

    startState = State(n)
    goalState = State(n)
    currState = State(n)

    #Creating the starting state
    startState.table.append(1)
    startState.table.append(2)
    startState.on[1] = 0
    print("\nInit...")
    print(startState.table)
    print(startState.on)

    #Creating the goal state
    goalState.table.append(2)
    goalState.on[2] = 0
    goalState.on[0] = 1
    print("\nGoal...")
    print(goalState.table)
    print(goalState.on)

    #Initializing the current state
    currState = startState
    print("\nCurrent...")
    print(currState.table)
    print(currState.on)

if __name__ == '__main__':
    main()
