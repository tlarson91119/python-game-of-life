#   Game of Life

#   CONTROLS:
#   - +/- keys increase/decrease the simulation speed
#   - Spacebar will pause/resume simulation
#   - "c", when paused, will clear the board
#   - "s", save board state
#   - "r", restore from last save
#   - "Control+s" save to file (board<#>.dat)

import sys
import os.path

import struct
import random
import math
import time
import pygame

# Initialize PyGame
pygame.init()

# Target Framerate
fps = 60
fpsClock = pygame.time.Clock()
gameDelay = 0.125;

# Screen Dimensions
screen_width, screen_height = 640, 480 
screen = pygame.display.set_mode((screen_width, screen_height))

# Screen Title and Icon
pygame.display.set_caption("Game of Life")
img = pygame.image.load("icon.png")
pygame.display.set_icon(img)

# Colors
BLACK   = (0,0,0)
GREY    = (0,25,25)
GREEN   = (0,255,15)
RED     = (175,0,0)
########################################
#           Game Of Life Code          #
########################################
cellSize = 8            # Size of the sells in pixels
generations = 1000      # Number of iterations

mouseDown = False           # True when mouse button pressed (False when released)
prevMousePosition = (0, 0)  # For drawing functionality

# Generate a random bit value
def randomBit():
    if round( random.uniform(0, 1)) == 1 and round( random.uniform(0,1)) == 1:
        return round( random.uniform(0, 1))
    return 0

# Returns a randomly generated board
def random_state(w, h):
    random_board = [[0 for i in range(w)] for j in range(h)]

    for y in range(h):
        for x in range(w):
            random_board[y][x] = randomBit()
    return random_board

# Returns an empty board
def dead_state(w, h):
    dead_board = [[0 for i in range(w)] for j in range(h)]
    return dead_board

# Save the boards current state (press r when paused to restore)
def save_state(board):
    return board

def save_to_file(board):
    i = 0
    # Check if files exist
    while os.path.exists("board%s.dat" % i):
        i += 1
    fname = "board%s.dat" % i

    with open(fname, "wb") as f:
        for row in board:
            for col in row:
                newByte = bytearray(col)
                f.write(struct.pack("?", newByte))     

# Calculate Next Board State
def next_board_state(board):
    board_width     = len(board[0])
    board_height    = len(board)
    h = board_height - 1      # Subtract one to avoid out of range indexes
    w = board_width - 1
    new_board = [[0 for i in range(board_width)] for j in range(board_height)]

    neighbors = 0

    # Iterate through each cell
    for y in range( board_height ):
        for x in range( board_width ):
            neighbors = 0

            if (x > 0 and y > 0) and (board[y-1][x-1] == 1):# Top-Left
                neighbors += 1
            
            if (y > 0) and (board[y-1][x] == 1):            # Top
                neighbors += 1

            if y > 0 and x < w and board[y-1][x+1] == 1:    # Top-Right
                neighbors += 1

            if x < w and board[y][x+1] == 1:                # Right
                neighbors += 1

            if x < w and y < h and board[y+1][x+1] == 1:    # Bottom-Right
                neighbors += 1

            if y < h and board[y+1][x] == 1:                # Bottom
                neighbors += 1

            if x > 0 and y < h and board[y+1][x-1] == 1:    # Bottom-Left
                neighbors += 1

            if x > 0 and board[y][x-1] == 1:                # Left
                neighbors += 1

            # Determine if a cell should die, live or be born
            if board[y][x] == 1 and (neighbors == 2 or neighbors == 3):
                # Cell is alive and has 2 or 3 neighbors (Keep alive)
                new_board[y][x] = 1
            elif board[y][x] == 0 and neighbors == 3:
                # Cell has no life but has 3 neighbors, give it some life
                new_board[y][x] = 1
            else:
                # This poor cell dies either because it's overpopulated or underpopulated
                new_board[y][x] = 0
    return new_board

def render(state):
    if isinstance(state, list):
        for y in range( len(state) ):
            for x in range( len(state[y]) ):
                if( state[y][x] == 1 ):
                    pygame.draw.rect(screen, GREEN,
                        (x*cellSize, y*cellSize, cellSize, cellSize))
                else:
                    pygame.draw.rect(screen, BLACK,
                        (x*cellSize, y*cellSize, cellSize, cellSize))
        # Draw Vertical Lines
        for x in range( round(screen_width/cellSize) ):
            pygame.draw.line(screen, GREY, (x*cellSize, 0), (x*cellSize, screen_height))
        # Draw Horizontal Lines
        for y in range( round(screen_height/cellSize) ):
            pygame.draw.line(screen, GREY, (0, y*cellSize), (screen_width, y*cellSize))
        return 0
    else:
        print("Error (render): argument is not a list...")
        return 1

def getGridPosition():
    # Snapping mouse cursor to the grid
    mouseX, mouseY = pygame.mouse.get_pos()
    gridX = math.floor(mouseX / cellSize) * cellSize
    gridY = math.floor(mouseY / cellSize) * cellSize
    return gridX, gridY # return grid position as a tuple

def drawCursor():
    # Get grid-snapped cursor position
    gridX, gridY = getGridPosition()

    cell = pygame.Rect( gridX-1, gridY-1, cellSize+3, cellSize+3 )
    if gridX >= 0 and gridX <= screen_width:
        if gridY >= 0 and gridY <= screen_height:
            pygame.draw.rect(screen, RED, cell, 2)

# Toggle grid cells for specified board. mouse argument expects -
#   returned tuple from getGridPosition()
def toggleCell( board, mouse,  ):
    x, y = mouse
    x = int(x / cellSize)
    y = int(y / cellSize)
    if board[y][x] == 1:
        board[y][x] = 0
    else:
        board[y][x] = 1

    return board

# Initialize Game of Life Board with a random state
board_state = random_state(round(screen_width/cellSize), round(screen_height/cellSize))
saved_state = save_state(board_state)


currentGeneration = 0   # Infinite iterations if <= 0
running = True

####################
# Main MyGame Loop #
####################
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # PAUSE and RESUME simulation
                if running:
                    running = False
                else:
                    running = True
            # Increase simulation speed
            if event.key == pygame.K_MINUS:
                if gameDelay > 0:
                    gameDelay -= 0.03125
                    print("Delay:", gameDelay)
            # Decrease speed
            if event.key == pygame.K_EQUALS:
                if gameDelay < 1:
                    gameDelay += 0.03125
                    print("Delay:", gameDelay)
            # Close simulation
            if event.key == pygame.K_q:
                pygame.quit()
                sys.exit()
        # If simulation is paused, accept mouse input
        if running == False:
            # Toggle cell
            if event.type == pygame.MOUSEBUTTONDOWN:
                # toggleCell(board_state, getGridPosition())
                mouseDown = True
            if event.type == pygame.MOUSEBUTTONUP:
                mouseDown = False
            # Handle key presses
            if event.type == pygame.KEYDOWN:
                # Clear the game board
                if event.key == pygame.K_c:
                    print("Board was cleared")
                    board_state = dead_state(
                        round(screen_width/cellSize),
                        round(screen_height/cellSize)
                    )
                # Save current board state
                if event.key == pygame.K_s:
                    print("Board state saved")
                    saved_state = save_state(board_state)
                # Restore saved board state
                if event.key == pygame.K_r:
                    print("Restored board from save")
                    board_state = saved_state
                # Load state from file
                if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    print("Saved board state to board<#>.dat")
                    save_to_file(board_state)

    if running:
        screen.fill(BLACK)
        render(board_state)

        if generations <= 0:
            # Run indefinitely
            board_state = next_board_state(board_state)
        else:
            board_state = next_board_state(board_state)
            currentGeneration += 1
        
        time.sleep( gameDelay )
    else:
        # When simulation is paused, allow editing of the board
        render(board_state)
        if mouseDown == True:
            # Compare current cursor position with previous to avoid repeadly toggling
            #   the same cell.
            if getGridPosition() != prevMousePosition:
                toggleCell(board_state, getGridPosition())
            prevMousePosition = getGridPosition()
        
        drawCursor()
    
    # Update the Screen
    pygame.display.flip()

    fpsClock.tick(fps)