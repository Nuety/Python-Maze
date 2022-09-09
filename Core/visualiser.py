import generator
import pygame
import sys
import math
import threading
import time

def guiLoop(event):
    # clock = pygame.time.Clock()
    # while not event.is_set():
    #     clock.tick(60)
    #     threadUpdate()
    t0 = time.time()
    while not event.is_set():
        dt = time.time()
        if (dt - t0) % 0.1 < 0.1:
            threadUpdate()

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

    #delicate multithreading stuff
    global tevent
    tevent = threading.Event()
    gui = threading.Thread(target=guiLoop, args=(tevent,))
    gui.start()

def threadUpdate():
    pygame.display.update()
    for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                sys.exit(0)
            

def screenUpdate():
    pygame.display.update()

#threadstop
def threadStop():
    tevent.set()

def draw(x, y, color):
    pygame.draw.rect(win, (color), pygame.Rect(x * cellwidth, y * cellheight, cellwidth + 1, cellheight + 1))
    

def cbvisualiser(x, y, color):
    pygame.draw.rect(win, (color), pygame.Rect(x * cellwidth, y * cellheight, cellwidth + 1, cellheight + 1))
    
    screenUpdate()

    for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                sys.exit(0) 
    return

def visMaze():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                sys.exit(0)
