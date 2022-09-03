
import random
from xmlrpc.client import Boolean
from colorama import init
from colorama import Fore, Back, Style
init(autoreset=True)



class cell:
    def __init__(self, r, c):
        self.row = r
        self.col = c
    wall = True
    visited = False

#Check if there is a unvisited neighborcell
def hasNeighbor(cell, maze):
    cellList = []

    #north
    if cell.row - 2 >= 0:
        cellList.append(maze[cell.row - 2][cell.col])
    #south
    if cell.row + 2 <= len(maze) - 1:
        cellList.append(maze[cell.row + 2][cell.col])
    #east
    if cell.col + 2 <= len(maze[0]) - 1:
        cellList.append(maze[cell.row][cell.col + 2])
    #west
    if cell.col - 2 >= 0:
        cellList.append(maze[cell.row][cell.col - 2])


    for c in range(len(cellList)):
        if cellList[c].visited == False:
            return True


    return False

#get random unvisited neighborcell
def getNeighbor(cell, maze):
    cellList = []

    #north
    if cell.row - 2 >= 0:
        cellList.append(maze[cell.row - 2][cell.col])
    #south
    if cell.row + 2 <= len(maze) - 1:
        cellList.append(maze[cell.row + 2][cell.col])
    #east
    if cell.col + 2 <= len(maze[0]) - 1:
        cellList.append(maze[cell.row][cell.col + 2])
    #west
    if cell.col - 2 >= 0:
        cellList.append(maze[cell.row][cell.col - 2])

    for c in reversed(range(len(cellList))):
        if cellList[c].visited == True:
            del cellList[c]

    #return random cell from the neighborlist
    rnd = random.randint(0, len(cellList) - 1)

    return cellList[rnd]

def newMaze(width: int, height: int, cb):
    #random numbers
    random.seed()

    #stack to backtrack
    cellStack = []


    #init array
    rows = ((width * 2) + 1)
    cols = ((height * 2) + 1)
    mazeArr = [[cell for i in range(rows)] for j in range(cols)]

    #init maze cells
    for i in range(cols):
        for j in range(rows):
            mazeArr[i][j] = cell(i,j)

    #assign first cell
    cellStack.append(mazeArr[1][1])
    currCell = mazeArr[1][1]
    currCell.visited = True
    currCell.wall = False

    #color first cell
    cb(currCell.col, currCell.row)

    #place entry and exit holes
    mazeArr[0][1].wall = False
    mazeArr[-1][-2].wall = False

    #main loop
    while len(cellStack) > 0:
        if hasNeighbor(currCell, mazeArr):
            neighbor = getNeighbor(currCell, mazeArr)
            neighbor.visited = True
            neighbor.wall = False

            #remove wall between currCell and neighbor
            rTemp = int((currCell.row + neighbor.row) / 2)
            cTemp = int((currCell.col + neighbor.col) / 2)
            
            mazeArr[rTemp][cTemp].wall = False
            
            cb(currCell.col, currCell.row)
            cb(cTemp, rTemp)

            cellStack.append(neighbor)
            currCell = neighbor

            cb(currCell.col, currCell.row)
            
        else: 
            currCell = cellStack[-1]
            cellStack.pop()
    
    #create bool list to return
    boolArr = [[True for i in range(rows)] for j in range(cols)]
    for i in range(cols):
        for j in range(rows):
            boolArr[i][j] = mazeArr[i][j].wall

    return boolArr




#DEBUG
mazeHeight = 10
mazeWidth = 30
def DEBUG():
    testarr = newMaze(mazeWidth, mazeHeight)
    rows = ((mazeWidth * 2) + 1)
    cols = ((mazeHeight * 2) + 1)
    for i in range(cols):
        print('')
        for j in range(rows):
            if testarr[i][j] == True:
                print(Back.RED + '.', end='')
            else:
                print(Back.GREEN + '.', end='')