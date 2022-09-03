import generator
import pygame
import sys
import math


win_width = 1920
win_height = 1080

#size of cells
xCells = 96
yCells = 54
cellwidth = win_width / ((xCells * 2) + 1)
cellheight = win_height / ((yCells * 2) + 1)

pygame.init()
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption('MazeyMan')

def cbvisualiser(x, y):
    pygame.draw.rect(win, (150, 102, 51), pygame.Rect(x * cellwidth, y * cellheight, cellwidth + 1, cellheight + 1))
    pygame.display.update()
    for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                sys.exit(0)
    return

def visMaze():
    maze = generator.newMaze(int(xCells), int(yCells), cbvisualiser)

    run = True

    for i in range(int(((xCells * 2) + 1))):
        for j in range(int(((yCells * 2) + 1))):
            if maze[j][i] == True:
                pygame.draw.rect(win, (70, 50, 30), pygame.Rect(i * cellwidth, j * cellheight, cellwidth + 1, cellheight + 1))

    while run:
        pygame.display.update()
                        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    sys.exit(0)
