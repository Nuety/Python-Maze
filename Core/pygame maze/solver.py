import visualiser
import generator
import math 
import random
import time





#Breadth first search
def solveMazebfs(maze):
    activeCells = []
    neighborList = []
    indexList = []
    indexAcc = 0
    colorBias = 0

    #set first cell
    activeCells.append(maze[1][1])
    indexList.append([0, maze[1][1].id])
    
    
    complete = False 
    while len(activeCells) != 0 and not complete:
        cell = activeCells.pop(0)
        colorBias += 0.001
        if colorBias > 0.3:
            colorBias = 0
        visualiser.draw(cell.col, cell.row, (180 - abs(math.sin(colorBias) * 50), 130 + abs(math.sin(colorBias) * 100) , 0))
        
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

                
                visualiser.draw(cTemp, rTemp, (180 , 130 + abs(math.sin(colorBias) * 100) , 0))
                

                if neighbor.row == len(maze) - 2 and neighbor.col == len(maze[0]) - 2:
                    complete = True
                    neighborList.clear()
                    break
                else:
                    activeCells.append(neighbor)
        indexAcc += 1

        
    #when exit located
    visualiser.drawMaze(maze)


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

#lefthand agent
def solveMazelefthand(maze):
    #draw agent
    agent = maze[1][1]
    visualiser.draw(agent.col, agent.row, (0,150,0))


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
    health = 250000

    while not complete:
        #continue running if front is not clear yet
        rnd = random.randint(0, 100)
        #randomly rotate right
        if not maze[agent.row + left[1]][agent.col + left[0]].wall:
            if rnd < 50:
                #rotate left
                rot = (rot - 1) % 4
                left = directions[(rot-1)%4]
                forward = directions[rot]
                right = directions[(rot+1)%4]
        elif not maze[agent.row + right[1]][agent.col + right[0]].wall:
            if rnd < 50:
                #rotate right
                rot = (rot + 1) % 4
                left = directions[(rot-1)%4]
                forward = directions[rot]
                right = directions[(rot+1)%4]
        #is forward wall?
        if maze[agent.row + forward[1]][agent.col + forward[0]].wall:
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
            visualiser.draw(agent.col, agent.row, (0,50,0))
            agent = maze[agent.row + forward[1]][agent.col + forward[0]]
            visualiser.draw(agent.col, agent.row, (0,150,0))
            path.append(agent)
            health -= 1
            if health <= 0:
                visualiser.draw(agent.col, agent.row, (255,0,0))
                return
        if agent.row == len(maze) - 2 and agent.col == len(maze[0]) - 2:
            complete = True
            break

    #when exit located
    visualiser.drawMaze(maze)

    c1 = 1
    c2 = 0

    currCell = path[c1]
    prevCell = path[c2]

    visualiser.draw(currCell.col, currCell.row, (0, 255, 0))

    while True:
        rTemp = int((currCell.row + prevCell.row) / 2)
        cTemp = int((currCell.col + prevCell.col) / 2)
        visualiser.draw(currCell.col, currCell.row, (0, 255, 0))
        visualiser.draw(cTemp, rTemp, (0, 255, 0))
        c1 += 1
        c2 += 1
        currCell = path[c1]
        prevCell = path[c2]



        
        if currCell.row == len(maze) - 2 and currCell.col == len(maze[0]) - 2:
            visualiser.draw(len(maze) - 2, len(maze[0]) - 2, (0, 255, 0))
            break
        prevCell = currCell



