import copy
import queue
import sys
import re
sys.setrecursionlimit(5000)

#Class that represents the state of the problem
class State:

    def __init__(self,n):
        #A table that contains all the block that sit directly on the table
        self.table = [0] * n
        #A table that dictates if a block has aonother block sitting on it
        #E.x If B sits on A: on[0] = 1 given that A->0, B->1, C->2 etc
        self.on = [None] * n
        self.parent = None

    def CreateChildren(currState,nodeList,n):
        #1st iter -> A Block (x=0)
        #2nd iter -> B Block (x=1)
        #3rd iter -> C Block (x=2)
        for x in range(0,n):
            #print(x)
            #If currState.on[x] != None then the block cant move
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
                                nodeList[-1].parent = currState
                                if currState.table[x] == 1:
                                    nodeList[-1].table[x] = 0
                                else:
                                    for j in range(0,n):
                                        if currState.on[j] == x:
                                            nodeList[-1].on[j] = None
                                nodeList[-1].on[i] = x
                                #print(nodeList[-1].table)
                                #print(nodeList[-1].on)
                                #print("\n")
                    elif i == n:
                        if currState.table[x] == 0:
                            nodeList.append(State(n))
                            nodeList[-1] = copy.deepcopy(currState)
                            nodeList[-1].parent = currState
                            nodeList[-1].table[x] = 1
                            for j in range(0,n):
                                if nodeList[-1].on[j] == x:
                                    nodeList[-1].on[j] = None
                            #print(nodeList[-1].table)
                            #print(nodeList[-1].on)
                            #print("\n")

    def BreadthFirstSearch(currState,n,nodeList,nodeStack,goalState):
        foundSolution = False
        q = queue.Queue()
        q.put(currState)
        print(nodeList)
        while foundSolution == False:
            currState = q.get()
            if currState.table == goalState.table and currState.on == goalState.on:
                foundSolution = True
                print("Solution")
                print(currState.table)
                print(currState.on)
            else:
                State.CreateChildren(currState,nodeList,n)
                print(len(nodeList))
                #print(nodeList)
                for x in nodeList:
                    q.put(x)
                nodeList.clear()
                #print(len(nodeList))
                #print(nodeList)
        return currState


    def TreeTraverse(currState,n,nodeList,nodeStack,goalState):
        treeDepth = 0
        #Each block can be at the right place with max 2 moves
        maxDepth = 2*n
        foundSolution = False
        numOfChildren = []

        while foundSolution == False:
            if treeDepth < maxDepth:
                print("1")
                State.CreateChildren(currState,nodeList,n)
                #print(nodeList)
                numOfChildren.append(len(nodeList)-1)


                for x in range(0,len(nodeList)):
                    nodeStack.append(nodeList.pop())

                #print("\n")
                #print(nodeStack)
                treeDepth = treeDepth + 1
                currState = nodeStack.pop()
                if currState.table == goalState.table and currState.on == goalState.on:
                    foundSolution = True
                    print("Solution")
            elif numOfChildren[-1] > 0:
                print("2")
                currState = nodeStack.pop()
                numOfChildren[-1] = numOfChildren[-1] - 1
                if currState.table == goalState.table and currState.on == goalState.on:
                    foundSolution = True
                    print("Solution")
                    print(currState.table)
                    print(currState.on)
            else:
                print("3")
                numOfChildren.pop()
                treeDepth = treeDepth - 1
                if len(nodeStack) > 0:
                    currState = nodeStack.pop()

        return currState

    #This function helps find the path from the root to the solution.
    def FindMoves(currState):
        parentStack = []
        parentStack.append(currState)
        while currState.parent != None:
            parentStack.append(currState.parent)
            currState = parentStack[-1]

        return parentStack

    def PrintMoves(currState,parentStack,n):
        parentList = []
        #Num of checks value. E.x If there are n states, there are n-1 moves
        #print("-"*50)
        while len(parentStack) != 0:
            tmp = parentStack.pop()
            #print(tmp.table)
            #print(tmp.on)
            parentList.append(tmp)
        #print("-"*50)
        print("-"*50)
        for x in range(0,len(parentList)):
            print(parentList[x].table)
            print(parentList[x].on)
        print("-"*50)
        numOfChecks = len(parentList) - 1
        for x in range(0,numOfChecks):
            for y in range(0,n):
                #Case when a block moves to the table from the top of another block
                if parentList[x].table[y] == 0 and parentList[x+1].table[y] == 1:
                    destination = "table"
                    who = y
                    for j in range(0,n):
                        if parentList[x].on[j] != parentList[x+1].on[j]:
                            source = j
                            print("Move(" + str(who) + "," + str(source) + "," + str(destination) + ")")
                #Case when a block moves from the table to the top of another block
                elif parentList[x].table[y] == 1 and parentList[x+1].table[y] == 0:
                    source = "table"
                    who = y
                    for j in range(0,n):
                        if parentList[x].on[j] != parentList[x+1].on[j]:
                            destination = j
                            print("Move(" + str(who) + "," + str(source) + "," + str(destination) + ")")
                #Case when a block moves from the top of a block to the top
                #of another block
                else:
                    if parentList[x].on[y] == None and parentList[x+1].on[y] != None:
                        destination = y
                        who = parentList[x+1].on[y]
                        for j in range(0,n):
                            if parentList[x].on[j] != None and parentList[x+1].on[j] == None:
                                source = j
                                print("Move(" + str(who) + "," + str(source) + "," + str(destination) + ")")

def Parser():

    inputObj = open(sys.argv[2],"r")
    input = inputObj.readlines()
    #print(input)

    #Storing n
    blockNames = re.findall("[A-Z]",input[2])
    n = len(blockNames)

    startState = State(n)
    goalState = State(n)

    #Storing INIT
    x = 3
    initLen = 3
    while re.search("goal",input[x]) == None:
        x = x + 1
        initLen = initLen + 1

    init = []
    tmpinit = []
    for x in range(3,initLen):
        tmpinit.append(re.findall("[(][A-Z\s]*[)]",input[x]))
    for x in tmpinit:
        for y in x:
            init.append(y)

    #Storing GOAL state
    goal = []
    tmpgoal = []
    for x in range(initLen,len(input)):
        tmpgoal.append(re.findall("[(][A-Z\s]*[)]",input[x]))
    for x in tmpgoal:
        for y in x:
            goal.append(y)
    print(goal)

    #Stripping ()
    for x in range(len(init)):
        init[x] = init[x].strip("()")
    for x in range(len(goal)):
        goal[x] = goal[x].strip("()")

    #Removing HANDEMPTY
    init.remove("HANDEMPTY")

    #Initializing the starting state
    for x in init:
        tmp = x.split()
        #print(tmp)
        if tmp[0] == "CLEAR":
            startState.on[blockNames.index(tmp[1])] = None
        elif tmp[0] == "ONTABLE":
            startState.table[blockNames.index(tmp[1])] = 1
        elif tmp[0] == "ON":
            startState.on[blockNames.index(tmp[2])] = blockNames.index(tmp[1])

    #Initializing the goal state
    for x in goal:
        tmp = x.split()
        #print(tmp)
        if tmp[0] == "CLEAR":
            goalState.on[blockNames.index(tmp[1])] = None
        elif tmp[0] == "ONTABLE":
            goalState.table[blockNames.index(tmp[1])] = 1
        elif tmp[0] == "ON":
            goalState.on[blockNames.index(tmp[2])] = blockNames.index(tmp[1])

    onTableBlock = []
    for x in range(n):
        onTableBlock.append(x)
    onTableBlock.append(None)
    print(onTableBlock)
    for x in goalState.on:
        del onTableBlock[onTableBlock.index(x)]

    print(onTableBlock)
    goalState.table[onTableBlock[0]] = 1

    return startState, goalState, n

def main():
    n = 3
    nodeList = []
    nodeStack = []
    kStack = []

    startState = State(n)
    goalState = State(n)
    currState = State(n)

    #Creating the starting state
    # startState.table[1] = 1
    # startState.table[2] = 1
    # startState.on[1] = 0
    startState.table[0] = 1
    startState.table[2] = 1
    startState.on[0] = 1
    print("\nInit...")
    print(startState.table)
    print(startState.on)

    #Creating the goal state
    # goalState.table[2] = 1
    # goalState.on[2] = 0
    # goalState.on[0] = 1
    goalState.table[2] = 1
    goalState.table[1] = 1
    goalState.on[2] = 0
    print("\nGoal...")
    print(goalState.table)
    print(goalState.on)

    startState, goalState, n = Parser()
    print("\nInit...")
    print(startState.table)
    print(startState.on)
    print("\nGoal...")
    print(goalState.table)
    print(goalState.on)

    #Initializing the current state
    currState = startState

    print("In Depth First Search")

    # currState = State.TreeTraverse(startState,n,nodeList,nodeStack,goalState)
    # parentStack = State.FindMoves(currState)
    # print("\n")
    #
    # State.PrintMoves(currState,parentStack,n)

    print("\n\nBreadth First Search:")
    currState = startState
    currState = State.BreadthFirstSearch(startState,n,nodeList,nodeStack,goalState)
    parentStack = State.FindMoves(currState)
    print("\n")
    State.PrintMoves(currState,parentStack,n)

    print("\n")
    startState, goalState, n = Parser()
    print(startState.table)
    print(startState.on)
    print("\nGoal...")
    print(goalState.table)
    print(goalState.on)


if __name__ == '__main__':
    main()
