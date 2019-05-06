import copy
import queue
import sys
import re
import time
sys.setrecursionlimit(50000)

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

                    elif i == n:
                        if currState.table[x] == 0:
                            nodeList.append(State(n))
                            nodeList[-1] = copy.deepcopy(currState)
                            nodeList[-1].parent = currState
                            nodeList[-1].table[x] = 1
                            for j in range(0,n):
                                if nodeList[-1].on[j] == x:
                                    nodeList[-1].on[j] = None

    def BreadthFirstSearch(currState,n,nodeList,nodeStack,goalState):
        foundSolution = False
        q = queue.Queue()
        q.put(currState)
        #print(nodeList)
        while foundSolution == False:
            currState = q.get()
            if currState.table == goalState.table and currState.on == goalState.on:
                foundSolution = True
                print("Solution")
                print(currState.table)
                print(currState.on)
            else:
                State.CreateChildren(currState,nodeList,n)
                #print(len(nodeList))
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

        while foundSolution == False:
            if treeDepth < maxDepth:
                if treeDepth < 2*n-1:
                    State.CreateChildren(currState,nodeList,n)

                tmpstack = []
                for x in range(len(nodeList)-1,-1,-1):
                    tmpstack.append(nodeList[x])

                nodeStack.append(copy.deepcopy(tmpstack))

                nodeList.clear()
                tmpstack.clear()

                treeDepth = treeDepth + 1

                currStack = nodeStack[-1]
                while len(currStack) == 0:
                    nodeStack.pop()
                    currStack = nodeStack[-1]
                    treeDepth = treeDepth - 1

                currState = currStack.pop()

                if currState.table == goalState.table and currState.on == goalState.on:
                    foundSolution = True
                    print("Solution")
                    print(currState.table)
                    print(currState.on)

        return currState

    #This function helps find the path from the root to the solution.
    def FindMoves(currState):
        parentStack = []
        parentStack.append(currState)
        while currState.parent != None:
            parentStack.append(currState.parent)
            currState = parentStack[-1]

        return parentStack

    def PrintMoves(currState,parentStack,n,blockNames):
        parentList = []
        #Num of checks value. E.x If there are n states, there are n-1 moves
        #print("-"*50)
        while len(parentStack) != 0:
            tmp = parentStack.pop()
            #print(tmp.table)
            #print(tmp.on)
            parentList.append(tmp)
        #print("-"*50)
        # print("-"*50)
        # for x in range(0,len(parentList)):
        #     print(parentList[x].table)
        #     print(parentList[x].on)
        # print("-"*50)
        numOfChecks = len(parentList) - 1
        for x in range(0,numOfChecks):
            for y in range(0,n):
                #Case when a block moves to the table from the top of another block
                if parentList[x].table[y] == 0 and parentList[x+1].table[y] == 1:
                    destination = "table"
                    who = blockNames[y]
                    for j in range(0,n):
                        if parentList[x].on[j] != parentList[x+1].on[j]:
                            source = blockNames[j]
                            print("Move(" + str(who) + "," + str(source) + "," + str(destination) + ")")
                            #return y
                #Case when a block moves from the table to the top of another block
                elif parentList[x].table[y] == 1 and parentList[x+1].table[y] == 0:
                    source = "table"
                    who = blockNames[y]
                    for j in range(0,n):
                        if parentList[x].on[j] != parentList[x+1].on[j]:
                            destination = blockNames[j]
                            print("Move(" + str(who) + "," + str(source) + "," + str(destination) + ")")
                            #return y
                #Case when a block moves from the top of a block to the top
                #of another block
                else:
                    if parentList[x].on[y] == None and parentList[x+1].on[y] != None:
                        destination = blockNames[y]
                        who = blockNames[parentList[x+1].on[y]]
                        for j in range(0,n):
                            if parentList[x].on[j] != None and parentList[x+1].on[j] == None:
                                source = blockNames[j]
                                print("Move(" + str(who) + "," + str(source) + "," + str(destination) + ")")
                                #return parentList[x+1].on[y]

def Parser():

    inputObj = open(sys.argv[2],"r")
    input = inputObj.readlines()
    #print(input)

    x = 2
    nameLen = 2
    while re.search("init|INIT",input[x]) == None:
        x = x + 1
        nameLen = nameLen + 1

    blockNames = []
    blockNamesinit = []
    for x in range(2,nameLen):
        blockNamesinit.append(re.findall("[A-Z][0-9]*",input[x]))
    for x in blockNamesinit:
        for y in x:
            blockNames.append(y)

    #blockNames = re.findall("[A-Z][0-9]*",input[2])
    n = len(blockNames)

    #Storing n
    # blockNames = re.findall("[A-Z][0-9]*",input[2])
    # n = len(blockNames)
    # print(blockNames)
    # print(len(blockNames))

    startState = State(n)
    goalState = State(n)

    #Storing INIT
    x = 3
    initLen = 3
    while re.search("goal|GOAL",input[x]) == None:
        x = x + 1
        initLen = initLen + 1

    init = []
    tmpinit = []
    for x in range(3,initLen):
        tmpinit.append(re.findall("[(][A-Z0-9\s]*[)]",input[x]))
    for x in tmpinit:
        for y in x:
            init.append(y)
    #print(init)
    #Storing GOAL state
    goal = []
    tmpgoal = []
    for x in range(initLen,len(input)):
        tmpgoal.append(re.findall("[(][A-Z0-9\s]*[)]",input[x]))
    for x in tmpgoal:
        for y in x:
            goal.append(y)
    #print(goal)

    #Stripping ()
    for x in range(len(init)):
        init[x] = init[x].strip("()")
    for x in range(len(goal)):
        goal[x] = goal[x].strip("()")

    #Removing HANDEMPTY
    init.remove("HANDEMPTY")

    # print(init)
    # print(goal)
    # print("\n\n")
    #Initializing the starting state
    for x in init:
        tmp = x.split()
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
    #print(onTableBlock)
    for x in goalState.on:
        del onTableBlock[onTableBlock.index(x)]

    #print(onTableBlock)
    goalState.table[onTableBlock[0]] = 1

    return startState, goalState, n , blockNames

def PrintStartGoalState(startState,goalState,blockNames,n):

    sState = copy.deepcopy(startState)
    gState = copy.deepcopy(goalState)

    for x in range(n):
        if sState.on[x] != None:
            sState.on[x] = blockNames[int(sState.on[x])]
        if gState.on[x] != None:
            gState.on[x] = blockNames[int(gState.on[x])]


    print("\nInit...")
    print(sState.table)
    print(sState.on)
    print("\nGoal...")
    print(gState.table)
    print(gState.on)

def CalcBestFirstNodeCosts(n,children,goalState):
    score = []
    inOrderChildren = []

    #Calculating the score for each node
    for x in children:
        score.append(0)
        for i in range(n):
            if x.table[i] != goalState.table[i]:
                score[-1] = score[-1] + 1
            if x.on[i] != goalState.on[i]:
                score[-1] = score[-1] + 1

    #Creating the sorted(according to score) Children list
    for x in range(len(children)):
        minChild = min(score)
        pos = score.index(minChild)

        #Setting the score of the max equal to "infinite"
        score[pos] = 1000000
        inOrderChildren.append(children[pos])

    return inOrderChildren

def BestFirstSearch(startState,goalState,n):
    #Best First Search
    currState = copy.deepcopy(startState)
    nodeList = []
    closedNodes = []
    tempList = []

    while currState.table != goalState.table and currState.on != goalState.on:
        State.CreateChildren(currState,nodeList,n)
        tempList = CalcBestFirstNodeCosts(n,nodeList,goalState)

        for x in tempList:
            closedNodes.append(x)

        currState = closedNodes.pop(0)
        nodeList.clear()


    print("Solution:")
    print(currState.table)
    print(currState.on)

    return currState

def MoveReturn(currState,parentStack,n,blockNames):
    parentList = []
    #Num of checks value. E.x If there are n states, there are n-1 moves
    #print("-"*50)
    parentList.append(parentStack.pop(0))
    parentList.append(parentStack.pop(0))
    # while len(parentStack) != 0:
    #     tmp = parentStack.pop()
    #     #print(tmp.table)
    #     #print(tmp.on)
    #     parentList.append(tmp)
    #print("-"*50)
    # print("-"*50)
    # for x in range(0,len(parentList)):
    #     print(parentList[x].table)
    #     print(parentList[x].on)
    # print("-"*50)
    numOfChecks = len(parentList) - 1
    for x in range(0,numOfChecks):
        for y in range(0,n):
            #Case when a block moves to the table from the top of another block
            if parentList[x].table[y] == 0 and parentList[x+1].table[y] == 1:
                destination = "table"
                who = blockNames[y]
                for j in range(0,n):
                    if parentList[x].on[j] != parentList[x+1].on[j]:
                        source = blockNames[j]
                        #print("Move(" + str(who) + "," + str(source) + "," + str(destination) + ")")
                        return y
            #Case when a block moves from the table to the top of another block
            elif parentList[x].table[y] == 1 and parentList[x+1].table[y] == 0:
                source = "table"
                who = blockNames[y]
                for j in range(0,n):
                    if parentList[x].on[j] != parentList[x+1].on[j]:
                        destination = blockNames[j]
                        #print("Move(" + str(who) + "," + str(source) + "," + str(destination) + ")")
                        return y
            #Case when a block moves from the top of a block to the top
            #of another block
            else:
                if parentList[x].on[y] == None and parentList[x+1].on[y] != None:
                    destination = blockNames[y]
                    who = blockNames[parentList[x+1].on[y]]
                    for j in range(0,n):
                        if parentList[x].on[j] != None and parentList[x+1].on[j] == None:
                            source = blockNames[j]
                            #print("Move(" + str(who) + "," + str(source) + "," + str(destination) + ")")
                            return parentList[x+1].on[y]

def AStarHeuretic(n,children,goalState,towers,blockNames):
    score = []
    inOrderChildren = []
    #This flag is true if the block of the current i block of the node sits on
    #different blocks than the i block of the node of the goal state
    onFlag = False

    #Calculating the score for each node
    for x in children:
        score.append(0)
        for i in range(n):
            if (x.table[i] == 1 and goalState.table[i] == 0) or (x.table[i] == 0 and goalState.table[i] == 1):
                score[-1] = score[-1] + 1
            elif (x.table[i] == 0 and goalState.table[i] == 0):
                if x.on[x.on.index(i)] != goalState.on[x.on.index(i)]:
                    onFlag = True
                currPosCheck = x.on.index(i)
                while (x.table[currPosCheck] != 1) and (goalState.table[currPosCheck] != 1) and (onFlag == False):
                    if x.on[x.on.index(currPosCheck)] != goalState.on[x.on.index(currPosCheck)]:
                        onFlag = True
                    currPosCheck = x.on.index(currPosCheck)
                if onFlag:
                    score[-1] = score[-1] + 2
                elif (x.table[currPosCheck] != 1) or (goalState.table[currPosCheck] != 1):
                    score[-1] = score[-1] + 2
                onFlag = False

    scoreCopy = copy.deepcopy(score)

    minS = min(scoreCopy)
    who = []
    whoPriority = []

    posMoves = []
    for x in range(len(scoreCopy)):
        if scoreCopy[x] == minS:
            posMoves.append(children[x])

    for x in posMoves:
        parentStack = State.FindMoves(x)
        who.append(MoveReturn(x,parentStack,n,blockNames))


    for x in towers:
        for j in who:
            if j in who:
                whoPriority.append(x.index(j))

    maxP = whoPriority.index(max(whoPriority))

    BestMove = posMoves[maxP]

    return BestMove

def AStar(startState,goalState,n,blockNames):
    #A* search
    currState = copy.deepcopy(startState)
    nodeList = []
    tempList = []
    numOfTowers = 0
    towers = []
    tempTower = []

    for x in range(len(goalState.on)):
        if goalState.on[x] == None and goalState.table[x] == 0:
            currPos = goalState.on.index(goalState.on[x])

            while goalState.table[currPos] != 1:
                tempTower.append(goalState.on.index(goalState.on[currPos]))
                currPos = goalState.on.index(currPos)
            tempTower.append(goalState.on.index(goalState.on[currPos]))

            towers.append(copy.deepcopy(tempTower))
            tempTower.clear()


    while currState.table != goalState.table and currState.on != goalState.on:
        State.CreateChildren(currState,nodeList,n)

        currState = AStarHeuretic(n,nodeList,goalState,towers,blockNames)

        nodeList.clear()


    print("Solution:")
    print(currState.table)
    print(currState.on)

    return currState

def main():
    n = 3
    nodeList = []
    nodeStack = []
    kStack = []

    startState = State(n)
    goalState = State(n)
    currState = State(n)

    startState, goalState, n, blockNames = Parser()
    currState = startState

    # print("\nInit...")
    # print(startState.table)
    # print(startState.on)
    # print("\nGoal...")
    # print(goalState.table)
    # print(goalState.on)

    #Choosing Deapth or Breadth first Search
    if sys.argv[1] == "depth":
        #Printing Starting and goal state
        start = time.time()
        PrintStartGoalState(startState,goalState,blockNames,n)

        #In Depth First Search
        print("\n\n****In Depth First Search:****")
        currState = State.TreeTraverse(startState,n,nodeList,nodeStack,goalState)
        parentStack = State.FindMoves(currState)
        print("\n")
        State.PrintMoves(currState,parentStack,n,blockNames)
        end = time.time()
        print("\nExecuted in: " + str(end - start))
    elif sys.argv[1] == "breadth":
        #Printing Starting and goal state
        start = time.time()
        PrintStartGoalState(startState,goalState,blockNames,n)

        #Breadth First Search
        print("\n\n****Breadth First Search:****")
        currState = startState
        currState = State.BreadthFirstSearch(startState,n,nodeList,nodeStack,goalState)
        parentStack = State.FindMoves(currState)
        print("\n")
        State.PrintMoves(currState,parentStack,n,blockNames)
        end = time.time()
        print("\nExecuted in: " + str(end - start))
    elif sys.argv[1] == "best":
        #Printing Starting and goal state
        start = time.time()
        PrintStartGoalState(startState,goalState,blockNames,n)

        print("\n\n****Best First Search:****")
        #Best First Search
        currState = BestFirstSearch(startState,goalState,n)
        parentStack = State.FindMoves(currState)
        print("\n")
        State.PrintMoves(currState,parentStack,n,blockNames)
        end = time.time()
        print("\nExecuted in: " + str(end - start))
    elif sys.argv[1] == "astar":
        #Printing Starting and goal state
        start = time.time()
        PrintStartGoalState(startState,goalState,blockNames,n)

        #A*
        print("\n\n***********AStar***********")
        currState = startState
        currState = AStar(startState,goalState,n,blockNames)
        parentStack = State.FindMoves(currState)
        print("\n")
        State.PrintMoves(currState,parentStack,n,blockNames)
        end = time.time()
        print("\nExecuted in: " + str(end - start))
    else:
        print("Error: Algorithms supported: breadth | depth | best | astar")



if __name__ == '__main__':
    main()
