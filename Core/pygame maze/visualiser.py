import generator
import pygame
import sys
import math
import threading
import time


class MazeVisualiser:
    def guiLoop(self):
        clock = pygame.time.Clock()
        while not self.tevent.is_set():
            clock.tick(60)  # Adjust the frame rate as needed
            self.threadUpdate()

    def __init__(self, xWin, yWin, xCells, yCells):
        self.cell_Hor = xCells
        self.cell_Ver = yCells
        self.winSizeX = xWin
        self.winSizeY = yWin

        self.cellwidth = xWin / ((self.cell_Hor * 2) + 1)
        # yWin - 50 to account for back to manu button
        self.cellheight = (yWin - 50) / ((self.cell_Ver * 2) + 1)

        pygame.font.init()

        self.win = pygame.display.set_mode((xWin, yWin))
        pygame.display.set_caption('MazeyMan 2.1')
        self.win.fill((70, 50, 30))

        #deligate multithreading stuff
        self.tevent = threading.Event()
        gui = threading.Thread(target=self.guiLoop, args=())
        gui.start()

    def threadUpdate(self):
        pygame.display.update()
        

                
    #threadstop
    def threadStop(self):
        self.tevent.set()

    def drawMaze(self, maze):
        for i in range(len(maze)):
            for j in range(len(maze[0])):
                if not maze[i][j].wall:
                    self.draw(j, i, (150, 102, 51))

    def draw(self, x, y, color):
        pygame.draw.rect(self.win, (color), pygame.Rect(x * self.cellwidth, y * self.cellheight, self.cellwidth + 1, self.cellheight + 1))

    def visMaze(self):
        # Draw a button
        button_rect = pygame.Rect(0, self.winSizeY - 50, self.winSizeX, 50)  # - 50 to account for button size
        pygame.draw.rect(self.win, (20, 20, 20), button_rect) 
        font = pygame.font.Font(None, 36)
        text = font.render("Back to Main Menu", True, (255, 255, 255))  # White text
        text_rect = text.get_rect(center=button_rect.center)
        self.win.blit(text, text_rect)

        pygame.display.flip()