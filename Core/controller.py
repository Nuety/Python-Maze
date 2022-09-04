import visualiser
import generator

#customize maze


#window size
win_width = 1920
win_height = 1080

#horizontal cells
xCells = 96

#vertical cells
yCells = 54

#solve?
solver = True


visualiser.init(win_width, win_height, xCells, yCells)

maze = generator.newMaze(int(xCells), int(yCells), visualiser.cbvisualiser)


#has while true so run last to keep still image of finished maze
visualiser.visMaze()