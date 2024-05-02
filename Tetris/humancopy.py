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
held = None
bag = []

shapes = {
    6: [(0, 0), (0, -1), (0, 1), (-1, 0)],
    2: [(0, 0), (0, -1), (-1, -1), (0, 1)],
    3: [(0, 0), (0, 1), (0, -1), (-1, 1)],
    7: [(0, 0), (-1, -1), (-1, 0), (0, 1)],
    5: [(0, 0), (0, -1), (-1, 0), (-1, 1)],
    1: [(0, 0), (0, -1), (0, 1), (0, 2)],
    4: [(0, 0), (-1, 0), (0, 1), (-1, 1)],
}

# Initialize Pygame
pygame.init()

cell_size = 30

# Set up the display
screen = pygame.display.set_mode(
    ((num_cols + 12) * cell_size + 2, num_rows * cell_size + 2)
)


def draw_piece(cell_left, cell_top, piece, color):
    for r, c in shapes[piece]:
        pygame.draw.rect(
            screen,
            (128, 128, 128),
            (
                cell_left + c * cell_size - 1,
                cell_top + r * cell_size - 1,
                cell_size + 1,
                cell_size + 1,
            ),
        )
        pygame.draw.rect(
            screen,
            color,
            (
                (cell_left + c * cell_size),
                (cell_top + r * cell_size),
                cell_size - 1,
                cell_size - 1,
            ),
        )


def render():
    # Clear the screen
    screen.fill((30, 30, 30))
    p = held
    cell_left = 2 * cell_size + 1
    cell_top = 3 * cell_size + 3
    if p == 1:  # I - Light Blue
        draw_piece(cell_left, cell_top, p, (0, 255, 255))
    elif p == 2:  # J - Dark Blue
        draw_piece(cell_left, cell_top, p, (0, 0, 255))
    elif p == 3:  # L - Orange
        draw_piece(cell_left, cell_top, p, (255, 165, 0))
    elif p == 4:  # O - Yellow
        draw_piece(cell_left, cell_top, p, (255, 255, 0))
    elif p == 5:  # S - Green
        draw_piece(cell_left, cell_top, p, (0, 255, 0))
    elif p == 6:  # T - Purple
        draw_piece(cell_left, cell_top, p, (160, 32, 240))
    elif p == 7:  # Z - Red
        draw_piece(cell_left, cell_top, p, (255, 0, 0))
    else:
        pygame.draw.rect(
            screen,
            (0, 0, 0),
            (cell_left, cell_top, cell_size - 1, cell_size - 1),
        )

    for i, p in enumerate(bag[:5]):
        cell_left = (num_cols + 8) * cell_size + 1
        cell_top = 3 * (i + 1) * cell_size + 3
        if p == 1:  # I - Light Blue
            draw_piece(cell_left, cell_top, p, (0, 255, 255))
        elif p == 2:  # J - Dark Blue
            draw_piece(cell_left, cell_top, p, (0, 0, 255))
        elif p == 3:  # L - Orange
            draw_piece(cell_left, cell_top, p, (255, 165, 0))
        elif p == 4:  # O - Yellow
            draw_piece(cell_left, cell_top, p, (255, 255, 0))
        elif p == 5:  # S - Green
            draw_piece(cell_left, cell_top, p, (0, 255, 0))
        elif p == 6:  # T - Purple
            draw_piece(cell_left, cell_top, p, (160, 32, 240))
        elif p == 7:  # Z - Red
            draw_piece(cell_left, cell_top, p, (255, 0, 0))
        else:
            pygame.draw.rect(
                screen,
                (0, 0, 0),
                (cell_left, cell_top, cell_size - 1, cell_size - 1),
            )

    for row in range(num_rows):
        for col in range(num_cols):
            cell_left = (col + 6) * cell_size + 1
            cell_top = row * cell_size + 3
            pygame.draw.rect(
                screen,
                (128, 128, 128),
                (cell_left - 1, cell_top, cell_size + 1, cell_size),
            )
            if board[row][col] == 1:  # I - Light Blue
                pygame.draw.rect(
                    screen,
                    (0, 255, 255),
                    (cell_left, cell_top, cell_size - 1, cell_size - 1),
                )
            elif board[row][col] == 2:  # J - Dark Blue
                pygame.draw.rect(
                    screen,
                    (0, 0, 255),
                    (cell_left, cell_top, cell_size - 1, cell_size - 1),
                )
            elif board[row][col] == 3:  # L - Orange
                pygame.draw.rect(
                    screen,
                    (255, 165, 0),
                    (cell_left, cell_top, cell_size - 1, cell_size - 1),
                )
            elif board[row][col] == 4:  # O - Yellow
                pygame.draw.rect(
                    screen,
                    (255, 255, 0),
                    (cell_left, cell_top, cell_size - 1, cell_size - 1),
                )
            elif board[row][col] == 5:  # S - Green
                pygame.draw.rect(
                    screen,
                    (0, 255, 0),
                    (cell_left, cell_top, cell_size - 1, cell_size - 1),
                )
            elif board[row][col] == 6:  # T - Purple
                pygame.draw.rect(
                    screen,
                    (160, 32, 240),
                    (cell_left, cell_top, cell_size - 1, cell_size - 1),
                )
            elif board[row][col] == 7:  # Z - Red
                pygame.draw.rect(
                    screen,
                    (255, 0, 0),
                    (cell_left, cell_top, cell_size - 1, cell_size - 1),
                )
            else:
                pygame.draw.rect(
                    screen,
                    (0, 0, 0),
                    (cell_left, cell_top, cell_size - 1, cell_size - 1),
                )

    pygame.display.update()  # Update the display


# Main game loop
running = True
game.update(-1)
t = 0
temp = ""
while running:
    if t % 100 == 0:
        info, done = game.update(0)
    t += 1

    keys = pygame.key.get_pressed()

    if keys[pygame.K_DOWN]:
        info, done = game.update(0)
        pygame.time.wait(12)

    for event in pygame.event.get():
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
            elif event.key == pygame.K_c:
                action = 6
            if event.key == pygame.K_r:
                board = array_zeros = np.zeros((21, 10))
                num_rows, num_cols = board.shape

                game = PlayGame()
                info, done = game.update(-1)

            else:
                info, done = game.update(action)

    piece = info["piece_num"]
    board = info["board"]
    bag = info["bag"]
    held = info["held"]

    if not temp == piece:
        t = 1
    temp = piece
    if done:
        pygame.quit()
        sys.exit()

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
