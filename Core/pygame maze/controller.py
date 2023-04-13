from inspect import _void
import visualiser
import generator
import solver
import time
import wfcgenerator


#customize maze


#window size
win_width = 1920
win_height = 1080

#horizontal cells
xCells = 100


#vertical cells
yCells = 100

#select generator
#wave function collapse "wfc"
#Depth first "df"
generatormethod = "wfc"

# visualise?
visualise = True

#solve?
solve = True

#select solve method
# "bfs" breadth first search
# "lefthand" - this is really bad
method = "bfs"



match generatormethod:
    case "df":
        maze = generator.newMaze(int(xCells), int(yCells))
    case "wfc":
        maze = wfcgenerator.newMaze(int(xCells), int(yCells))


if visualise:
    visualiser.init(win_width, win_height, xCells, yCells)
    visualiser.drawMaze(maze)

    if solve: 
        match method:
            case "bfs":
                solver.solveMazebfs(maze)
            case "lefthand":
                solver.solveMazelefthand(maze)
                


    #has while true so run last to keep still image of finished maze without crashing
    time.sleep(2)
    visualiser.threadStop()
    visualiser.visMaze()