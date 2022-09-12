import random

class cell:
    def __init__(self, r, c, number):
        self.row = r
        self.col = c
        self.id = number
    wall = True
    visited = False
    
#lazy redundancy
def deadEnd(cell, maze):
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
            
    #return random cell from the neighborlist
    rnd = random.randint(0, len(cellList) - 1)
    neighbor = cellList[rnd]

    rTemp = int((cell.row + neighbor.row) / 2)
    cTemp = int((cell.col + neighbor.col) / 2)
    
    
    maze[rTemp][cTemp].wall = False

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
        if not cellList[c].visited:
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

    if cellList == []:
        return False

    for c in reversed(range(len(cellList))):
        if cellList[c].visited:
            del cellList[c]

    #return random cell from the neighborlist
    rnd = random.randint(0, len(cellList) - 1)

    return cellList[rnd]

def newMaze(width: int, height: int):
    #random numbers
    random.seed()
    inc = 0

    #stack to backtrack
    cellStack = []

    #init array
    rows = int((width * 2) + 1)
    cols = int((height * 2) + 1)
    mazeArr = [[cell for i in range(rows)] for j in range(cols)]

    #init maze cells
    for i in range(cols):
        for j in range(rows):
            mazeArr[i][j] = cell(i,j, inc)
            inc += 1

    #assign first cell
    cellStack.append(mazeArr[1][1])
    currCell = mazeArr[1][1]
    currCell.visited = True
    currCell.wall = False

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

            cellStack.append(neighbor)
            currCell = neighbor
            
        else:
            #return random cell from the neighborlist
            rnd = random.randint(0, 100)

            if rnd < 1:
                deadEnd(currCell, mazeArr)

            currCell = cellStack[-1]
            cellStack.pop()

    #unset scisited status
    for i in range(cols):
        for j in range(rows):
            mazeArr[i][j].visited = False

    return mazeArr