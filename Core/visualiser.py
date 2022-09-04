import generator
import pygame
import sys
import math



def init(xWin, yWin, xCells, yCells):
    global cellwidth
    global cellheight
    global win
    global cell_Hor
    global cell_Ver


    cell_Hor = xCells
    cell_Ver = yCells

    cellwidth = xWin / ((cell_Hor * 2) + 1)
    cellheight = yWin / ((cell_Ver * 2) + 1)

    pygame.init()
    win = pygame.display.set_mode((xWin, yWin))
    pygame.display.set_caption('MazeyMan')
    win.fill((70, 50, 30))

def cbvisualiser(x, y, color):
    pygame.draw.rect(win, (color), pygame.Rect(x * cellwidth, y * cellheight, cellwidth + 1, cellheight + 1))
    
    pygame.display.update()
    
    for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                sys.exit(0) 
    return

def visMaze():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                sys.exit(0)
