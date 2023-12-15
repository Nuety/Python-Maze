import visualiser
import generator
import math 
import random
import time
import pygame
import sys

class MazeSolver:
    def __init__(self, vis, maz, colCells, rowCells):
        self.visual = vis
        self.maze = maz

        self.mazeCellLenRow = colCells
        self.mazeCellLenCol = rowCells

        self.firstcellRow = random.randrange(1, (self.mazeCellLenRow * 2) + 1, 2)
        self.firstcellCol = random.randrange(1, (self.mazeCellLenCol * 2) + 1, 2)
        self.lastcellRow = random.randrange(1, (self.mazeCellLenRow * 2) + 1, 2)
        self.lastcellCol = random.randrange(1, (self.mazeCellLenCol * 2) + 1, 2)

    #Breadth first search
    def solveMazebfs(self, solvetimestep):
        activeCells = []
        neighborList = []
        indexList = []
        indexAcc = 0
        colorBias = 0

        #set first cell
        activeCells.append(self.maze[self.firstcellRow][self.firstcellCol])
        #zero is for the first in the incrementer list
        indexList.append([0, self.maze[self.firstcellRow][self.firstcellCol].id])
        
        # activeCells.append(self.maze[1][1])
        # indexList.append([0, self.maze[1][1].id])

        #draw start blue
        self.visual.draw(self.firstcellRow, self.firstcellCol, (0,0,255))

        #draw end red
        self.visual.draw(self.lastcellRow, self.lastcellCol, (255,0,0))
        
        complete = False 
        while len(activeCells) != 0 and not complete:
            cell = activeCells.pop(0)
            colorBias += 0.001
            if colorBias > 0.3:
                colorBias = 0

            self.visual.draw(cell.col, cell.row, (180 - abs(math.sin(colorBias) * 50), 130 + abs(math.sin(colorBias) * 100) , 0))
            
            cell.visited = True
            if generator.hasNeighbor(cell, self.maze):
                neighborList.clear()
                
                #north
                if self.maze[cell.row - 1][cell.col].wall == False:
                    neighborList.append(self.maze[cell.row - 2][cell.col])
                #south
                if self.maze[cell.row + 1][cell.col].wall == False:
                    neighborList.append(self.maze[cell.row + 2][cell.col])
                #east
                if self.maze[cell.row][cell.col + 1].wall == False:
                    neighborList.append(self.maze[cell.row][cell.col + 2])
                #west
                if self.maze[cell.row][cell.col - 1].wall == False:
                    neighborList.append(self.maze[cell.row][cell.col - 2])

                for c in reversed(range(len(neighborList))):
                    if neighborList[c].visited:
                        del neighborList[c]
                for neighbor in neighborList:
                    if not neighbor.isFound:

                        indexList.append([indexAcc, neighbor.id])

                        rTemp = int((cell.row + neighbor.row) / 2)
                        cTemp = int((cell.col + neighbor.col) / 2)
                        self.maze[rTemp][cTemp].wall = False

                        
                        self.visual.draw(cTemp, rTemp, (180 , 130 + abs(math.sin(colorBias) * 100) , 0))
                        

                        if neighbor.row == self.lastcellRow and neighbor.col == self.lastcellCol:
                            complete = True
                            neighborList.clear()
                            break
                        else:
                            activeCells.append(neighbor)
                            neighbor.isFound = True
            indexAcc += 1

        #when exit located
        self.visual.drawMaze(self.maze)
        time.sleep(0.5)

        currCell = self.maze[self.lastcellRow][self.lastcellCol]
        prevCell = self.maze[self.lastcellRow][self.lastcellCol]

        self.visual.draw(currCell.col, currCell.row, (0, 255, 0))

        #monkeybrain
        duoList = indexList[-1]
        currIndex = len(indexList) - 1

        maze1D = []
        #create a 1d list of the maze
        for i in range(len(self.maze)):
            for j in range(len(self.maze[0])):
                maze1D.append(self.maze[i][j])

        while True:
            duoList = indexList[currIndex]
            currIndex = duoList[0]
            currCell = maze1D[indexList[currIndex][1]]

            rTemp = int((currCell.row + prevCell.row) / 2)
            cTemp = int((currCell.col + prevCell.col) / 2)
            time.sleep(solvetimestep)

            self.visual.draw(currCell.col, currCell.row, (0, 255, 0))
            self.visual.draw(cTemp, rTemp, (0, 255, 0))

            if currCell.row == self.firstcellRow and currCell.col == self.firstcellCol:
                #draw start blue
                self.visual.draw(self.firstcellCol, self.firstcellRow, (0,0,255))

                #draw end red
                self.visual.draw(self.lastcellCol, self.lastcellRow, (255,0,0))
                break
            prevCell = currCell

    #lefthand agent
    def solveMazelefthand(self):
        #draw agent
        agent = self.maze[self.firstcellRow][self.firstcellRow]
        self.visual.draw(agent.col, agent.row, (0,150,0))


        #rotation stuff
        #down left up right (in that order)
        directions = [[0,1], [-1,0], [0,-1], [1,0]]
        #rot can overflow, i don't care
        rot = 0
        left = directions[(rot-1)%4]
        forward = directions[rot]
        right = directions[(rot+1)%4]
        complete = False
        path = []
        health = 25000000

        while not complete:
            #continue running if front is not clear yet
            rnd = random.randint(0, 100)
            #randomly rotate right
            if not self.maze[agent.row + left[1]][agent.col + left[0]].wall:
                if rnd < 50:
                    #rotate left
                    rot = (rot - 1) % 4
                    left = directions[(rot-1)%4]
                    forward = directions[rot]
                    right = directions[(rot+1)%4]
            elif not self.maze[agent.row + right[1]][agent.col + right[0]].wall:
                if rnd < 50:
                    #rotate right
                    rot = (rot + 1) % 4
                    left = directions[(rot-1)%4]
                    forward = directions[rot]
                    right = directions[(rot+1)%4]
            #is forward wall?
            if self.maze[agent.row + forward[1]][agent.col + forward[0]].wall:
                #is right wall?
                
                if rnd < 50:
                    #rotate right
                    rot = (rot + 1) % 4
                    left = directions[(rot-1)%4]
                    forward = directions[rot]
                    right = directions[(rot+1)%4]
                else:
                    #rotate left
                    rot = (rot - 1) % 4
                    left = directions[(rot-1)%4]
                    forward = directions[rot]
                    right = directions[(rot+1)%4]
            else:
                #agent takes step in direction
                self.visual.draw(agent.col, agent.row, (0,50,0))
                agent = self.maze[agent.row + forward[1]][agent.col + forward[0]]
                self.visual.draw(agent.col, agent.row, (0,150,0))
                path.append(agent)
                health -= 1
                if health <= 0:
                    self.visual.draw(agent.col, agent.row, (255,0,0))
                    return
            if agent.row == self.lastcellRow and agent.col == self.lastcellCol:
                complete = True
                break

        #when exit located
        self.visual.drawMaze(self.maze)

        c1 = 1
        c2 = 0

        currCell = path[c1]
        prevCell = path[c2]

        self.visual.draw(currCell.col, currCell.row, (0, 255, 0))

        while True:
            rTemp = int((currCell.row + prevCell.row) / 2)
            cTemp = int((currCell.col + prevCell.col) / 2)
            
            self.visual.draw(cTemp, rTemp, (0, 255, 0))
            self.visual.draw(currCell.col, currCell.row, (0, 255, 0))
            c1 += 1
            c2 += 1
            currCell = path[c1]
            prevCell = path[c2]
            
            if currCell.row == self.lastcellRow and currCell.col == self.lastcellCol:
                #draw start blue
                self.visual.draw(self.firstcellCol, self.firstcellRow, (0,0,255))

                #draw end red
                self.visual.draw(self.lastcellCol, self.lastcellRow, (255,0,0))
                break
            prevCell = currCell

    #amogus
    def solveFindAmogus(self):
        Amogi = []

        for row in range(1, (self.mazeCellLenRow * 2) - 3, 2):
            for col in range(1, (self.mazeCellLenCol * 2) - 1, 2):
                upAmog = []
                leftAmog = []
                for aCol in range(col, col + 3):
                    for aRow in range(row, row + 5):
                        upAmog.append(self.maze[aRow][aCol])
                        leftAmog.append(self.maze[aCol][aRow])
                
                Amogi.append(upAmog)
                Amogi.append(leftAmog)

        for row in range(1, (self.mazeCellLenRow * 2) - 3, 2):
            for col in range(1, (self.mazeCellLenCol * 2) - 1, 2):
                downAmog = []
                rightAmog = []
                for aCol in range(col, col - 3, -1):
                    for aRow in range(row, row - 5, -1):
                        downAmog.append(self.maze[aCol][aRow])
                        rightAmog.append(self.maze[aRow][aCol])
                Amogi.append(downAmog)
                Amogi.append(rightAmog)
        for amog in Amogi:
            skip = False
            for cell in amog:
                if cell.visited:
                    skip = True
            if amog[5].wall or amog[7].wall or amog[3].wall or amog[13].wall or not amog[9].wall:
                skip = True
            if amog[1].wall == amog[11].wall:
                skip = True

            if not skip:
                for cell in amog:
                    if not cell.wall:
                        self.visual.draw(cell.col, cell.row, (255,0,0))
                    cell.visited = True