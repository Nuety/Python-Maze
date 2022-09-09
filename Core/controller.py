from inspect import _void
import visualiser
import generator
import solver

#customize maze


#window size
win_width = 1920
win_height = 1080

#horizontal cells
xCells = 384

#vertical cells
yCells = 216

#show generation?
showGenerator = False

#solve?
solve = True

#show solution?
showSolve = False

visualiser.init(win_width, win_height, xCells, yCells)


if showGenerator:
    maze = generator.newMaze(int(xCells), int(yCells), visualiser.cbvisualiser)
else:
    maze = generator.newMaze(int(xCells), int(yCells), visualiser.draw)
    visualiser.screenUpdate()



if solve: 
    if showSolve:
        solver.solveMaze(maze, visualiser.screenUpdate)
    else:
        solver.solveMaze(maze, _void)

#has while true so run last to keep still image of finished maze without crashing
visualiser.visMaze()