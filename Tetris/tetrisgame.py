import sys
import pygame
import gymnasium as gym
from gym import spaces
import numpy as np
import tetris
from tetris import PlayGame

class TetrisEnv(gym.Env):

    def __init__(self, board):
        super(TetrisEnv, self).__init__()
        self.board = np.array(board)  # Maze represented as a 2D numpy array
        self.num_rows, self.num_cols = self.board.shape

        # 6 possible actions: 0=soft_drop, 1=left, 2=right, 3=hard_drop, 4=rotate_left, 5=rotate_left
        self.action_space = spaces.Discrete(6)  

        # Observation space is grid of size:rows x columns
        self.observation_space = spaces.Box(low=0, high=1, shape=(21, 10), dtype=np.int8)

        self.lines_cleared = 0

        self.game = PlayGame()
        self.piece_row = 1
        self.piece_col = 4
        self.piece_rot = 0
        self.piece = None
        self.piece_name = None
        self.bag = []

        # Initialize Pygame
        pygame.init()
        self.cell_size = 30

        # setting display size
        self.screen = pygame.display.set_mode((self.num_cols * self.cell_size + 2, self.num_rows * self.cell_size + 2))

    def reset(self):
        self.piece_row = 1
        self.piece_col = 4
        self.piece_rot = 0
        self.piece = None
        self.board = np.zeros((21,10))
        return self.board

    def step(self, action):
        reward = 0
        done = False


        self.board, self.piece, self.bag, done = self.game.update(self.board, action)
        

        if self.lines_cleared == 40:
            done = True

        obs = np.flatten(np.clip(self.board, 0, 1))
        
        reward -= 1
        return obs, reward, done, {}

    

    def render(self):
        # Clear the screen
        self.screen.fill((128, 128, 128))  
        
        # Draw env elements one cell at a time
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                cell_left = col * self.cell_size + 1
                cell_top = row * self.cell_size + 3
                
                if self.board[row][col] == 1: # I - Light Blue 
                    pygame.draw.rect(self.screen, (0, 255, 255), (cell_left+1, cell_top-1, self.cell_size-2, self.cell_size-2))
                elif self.board[row][col] == 2: # J - Dark Blue
                    pygame.draw.rect(self.screen, (0, 0, 255), (cell_left+1, cell_top-1, self.cell_size-2, self.cell_size-2))
                elif self.board[row][col] == 3: # L - Orange
                    pygame.draw.rect(self.screen, (255, 165, 0), (cell_left+1, cell_top-1, self.cell_size-2, self.cell_size-2))
                elif self.board[row][col] == 4: # O - Yellow
                    pygame.draw.rect(self.screen, (255, 255, 0), (cell_left+1, cell_top-1, self.cell_size-2, self.cell_size-2))
                elif self.board[row][col] == 5: # S - Green
                    pygame.draw.rect(self.screen, (0, 255, 0), (cell_left+1, cell_top-1, self.cell_size-2, self.cell_size-2))
                elif self.board[row][col] == 6: # T - Purple
                    pygame.draw.rect(self.screen, (160, 32, 240), (cell_left+1, cell_top-1, self.cell_size-2, self.cell_size-2))
                elif self.board[row][col] == 7: # Z - Red
                    pygame.draw.rect(self.screen, (255, 0, 0), (cell_left+1, cell_top-1, self.cell_size-2, self.cell_size-2))
                else:
                    pygame.draw.rect(self.screen, (0, 0, 0), (cell_left+1, cell_top-1, self.cell_size-2, self.cell_size-2))

        pygame.display.update()  # Update the display