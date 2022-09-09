from concurrent.futures import thread
from multiprocessing import Event
from operator import index
import visualiser
import generator
import pygame
import sys
import math
import time 






#Breadth first search
def solveMaze(maze):
    activeCells = []
    neighborList = []
    indexList = []
    indexAcc = 0

    #set first cell
    activeCells.append(maze[1][1])
    indexList.append([0, maze[1][1].id])
    
    
    complete = False 
    while len(activeCells) != 0 and not complete:
        cell = activeCells.pop(0)
        visualiser.draw(cell.col, cell.row, (0, 0, 255))
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
                indexList.append([indexAcc, neighbor.id])

                rTemp = int((cell.row + neighbor.row) / 2)
                cTemp = int((cell.col + neighbor.col) / 2)
                maze[rTemp][cTemp].wall = False
                visualiser.draw(cTemp, rTemp, (0, 0, 255))

                if neighbor.row == len(maze) - 2 and neighbor.col == len(maze[0]) - 2:
                    complete = True
                    neighborList.clear()
                    break
                else:
                    activeCells.append(neighbor)
        indexAcc += 1

                        
    #when exit located
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if not maze[i][j].wall:
                visualiser.draw(j, i, (150, 102, 51))


    currCell = maze[len(maze) - 2][len(maze[0]) - 2]
    prevCell = maze[len(maze) - 2][len(maze[0]) - 2]

    visualiser.draw(currCell.col, currCell.row, (0, 255, 0))

    #monkeybrain
    duoList = indexList[-1]
    currIndex = len(indexList) - 1

    maze1D = []
    #create a 1d list of the maze
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            maze1D.append(maze[i][j])

    while True:
        duoList = indexList[currIndex]
        currIndex = duoList[0]
        currCell = maze1D[indexList[currIndex][1]]

        rTemp = int((currCell.row + prevCell.row) / 2)
        cTemp = int((currCell.col + prevCell.col) / 2)
        visualiser.draw(currCell.col, currCell.row, (0, 255, 0))
        visualiser.draw(cTemp, rTemp, (0, 255, 0))



        
        if currCell.row == 1 and currCell.col == 1:
            visualiser.draw(1, 1, (0, 255, 0))
            break
        prevCell = currCell