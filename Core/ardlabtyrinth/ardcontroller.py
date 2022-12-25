from generator import *
import ardsolve
import serial
import time


#customize maze
#should be set to the exact size of the led board

#horizontal cells
xCells = 7

#vertical cells
yCells = 7



while (True):
    maze = newMaze(int(xCells), int(yCells))
    arduino = serial.Serial(port='COM8', baudrate=460800, timeout=.1)
    arduino.write(bytes('CLEAR\n', 'utf-8'))

    for i in range(1 + xCells * 2):
        for j in range(1 + yCells * 2):
            if maze[i][j].wall:
                (r,g,b) = (48, 0, 0)
            else:
                (r,g,b) = (0, 0, 0)
            send = 'SET %03d %03d %03d %03d %03d\n'%(i,j,r,g,b)
            arduino.write(bytes(send, 'utf-8'))
    
    # Make entry green
    arduino.write(bytes('SET 001 000 000 48 000\n', 'utf-8'))
    # Make exit green
    arduino.write(bytes('SET 013 014 000 48 000\n', 'utf-8'))
    arduino.write(bytes('PRINT\n'.encode()))

    solvedMaze = ardsolve.solveMaze(maze)

    for c in reversed(solvedMaze):
        y, x = c
        sendsolve = 'SET %03d %03d 000 048 000\n'%(x,y)
        arduino.write(bytes(sendsolve, 'utf-8'))
        arduino.write(bytes('PRINT\n'.encode()))
        time.sleep(0.05)



    time.sleep(2)
    arduino.close()

