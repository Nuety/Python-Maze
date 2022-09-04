import visualiser
import generator
import solver

#customize maze


#window size
win_width = 1920
win_height = 1080

#horizontal cells
xCells = 100

#vertical cells
yCells = 100

#solve?
solve = True


visualiser.init(win_width, win_height, xCells, yCells)

maze = generator.newMaze(int(xCells), int(yCells), visualiser.cbvisualiser)

if solve: 
    solver.solveMaze(maze, visualiser.cbvisualiser)

#has while true so run last to keep still image of finished maze without crashing
visualiser.visMaze()