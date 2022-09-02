import generator
import pygame
import numpy
import sys
import math


win_width = 1920
win_height = 1080

#size of cells
yCells = 10
xCells = 10
cellwidth = win_width / ((xCells * 2) + 1)
cellheight = win_height / ((yCells * 2) + 1)



pygame.init()
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption('MazeyMan')

clock = pygame.time.Clock()


maze = generator.newMaze(int(xCells), int(yCells))

run = True

while run:

    for i in range(int(((xCells * 2) + 1))):
        for j in range(int(((yCells * 2) + 1))):
            if maze[j][i] == True:
                for c in range(int(cellwidth)):
                    for c2 in range(int(cellheight)):
                        pygame.draw.line(win, (127, 127, 127), (i * cellwidth, j * cellheight), (i * cellwidth + c, j * cellheight + c2))


    pygame.display.update()
                    


    

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                sys.exit(0)
