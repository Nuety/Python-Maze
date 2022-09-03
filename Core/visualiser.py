import generator
import pygame
import sys
import math


win_width = 1920
win_height = 1080

#size of cells
yCells = 350
xCells = 550
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
                pygame.draw.rect(win, (127, 127, 127), pygame.Rect(i * cellwidth, j * cellheight, cellwidth + 1, cellheight + 1))

    pygame.display.update()
                    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                sys.exit(0)
