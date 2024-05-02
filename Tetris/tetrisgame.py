import sys
import pygame
import gymnasium as gym
from gymnasium import spaces
import numpy as np
import tetris
from tetris import PlayGame


class TetrisEnv(gym.Env):

    def __init__(self, board, seed=None):
        super(TetrisEnv, self).__init__()
        self.board = np.array(board)  # Maze represented as a 2D numpy array
        self.num_rows, self.num_cols = self.board.shape

        # 9 possible actions: 0=soft_drop, 1=left, 2=right, 3=hard_drop, 4=rotate_left,
        # 5=rotate_left, 6=hold, 7=hold_left, 8=hold_right
        self.action_space = spaces.Discrete(9)

        # Observation space is grid of size:rows x columns
        self.observation_space = spaces.Box(
            low=0, high=255, shape=(220,), dtype=np.int64
        )

        self.lines_cleared = 0

        self.game = PlayGame(board, seed)
        self.info, _ = self.game.update(-1)

        # Initialize Pygame
        pygame.init()
        self.cell_size = 30

        # setting display size
        self.screen = pygame.display.set_mode(
            (
                (self.num_cols + 12) * self.cell_size + 2,
                self.num_rows * self.cell_size + 2,
            )
        )

    def reset(self, seed=None, options=None):
        self.game = PlayGame(np.zeros((21, 10)), seed)
        self.info, _ = self.game.update(-1)
        self.board = self.info["board"]
        obs = np.squeeze(np.clip(self.board, 0, 1).reshape(-1, 1))
        other_obs = [
            self.info["piece_num"],
            self.info["held"],
            self.info["row"],
            self.info["col"],
            self.info["rotation"],
        ] + self.info["bag"][:5]
        obs = np.append(obs, other_obs)
        obs = obs.astype(np.int64)
        return obs, {}

    def step(self, action):
        reward = 0
        done = False
        if action >= 1 and action <= 6:
            reward -= 1
        else:
            reward -= 2

        temp_lines = self.lines_cleared

        self.info, done = self.game.update(action)

        reward += 10 * self.lines_cleared - temp_lines

        if self.lines_cleared == 40:
            reward += 1000
            done = True

        self.board = self.info["board"]
        obs = np.squeeze(np.clip(self.board, 0, 1).reshape(-1, 1))
        other_obs = [
            self.info["piece_num"],
            self.info["held"],
            self.info["row"],
            self.info["col"],
            self.info["rotation"],
        ] + self.info["bag"][:5]
        obs = np.append(obs, other_obs)
        obs = obs.astype(np.int64)

        return obs, reward, done, {}

    def draw_piece(self, cell_left, cell_top, piece, color):
        shapes = {
            6: [(0, 0), (0, -1), (0, 1), (-1, 0)],
            2: [(0, 0), (0, -1), (-1, -1), (0, 1)],
            3: [(0, 0), (0, 1), (0, -1), (-1, 1)],
            7: [(0, 0), (-1, -1), (-1, 0), (0, 1)],
            5: [(0, 0), (0, -1), (-1, 0), (-1, 1)],
            1: [(0, 0), (0, -1), (0, 1), (0, 2)],
            4: [(0, 0), (-1, 0), (0, 1), (-1, 1)],
        }

        for r, c in shapes[piece]:
            pygame.draw.rect(
                self.screen,
                (128, 128, 128),
                (
                    cell_left + c * self.cell_size - 1,
                    cell_top + r * self.cell_size - 1,
                    self.cell_size + 1,
                    self.cell_size + 1,
                ),
            )
            pygame.draw.rect(
                self.screen,
                color,
                (
                    (cell_left + c * self.cell_size),
                    (cell_top + r * self.cell_size),
                    self.cell_size - 1,
                    self.cell_size - 1,
                ),
            )

    def render(self):
        # Clear the self.screen
        self.screen.fill((30, 30, 30))
        self.held = self.info["held"]
        cell_left = 2 * self.cell_size + 1
        cell_top = 3 * self.cell_size + 3
        if self.held == 1:  # I - Light Blue
            self.draw_piece(cell_left, cell_top, self.held, (0, 255, 255))
        elif self.held == 2:  # J - Dark Blue
            self.draw_piece(cell_left, cell_top, self.held, (0, 0, 255))
        elif self.held == 3:  # L - Orange
            self.draw_piece(cell_left, cell_top, self.held, (255, 165, 0))
        elif self.held == 4:  # O - Yellow
            self.draw_piece(cell_left, cell_top, self.held, (255, 255, 0))
        elif self.held == 5:  # S - Green
            self.draw_piece(cell_left, cell_top, self.held, (0, 255, 0))
        elif self.held == 6:  # T - Purple
            self.draw_piece(cell_left, cell_top, self.held, (160, 32, 240))
        elif self.held == 7:  # Z - Red
            self.draw_piece(cell_left, cell_top, self.held, (255, 0, 0))
        else:
            pygame.draw.rect(
                self.screen,
                (0, 0, 0),
                (cell_left, cell_top, self.cell_size - 1, self.cell_size - 1),
            )

        for i, p in enumerate(self.info["bag"][:5]):
            cell_left = (self.num_cols + 8) * self.cell_size + 1
            cell_top = 3 * (i + 1) * self.cell_size + 3
            if p == 1:  # I - Light Blue
                self.draw_piece(cell_left, cell_top, p, (0, 255, 255))
            elif p == 2:  # J - Dark Blue
                self.draw_piece(cell_left, cell_top, p, (0, 0, 255))
            elif p == 3:  # L - Orange
                self.draw_piece(cell_left, cell_top, p, (255, 165, 0))
            elif p == 4:  # O - Yellow
                self.draw_piece(cell_left, cell_top, p, (255, 255, 0))
            elif p == 5:  # S - Green
                self.draw_piece(cell_left, cell_top, p, (0, 255, 0))
            elif p == 6:  # T - Purple
                self.draw_piece(cell_left, cell_top, p, (160, 32, 240))
            elif p == 7:  # Z - Red
                self.draw_piece(cell_left, cell_top, p, (255, 0, 0))
            else:
                pygame.draw.rect(
                    self.screen,
                    (0, 0, 0),
                    (cell_left, cell_top, self.cell_size - 1, self.cell_size - 1),
                )

        for row in range(self.num_rows):
            for col in range(self.num_cols):
                cell_left = (col + 6) * self.cell_size + 1
                cell_top = row * self.cell_size + 3
                pygame.draw.rect(
                    self.screen,
                    (128, 128, 128),
                    (cell_left - 1, cell_top, self.cell_size + 1, self.cell_size),
                )
                if self.board[row][col] == 1:  # I - Light Blue
                    pygame.draw.rect(
                        self.screen,
                        (0, 255, 255),
                        (cell_left, cell_top, self.cell_size - 1, self.cell_size - 1),
                    )
                elif self.board[row][col] == 2:  # J - Dark Blue
                    pygame.draw.rect(
                        self.screen,
                        (0, 0, 255),
                        (cell_left, cell_top, self.cell_size - 1, self.cell_size - 1),
                    )
                elif self.board[row][col] == 3:  # L - Orange
                    pygame.draw.rect(
                        self.screen,
                        (255, 165, 0),
                        (cell_left, cell_top, self.cell_size - 1, self.cell_size - 1),
                    )
                elif self.board[row][col] == 4:  # O - Yellow
                    pygame.draw.rect(
                        self.screen,
                        (255, 255, 0),
                        (cell_left, cell_top, self.cell_size - 1, self.cell_size - 1),
                    )
                elif self.board[row][col] == 5:  # S - Green
                    pygame.draw.rect(
                        self.screen,
                        (0, 255, 0),
                        (cell_left, cell_top, self.cell_size - 1, self.cell_size - 1),
                    )
                elif self.board[row][col] == 6:  # T - Purple
                    pygame.draw.rect(
                        self.screen,
                        (160, 32, 240),
                        (cell_left, cell_top, self.cell_size - 1, self.cell_size - 1),
                    )
                elif self.board[row][col] == 7:  # Z - Red
                    pygame.draw.rect(
                        self.screen,
                        (255, 0, 0),
                        (cell_left, cell_top, self.cell_size - 1, self.cell_size - 1),
                    )
                else:
                    pygame.draw.rect(
                        self.screen,
                        (0, 0, 0),
                        (cell_left, cell_top, self.cell_size - 1, self.cell_size - 1),
                    )

        pygame.display.update()  # Update the display
