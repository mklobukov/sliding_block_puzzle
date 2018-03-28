#!/usr/bin/env python

#Author: Mark Klobukov
#Class: CS510 (AI) @ Drexel U
#SBP with random walk, BFS, DFS, IDS
#10/19/2017

from random import *
from Queue import *
from copy import *
import time
import sys

class Node(object):
    def __init__(self, state, path, nsteps):
        self.state = state
        self.path = path
        self.nsteps = nsteps

    def __str__(self):
        return str(self.state)


def loadStateFromDisk(fileName):
    linesRead = 0
    rows = 0
    cols = 0
    state = list()

    with open(fileName) as fp:
        for line in fp:
            if len(line) == 0:
                break
            if linesRead == 0:
                dim = line.split(",")
                linesRead = linesRead+1
                rows = int(dim[1])
                cols = int(dim[0])
                state = [[None for xCoord in range(cols)] for yCoord in range(rows)]
            else:
                thisRow = line.split(",")
                for idx in range(0, len(thisRow)-1):
                    state[linesRead-1][idx] = int(thisRow[idx])
                linesRead = linesRead+1
        return state

def printState(state):
    print str(len(state[0])) + "," + str(len(state)) + ", "
    for row in state:
        for el in row:
            sys.stdout.write(str(el)+",")
            sys.stdout.flush()
        print " "



def cloneState(state):
    stateCopy = [row[:] for row in state]
    return stateCopy

def puzzleComplete(state):
    for row in state:
        for el in row:
            if el == -1:
                return False
    return True

def getPieceCoord(state, piece):
    coord = list()
    for rowIdx, row in enumerate(state):
        for colIdx, el in enumerate(row):
            if el == piece:
                coord.append([rowIdx, colIdx])
    return coord
#given state and piece, return list of al moves that can be performed
def generateMoves(state, piece):
    moves = list()
    master = False
    if (piece ==2):
        master = True
    single, vert, horiz, sq = False, False, False, False

    coord = getPieceCoord(state, piece)
    ncells = len(coord)
    if ncells == 1:
        single = True
    elif ncells == 4:
        sq=  True
    else:
        if coord[0][0] == coord[1][0]:
            horiz = True
        else:
            vert = True

    #generate moves for single:
    if single:
        i = coord[0][0]
        j = coord[0][1]
        #check up
        if(state[i-1][j] == 0 or (master and state[i-1][j] == -1)):
            moves.append([piece, "up"])
        #check down
        if(state[i+1][j] == 0 or (master and state[i+1][j] == -1)):
            moves.append([piece, "down"])
        #check right
        if(state[i][j+1] == 0 or (master and state[i][j+1] == -1)):
            moves.append([piece, "right"])
        #check left
        if(state[i][j-1] == 0 or (master and state[i][j-1] == -1)):
            moves.append([piece, "left"])
    #generate moves for horizontal
    elif horiz:
        # //can move sideways if one space to the side empty
        # //can move up/down if both spaces up/down are empty
        i = coord[0][0]
        j1 = coord[0][1]
        j2 = coord[1][1]
        #check left:
        if (state[i][j1-1] == 0 or (master and state[i][j1-1] == -1)):
            moves.append([piece, "left"])
        if (state[i][j2+1] == 0 or (master and state[i][j2+1] == -1)):
            moves.append([piece, "right"])
        #check up
        if ((state[i-1][j1] == 0 and state[i-1][j2] == 0) or
            (master and state[i-1][j1] == -1 and state[i-1][j2] == -1)):
            moves.append([piece, "up"])
        #check down
        if ((state[i+1][j1] == 0 and state[i+1][j2] == 0) or
            (master and state[i+1][j1] == -1 and state[i+1][j2] == -1)):
            moves.append([piece, "down"])

    elif vert:
        i1 = coord[0][0]
        i2 = coord[1][0]
        j = coord[0][1]

        #check up
        if(state[i1-1][j] == 0 or (master and state[i1-1][j] == -1)):
            moves.append([piece, "up"])
        #check down
        if(state[i2+1][j] == 0 or (master and state[i2+1][j] == -1)):
            moves.append([piece, "down"])
        #check right
        if((state[i1][j+1] == 0 and state[i2][j+1] == 0) or
            (master and state[i1][j+1] == -1 and state[i2][j+1] == -1)):
            moves.append([piece, "right"])
        #check left
        if((state[i1][j-1] == 0 and state[i2][j-1] == 0) or
            (master and state[i1][j-1] == -1 and state[i2][j-1] == -1)):
            moves.append([piece, "left"])

    elif sq:
        i1 = coord[0][0]
        j1 = coord[0][1]
        i2 = coord[1][0]
        j2 = coord[1][1]
        #CHECK UP
        if((state[i1-1][j1] == 0 and state[i1-1][j2] == 0) or
            (master and state[i1-1][j1] == -1 and state[i1-1][j2] == -1 )):
            moves.append([piece, "up"])
        #check down
        if ((state[i2+1][j1] == 0 and state[i2+1][j2] == 0) or
            (master and state[i2+1][j1] == -1 and state[i2+1][j2] == -1)):
            moves.append([piece, "down"])
        #check right
        if ((state[i1][j2+1] == 0 and state[i2][j2+1] == 0) or
            (master and state[i1][j2+1] == -1 and state[i2][j2+1] == -1)):
            moves.append([piece, "right"])
        #check left
        if ((state[i1][j1-1] == 0 and state[i2][j1-1] == 0) or
            (master and state[i1][j1-1] == -1 and state[i2][j1-1] == -1)):
            moves.append([piece, "left"])
    else:
        print "Couldn't identify the shape of piece. Smth went wrong"

    return moves

def generateAllMoves(state):
    allMoves = list()
    donePieces = list()
    for row in state:
        for el in row:
            if el == 1 or el == -1 or el == 0:
                continue
            if not (el in donePieces):
                thisMoves = generateMoves(state, el)
                for move in thisMoves:
                    allMoves.append(move)
                donePieces.append(el)
    return allMoves

def applyMove(state, move):
    coords = getPieceCoord(state, move[0])
    ncells = len(coords)
    d = move[1]
    #apply up
    if d == "up":
        for coord in coords:
            if(state[coord[0]-1][coord[1]] == -1):
                state[coord[0]-1][coord[1]] = 0
            swapValues(state, coord,
                        [coord[0]-1, coord[1]])
    elif d == "down":
        for i in range(len(coords)-1, -1, -1):
            coord = coords[i]
            if(state[coord[0]+1][coord[1]] == -1):
                state[coord[0]+1][coord[1]] = 0
            swapValues(state,coord,
                        [coord[0]+1,coord[1]])
    elif d == "left":
        for coord in coords:
            if(state[coord[0]][coord[1]-1] == -1):
                state[coord[0]][coord[1]-1] = 0
            swapValues(state, coord,
                        [coord[0],coord[1]-1])
    elif d == "right":
        for i in range(len(coords)-1, -1, -1):
            coord = coords[i]
            if(state[coord[0]][coord[1]+1] == -1):
                state[coord[0]][coord[1]+1] = 0
            swapValues(state,coord,
                        [coord[0],coord[1]+1])

def swapValues(state, coord1, coord2):
    temp = state[coord1[0]][coord1[1]]
    state[coord1[0]][coord1[1]] = state[coord2[0]][coord2[1]]
    state[coord2[0]][coord2[1]] = temp

def applyMoveCloning(state, move):
    newState = cloneState(state)
    applyMove(newState, move)
    return newState

def statesIdentical(state1, state2):
    rows = len(state1)
    cols = len(state1[0])
    for i in range(0, rows):
        for j in range(0, cols):
            if state1[i][j] != state2[i][j]:
                return False
    return True

def normalizeState(state):
    rows = len(state)
    cols = len(state[0])
    nextIdx = 3
    for i in range(0, rows):
        for j in range(0, cols):
            if(state[i][j] == nextIdx):
                nextIdx = nextIdx + 1
            elif (state[i][j] > nextIdx):
                swapIdx(state, nextIdx, state[i][j])
                nextIdx = nextIdx + 1

def swapIdx(state, idx1, idx2):
    rows = len(state)
    cols = len(state[0])

    for i in range(0, rows):
        for j in range(0, cols):
            if (state[i][j] == idx1):
                state[i][j] = idx2
            elif (state[i][j] == idx2):
                state[i][j] = idx1

def randomWalk(state, limit):
    totalMoves = 0
    puzzleNotSolved = True

    while(puzzleNotSolved and totalMoves < limit):
        printState(state)
        # sys.stdout.write("\n ")
        # sys.stdout.flush()
        print " "
        allMoves = generateAllMoves(state)
        moveIdx = randint(0, len(allMoves)-1)
        applyMove(state, allMoves[moveIdx])
        normalizeState(state)
        totalMoves = totalMoves + 1
        printMove(allMoves[moveIdx])
        print " "
        if puzzleComplete(state):
            puzzleNotSolved = False
    printState(state)
    print " "

def printMove(move):
    print "("+str(move[0]) + "," + str(move[1]) + ") "

def BFS(state):
    start = time.clock()
    nodesExplored = 1
    q = Queue()
    #queue will consist of nodes
    rootNode = Node(state, list(), 0)
    q.put(rootNode)
    visitedStates = list()
    stateCpy = cloneState(state)
    normalizeState(stateCpy)
    visitedStates.append(stateCpy)
    depth = 1
    while (not q.empty()):
        for i in range(0, q.qsize()):
            node = q.get()
            if puzzleComplete(node.state):
                end = time.clock()
                totalTime = end-start
                return [node, nodesExplored, totalTime]
            allMoves = generateAllMoves(node.state)
            for move in allMoves:
                newState = applyMoveCloning(node.state, move)
                newStateNorm = cloneState(newState)
                normalizeState(newStateNorm)
                if newStateNorm not in visitedStates:
                    path = node.path + [[move[0], move[1]]]
                    childNode = Node(newState, path, len(path))
                    q.put(childNode)
                    visitedStates.append(newStateNorm)
                    nodesExplored = nodesExplored+1
        depth = depth +1

def DFS(state):
    start = time.clock()
    nodesExplored = 1
    s = list() #stack
    rootNode = Node(state, list(), 0)
    s.append(rootNode)
    visitedStates = list()
    rootStateNorm = cloneState(state)
    normalizeState(rootStateNorm)
    visitedStates.append(rootStateNorm)

    while (len(s) != 0):
        node = s.pop()
        if puzzleComplete(node.state):
            end = time.clock()
            totalTime = end - start
            return [node, nodesExplored, totalTime]
        allMoves = generateAllMoves(node.state)
        for idx, move in enumerate(allMoves):
            newState = applyMoveCloning(node.state, move)
            newStateNorm = cloneState(newState)
            normalizeState(newStateNorm)
            if (newStateNorm not in visitedStates):
                path = node.path + [[move[0], move[1]]]
                childNode = Node(newState, path, len(path))
                s.append(childNode)
                visitedStates.append(newStateNorm)
                nodesExplored = nodesExplored + 1

def IDS(state, maxDepth):
    limit = 1
    while (limit < maxDepth):
        start = time.clock()
        depth = 0
        while (depth <= limit):
            nodesExplored = 1
            #start from the beginning but go one level deeper
            s = list() #stack
            rootNode = Node(state, list(), 0)
            s.append(rootNode)
            visitedStates = list()
            rootStateNorm = cloneState(state)
            normalizeState(rootStateNorm)
            visitedStates.append(rootStateNorm)
            while(len(s) != 0):
                node = s.pop()
                if node.nsteps > limit:
                    continue
                if puzzleComplete(node.state):
                    end = time.clock()
                    totalTime = end-start
                    return [node, nodesExplored, totalTime]
                allMoves = generateAllMoves(node.state)
                for idx, move in enumerate(allMoves):
                    newState = applyMoveCloning(node.state, move)
                    newStateNorm = cloneState(newState)
                    normalizeState(newStateNorm)
                    if (newStateNorm not in visitedStates):
                        path = node.path + [[move[0], move[1]]]
                        childNode = Node(newState, path, len(path))
                        s.append(childNode)
                        visitedStates.append(newStateNorm)
                        nodesExplored = nodesExplored + 1
            depth = depth +1
        limit = limit + 1



def main():
    stateFileName = "SBP-level0.txt"
    state = loadStateFromDisk(stateFileName)

    print "********Random Walk********"
    N = 3
    randomWalk(state, N)


    print "********BFS********"
    state = loadStateFromDisk("SBP-level3.txt")
    solutionNode, nodesExplored, totalTime = BFS(state)
    reportResults(solutionNode, nodesExplored, totalTime)

    print "********DFS********"
    state = loadStateFromDisk("SBP-level3.txt")
    dfsNode, nodesExplored, totalTime = DFS(state)
    reportResults(dfsNode, nodesExplored, totalTime)

    print "********IDS********"
    state = loadStateFromDisk("SBP-level3.txt")
    maxDepth = 50
    idsNode, nodesExplored, totalTime = IDS(state, maxDepth)
    reportResults(idsNode, nodesExplored, totalTime)

def reportResults(node, nodesExplored, totalTime):
    if node == None:
        print "Solution not found"
        return
    for move in node.path:
        printMove(move)
    printState(node.state)

    print " "
    print nodesExplored, totalTime, len(node.path)
    print " "

if __name__ == "__main__":
    main()
