from inspect import _void
import visualiser
import generator
import solver
import time


#customize maze


#window size
win_width = 1920
win_height = 1080

#horizontal cells
xCells = 192

#vertical cells
yCells = 108

# visualise?
visualise = True

#solve?
solve = True






maze = generator.newMaze(int(xCells), int(yCells))

if visualise:
    visualiser.init(win_width, win_height, xCells, yCells)
    visualiser.drawMaze(maze)

    if solve: 
        solver.solveMaze(maze)


    #has while true so run last to keep still image of finished maze without crashing
    time.sleep(2)
    visualiser.threadStop()
    visualiser.visMaze()