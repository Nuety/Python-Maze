from asyncio.windows_events import NULL
from locale import currency
import visualiser
import generator
import pygame
import sys
import math


#Breadth first search
def solveMaze(maze, cbDraw):
    visitedCells = []
    activeCells = []
    neighborList = []
    indexList = []

    #set first cell
    activeCells.append(maze[1][1])
    visitedCells.append(maze[1][1])
    complete = False
    
    while not complete:
        for cell in activeCells:
            cbDraw(cell.col, cell.row, (0, 0, 255))
            cell.visited = True
            if generator.hasNeighbor(cell, maze):
                neighborList.clear()
                
                #north
                if maze[cell.row - 1][cell.col].wall == False:
                    neighborList.append(maze[cell.row - 2][cell.col])
                #south
                if maze[cell.row + 1][cell.col].wall == False:
                    neighborList.append(maze[cell.row + 2][cell.col])
                #east
                if maze[cell.row][cell.col + 1].wall == False:
                    neighborList.append(maze[cell.row][cell.col + 2])
                #west
                if maze[cell.row][cell.col - 1].wall == False:
                    neighborList.append(maze[cell.row][cell.col - 2])

                for c in reversed(range(len(neighborList))):
                    if neighborList[c].visited:
                        del neighborList[c]
                
                for neighbor in neighborList:
                    visitedCells.append(neighbor)
                    
                    indexList.append([cell.id, neighbor.id])

                    rTemp = int((cell.row + neighbor.row) / 2)
                    cTemp = int((cell.col + neighbor.col) / 2)
                    maze[rTemp][cTemp].wall = False
                    cbDraw(cTemp, rTemp, (0, 0, 255))

                    if neighbor.row == len(maze) - 2 and neighbor.col == len(maze[0]) - 2:
                        complete = True
                        indexList.append([cell.id, neighbor.id])
                    else:
                        activeCells.append(neighbor)

                    

            activeCells.remove(cell)

                        
    #when exit located
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if not maze[i][j].wall:
                visualiser.draw(j, i, (150, 102, 51))
    visualiser.screenUpdate()

    complete = False

    currCell = maze[len(maze) - 2][len(maze[0]) - 2]
    prevCell = maze[len(maze) - 2][len(maze[0]) - 2]

    #monkeybrain
    duoList = indexList[-1]
    currIndex = duoList[1]
    visualiser.draw(currCell.col, currCell.row, (0, 255, 0))
    print(duoList)


    maze1D = []
    #create a 1d list of the maze
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            maze1D.append(maze[i][j])

    while not complete:
        
                
        


        visualiser.screenUpdate()

        for i in indexList:
            if i[1] == currIndex:
                duoList = i
        currIndex = duoList[0]
        currCell = maze1D[currIndex]
        print(duoList)

        rTemp = int((currCell.row + prevCell.row) / 2)
        cTemp = int((currCell.col + prevCell.col) / 2)
        visualiser.draw(cTemp, rTemp, (0, 255, 0))
        visualiser.draw(currCell.col, currCell.row, (0, 255, 0))
        
        prevCell = currCell
        
        if currCell.row == 1 and currCell.col == 1:
            visualiser.draw(1, 1, (0, 255, 0))
            visualiser.screenUpdate()
            complete = True