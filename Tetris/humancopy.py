import pygame
import sys
import numpy as np
from tetris import PlayGame

board = array_zeros = np.zeros((21, 10))
num_rows, num_cols = board.shape

game = PlayGame()
piece_row = 1
piece_col = 4
piece_rot = 0
piece = None
piece_name = None

# Initialize Pygame
pygame.init()

cell_size = 30

# Set up the display
screen = pygame.display.set_mode((num_cols * cell_size + 2,num_rows * cell_size + 2))

# Initialize your Tetris game logic
game = PlayGame()

def render():
        # Clear the screen
        screen.fill((128, 128, 128))  
        
        # Draw env elements one cell at a time
        for row in range(num_rows):
            for col in range(num_cols):
                cell_left = col * cell_size + 1
                cell_top = row * cell_size + 3
                
                if board[row][col] == 1: # I - Light Blue 
                    pygame.draw.rect(screen, (0, 255, 255), (cell_left+1, cell_top-1, cell_size-2,cell_size-2))
                elif board[row][col] == 2: # J - Dark Blue
                    pygame.draw.rect(screen, (0, 0, 255), (cell_left+1, cell_top-1, cell_size-2,cell_size-2))
                elif board[row][col] == 3: # L - Orange
                    pygame.draw.rect(screen, (255, 165, 0), (cell_left+1, cell_top-1, cell_size-2,cell_size-2))
                elif board[row][col] == 4: # O - Yellow
                    pygame.draw.rect(screen, (255, 255, 0), (cell_left+1, cell_top-1, cell_size-2,cell_size-2))
                elif board[row][col] == 5: # S - Green
                    pygame.draw.rect(screen, (0, 255, 0), (cell_left+1, cell_top-1, cell_size-2,cell_size-2))
                elif board[row][col] == 6: # T - Purple
                    pygame.draw.rect(screen, (160, 32, 240),(cell_left+1, cell_top-1, cell_size-2,cell_size-2))
                elif board[row][col] == 7: # Z - Red
                    pygame.draw.rect(screen, (255, 0, 0), (cell_left+1, cell_top-1, cell_size-2,cell_size-2))
                else:
                    pygame.draw.rect(screen, (0, 0, 0), (cell_left+1, cell_top-1, cell_size-2,cell_size-2))

        pygame.display.update()  # Update the display

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        action = 0
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                action = 1
            elif event.key == pygame.K_RIGHT:
                action = 2
            elif event.key == pygame.K_DOWN:
                action = 0
            elif event.key == pygame.K_SPACE:
                action = 3
            elif event.key == pygame.K_z:
                action = 4
            elif event.key == pygame.K_UP:
                action = 5
        
        game.update(board, action)

    # Render the current game state
    screen.fill((0, 0, 0))  # Clear the screen with black
    render()  # Adjust this call to match your render function's signature

    # Update the display
    pygame.display.flip()

    # Control the game speed
    pygame.time.Clock().tick(100)



# Quit Pygame
pygame.quit()
sys.exit()