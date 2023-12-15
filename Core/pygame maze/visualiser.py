import pygame
import threading
from threadManager import ThreadManager

class MazeVisualiser:
    def guiLoop(self):
        while not self.tevent.is_set():
            with self.mutex:
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
        pygame.display.set_caption('MazeyMan 2.5')
        self.win.fill((70, 50, 30))
        self.back_buffer = pygame.Surface((xWin, yWin))
        self.back_buffer.fill((70, 50, 30))

        # Draw a button
        self.menu_button_rect = pygame.Rect(0, yWin - 50, xWin, 50)
        self.menu_button_color = (0, 0, 0)
        self.menu_font = pygame.font.Font(None, 36)
        self.menu_button_text = self.menu_font.render("Back to Menu", True, (255, 255, 255))

        #deligate multithreading stuff
        self.thread_manager = ThreadManager()
        self.mutex = threading.Lock()
        self.tevent = threading.Event()
        threading.Thread(target=self.guiLoop, args=()).start()

    def threadUpdate(self):
        self.win.blit(self.back_buffer, (0, 0))
        pygame.draw.rect(self.win, self.menu_button_color, self.menu_button_rect)
        self.win.blit(self.menu_button_text, (self.menu_button_rect.centerx - self.menu_button_text.get_width() // 2, self.menu_button_rect.centery - self.menu_button_text.get_height() // 2))

        pygame.display.flip()
    
    #threadstop
    def threadStop(self):
        self.tevent.set()

    def drawMaze(self, maze):
        chunk_size_x = max(1, int(self.winSizeX * 1/2))
        chunk_size_y = max(1, int(self.winSizeY * 1/2))

        for i in range(0, len(maze), chunk_size_y):
            for j in range(0, len(maze[0]), chunk_size_x):
                chunk = [row[j:j + chunk_size_x] for row in maze[i:i + chunk_size_y]]
                self.thread_manager.start_thread(self.drawThread, args=(chunk, i, j))

    def drawThread(self, chunk, i, j):
        for x in range(len(chunk)):
            for y in range(len(chunk[0])):
                if not chunk[x][y].wall:
                    self.draw(y + j, x + i, (150, 102, 51))

    def drawMazeAsync(self, cell):
        threading.Thread(target=self.drawCellThread, args=(cell,)).start()

    def drawCellThread(self, cell):
        self.draw(cell.col, cell.row, (150, 102, 51))

    def draw(self, x, y, color):
        pygame.draw.rect(self.back_buffer, color, pygame.Rect(x * self.cellwidth, y * self.cellheight, self.cellwidth + 1, self.cellheight + 1))

    def visMaze(self):
        pass