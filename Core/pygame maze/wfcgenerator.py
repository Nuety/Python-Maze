import random
import numpy

class ecell:
    def __init__(self, r, c, up, right, down, left, ent, toent):
        self.row = r
        self.col = c
        self.dir = [up, right, down, left]
        self.entropy = ent
        self.totent = toent
    collapsed = False
    
    #debug i think
    def info(self):
        return (self.row, self.col, self.entropy, self.totent, self.dir)
    
class displaycell:
    def __init__(self, r, c, inc):
        self.row = r
        self.col = c
        self.id = inc
    wall = True
    visited = False
    
    #debug i think
    def info(self):
        return (self.row, self.col, self.wall)

def setup(maze, cols, rows):
    #init maze cells
    for i in range(cols):
        for j in range(rows):

            #corners
            #top left
            if i == 0 and j == 0:
                entropy = [1,2]
                maze[i][j] = ecell(i,j, 0, 1, 1, 0, entropy, len(entropy))

            elif i == cols-1 and j == rows-1:
                entropy = [1,2]
                maze[i][j] = ecell(i,j, 1, 0, 0, 1, entropy, len(entropy))

            elif i == 0 and j == cols-1:
                entropy = [1,2]
                maze[i][j] = ecell(i,j, 0, 0, 1, 1, entropy, len(entropy))

            elif i == rows-1 and j == 0:
                entropy = [1,2]
                maze[i][j] = ecell(i,j, 1, 1, 0, 0, entropy, len(entropy))

            #sides
            elif i == 0 and j != 0:
                entropy = [0,1,2]
                maze[i][j] = ecell(i,j, 0, 1, 1, 1, entropy, len(entropy))

            elif i == cols-1 and j != 0:
                entropy = [0,1,2]
                maze[i][j] = ecell(i,j, 1, 1, 0, 1, entropy, len(entropy))
                
            elif j == 0 and i != 0:
                entropy = [0,1,2]
                maze[i][j] = ecell(i,j, 1, 1, 1, 0, entropy, len(entropy))
                
            elif j == rows-1 and i != 0:
                entropy = [0,1,2]
                maze[i][j] = ecell(i,j, 1, 0, 1, 1, entropy, len(entropy))
                
            #middle
            else:
                entropy = [0,1,2]
                maze[i][j] = ecell(i,j, 1, 1, 1, 1, entropy, len(entropy))

#refresh neighbor entropy
def refreshEntropy(cell):
    dir = cell.dir 
    if dir == [0,0,0,0]:
        cell.entropy = []
        cell.totent = 0
        cell.collapsed = True
    elif dir == [1,1,1,1]:
        cell.entropy = [0,1,2]
        cell.totent = 3
    elif dir == [1,0,0,0] or dir == [0,1,0,0] or dir == [0,0,1,0] or dir == [0,0,0,1]:
        cell.entropy = [2]
        cell.totent = 1
    elif dir == [1,1,0,0] or dir == [0,1,1,0] or dir == [0,0,1,1] or dir == [1,0,0,1]:
        cell.entropy = [1,2]
        cell.totent = 2
    elif dir == [1,1,1,0] or dir == [0,1,1,1] or dir == [1,0,1,1] or dir == [1,1,0,1]:
        cell.entropy = [0,1,2]
        cell.totent = 3
    elif dir == [1,0,1,0] or dir == [0,1,0,1]:
        cell.entropy = [0,2]
        cell.totent = 2
    # if dir.all() == all([0,0,0,0]):
    #     cell.entropy = []
    #     cell.totent = 0
    #     cell.collapsed = True
    # elif dir.all() == all([1,1,1,1]):
    #     cell.entropy = [0,1,2,3,4]
    #     cell.totent = 5
    # elif dir.all() == all([1,0,0,0]) or dir.all() == all([0,1,0,0]) or dir.all() == all([0,0,1,0]) or dir.all() == all([0,0,0,1]):
    #     cell.entropy = [4]
    #     cell.totent = 1
    # elif dir.all() == all([1,1,0,0]) or dir.all() == all([0,1,1,0]) or dir.all() == all([0,0,1,1]) or dir.all() == all([1,0,0,1]):
    #     cell.entropy = [2,4]
    #     cell.totent = 2
    # elif dir.all() == all([1,1,1,0]) or dir.all() == all([0,1,1,1]) or dir.all() == all([1,0,1,1]) or dir.all() == all([1,1,0,1]):
    #     cell.entropy = [1,2,3,4]
    #     cell.totent = 4
    # elif dir.all() == all([1,0,1,0]) or dir.all() == all([0,1,0,1]):
    #     cell.entropy = [1,4]
    #     cell.totent = 2
    


#check if maze has more entropy
def totalentropy(maze):
    totalentropy = 0
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            totalentropy += maze[i][j].totent
    return totalentropy

#select cell tile
def selectTile(cell):
    rnd = random.randint(0, cell.totent-1)
    newEntropy = cell.entropy[rnd]
    cell.totent = 1
    cell.entropy = newEntropy


#find cell with lowest entropy
def getlowestentropy(maze):
    #rnd to randomly select new "lowest"
    rnd = random.randint(0, 1)
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if not maze[i][j].collapsed:
                currCell = maze[i][j]

    for i in range(len(maze)):
        for j in range(len(maze[0])):
            try:
                if maze[i][j].totent <= currCell.totent and not maze[i][j].collapsed and rnd == 1:
                    currCell = maze[i][j]
            except:
                return -1

    return currCell

def findRotation(cell):
    #rotation of cell
    cellRot = cell.dir


    #rotation of block
    match cell.entropy:
        case 0:
            tileRot = [0,1,0,1]
        case 1:
            tileRot = [1,0,0,1]
        #this must exist
        case 2:
            tileRot = [1,0,0,0]

    while True:
        #random to skip selection so not all will look down
        rnd = random.randint(0,3)

        temp = numpy.subtract(cellRot, tileRot)
        negatives = 0
        for num in temp:
            if num == -1:
                negatives -= 1
        if negatives != 0:
            newRot = [tileRot[3], tileRot[0], tileRot[1], tileRot[2]]
            tileRot = newRot

        
        if rnd == 1:
            newRot = [tileRot[3], tileRot[0], tileRot[1], tileRot[2]]
            tileRot = newRot

        #number of correct positions (not -1)
        count = 0
        temp = numpy.subtract(cellRot, tileRot)
        for num in temp:
            if num != -1:
                count += 1

        if count == 4:
            return tileRot




def newMaze(width: int, height: int):
    #random numbers
    random.seed()

    #init array
    displayrows = int((width * 2) + 1)
    displaycols = int((height * 2) + 1)

    mazeArr= [[displaycell for i in range(displayrows)] for j in range(displaycols)]
    inc = 0
    #init maze cells
    for i in range(displaycols):
        for j in range(displayrows):
            mazeArr[i][j] = displaycell(i,j, inc)
            inc += 1


    cellArr = [[ecell for i in range(width)] for j in range(height)]

    setup(cellArr, height, width)


    #main loop
    while totalentropy(cellArr) > width*height:
        currCell = getlowestentropy(cellArr)
        if not currCell == 0:
            selectTile(currCell)
            currCell.collapsed = True

            rotation = findRotation(currCell)

            #find which corridors to close off
            #array to know which neighbors to close from
            closeArr = numpy.subtract(currCell.dir, rotation)

            #close current cell walls by setting rotation
            currCell.dir = rotation

            #close walls from neighbors
            r = currCell.row - 1
            c = currCell.col - 1
            #up
            if closeArr[0] == 1 and cellArr[r-1][c].dir[2] != 0:
                cellArr[r-1][c].dir[2] = cellArr[r-1][c].dir[2] - 1
                refreshEntropy(cellArr[r-1][c])
            #right
            if closeArr[1] == 1 and cellArr[r][c+1].dir[3] != 0:
                cellArr[r][c+1].dir[3] = cellArr[r][c+1].dir[3] - 1
                refreshEntropy(cellArr[r][c+1])
            #down
            if closeArr[2] == 1 and cellArr[r+1][c].dir[0] != 0:
                cellArr[r+1][c].dir[0] = cellArr[r+1][c].dir[0] - 1
                refreshEntropy(cellArr[r+1][c])
            #left
            if closeArr[3] == 1 and cellArr[r][c-1].dir[1] != 0 :
                cellArr[r][c-1].dir[1] = cellArr[r][c-1].dir[1] - 1
                refreshEntropy(cellArr[r][c-1])

    for row in cellArr:
        for cell in row:
            #remove wall of self
            mazeArr[int((2 * cell.row) + 1)][int((2 * cell.col) + 1)].wall = False
            #remove wall of passage
            if cell.dir[0] == 1:
                mazeArr[int((2 * cell.row))][int((2 * cell.col) + 1)].wall = False
            if cell.dir[1] == 1:
                mazeArr[int((2 * cell.row) + 1)][int((2 * cell.col) + 2)].wall = False
            if cell.dir[2] == 1:
                mazeArr[int((2 * cell.row) + 2)][int((2 * cell.col) + 1)].wall = False
            if cell.dir[3] == 1:
                mazeArr[int((2 * cell.row) + 1)][int((2 * cell.col))].wall = False




    return mazeArr