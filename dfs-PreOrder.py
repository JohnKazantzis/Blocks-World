import copy

#Class that represents the state of the problem
class State:

    def __init__(self,n):
        #A table that contains all the block that sit directly on the table
        self.table = [0] * n
        #A table that dictates if a block has aonother block sitting on it
        #E.x If B sits on A: on[0] = 1 given that A->0, B->1, C->2 etc
        self.on = [None] * n

    def CreateChildren(currState,nodeList,n):
        #1st iter -> A Block (x=0)
        #2nd iter -> B Block (x=1)
        #3rd iter -> C Block (x=2)
        for x in range(0,3):
            print(x)
            if currState.on[x] == None:
                #The i var (except when i=n) represents the block we want to put
                #the x block on. The i=n value represents the table
                for i in range(0,n+1):
                    if i != n and i != x:
                        #Checking if the x block is already on the block
                        #we want to put it on
                        if currState.on[i] != x:
                            #Checking if anything is on the block we want to
                            #put the x block on
                            if currState.on[i] == None:
                                nodeList.append(State(n))
                                nodeList[-1] = copy.deepcopy(currState)
                                if currState.table[x] == 1:
                                    nodeList[-1].table[x] = 0
                                else:
                                    for j in range(0,3):
                                        if currState.on[j] == x:
                                            nodeList[-1].on[j] = None
                                nodeList[-1].on[i] = x
                                print(nodeList[-1].table)
                                print(nodeList[-1].on)
                                print("\n")
                    elif i == n and i != x:
                        if currState.table[x] == 0:
                            nodeList.append(State(n))
                            nodeList[-1] = copy.deepcopy(currState)
                            nodeList[-1].table[x] = 1
                            for j in range(0,3):
                                if nodeList[-1].on[j] == x:
                                    nodeList[-1].on[j] = None
                            print(nodeList[-1].table)
                            print(nodeList[-1].on)
                            print("\n")



def main():
    n = 3
    nodeList = []

    startState = State(n)
    goalState = State(n)
    currState = State(n)

    #Creating the starting state
    startState.table[1] = 1
    startState.table[2] = 1
    startState.on[1] = 0
    print("\nInit...")
    print(startState.table)
    print(startState.on)

    #Creating the goal state
    goalState.table[2] = 1
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
    print("\n")

    State.CreateChildren(currState,nodeList,n)

if __name__ == '__main__':
    main()
