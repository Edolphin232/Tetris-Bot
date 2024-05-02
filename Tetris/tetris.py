import numpy as np
import random

shapes = {
    6: [(0, 0), (0, -1), (0, 1), (-1, 0)],
    2: [(0, 0), (0, -1), (-1, -1), (0, 1)],
    3: [(0, 0), (0, 1), (0, -1), (-1, 1)],
    7: [(0, 0), (-1, -1), (-1, 0), (0, 1)],
    5: [(0, 0), (0, -1), (-1, 0), (-1, 1)],
    1: [(0, 0), (0, -1), (0, 1), (0, 2)],
    4: [(0, 0), (-1, 0), (0, 1), (-1, 1)],
}

pieces = [1, 2, 3, 4, 5, 6, 7]


class PlayGame:
    def __init__(self):
        self.info = {
            "board": np.zeros((21, 10)),
            "bag": [],
            "piece": [],
            "row": 1,
            "col": 4,
            "rotation": 0,
            "piece_num": 0,
            "held": 0,
            "can_hold": True,
            "lines_cleared": 0,
        }
        new_pieces = pieces.copy()
        random.shuffle(new_pieces)
        self.info["bag"] += new_pieces
        self.info["piece_num"] = self.info["bag"][0]
        self.info["piece"] = shapes.get(self.info["bag"][0])
        self.info["bag"].remove(self.info["bag"][0])

    def gen_new_piece(self):
        if self.info["board"][1][4] != 0:
            return True
        if len(self.info["bag"]) < 7:
            new_pieces = pieces.copy()
            random.shuffle(new_pieces)
            self.info["bag"] += new_pieces
        self.info["piece_num"] = self.info["bag"][0]
        self.info["piece"] = shapes.get(self.info["bag"][0])
        self.info["bag"].remove(self.info["bag"][0])
        self.info["row"] = 1
        self.info["col"] = 4
        self.info["rotation"] = 0
        self.info["can_hold"] = True

        for row, col in self.info["piece"]:

            self.info["board"][self.info["row"] + row][self.info["col"] + col] = (
                self.info["piece_num"]
            )

        return False

    def update(self, action):
        if self.info["piece_num"] == 0:
            if self.info["board"][1][4] != 0:
                return (self.info, True)
            else:
                self.gen_new_piece()
                self.info["can_hold"] = True

        if action == 0:  # Soft Drop
            self.info["board"], self.info["row"], settled = self.soft_drop(
                self.info["board"],
                self.info["piece"],
                self.info["row"],
                self.info["col"],
                self.info["piece_num"],
            )
            if settled:
                self.info["piece_num"] = 0
                self.info["board"] = self.clear_lines(self.info["board"])
                self.info["can_hold"] = True
                return (self.info, self.gen_new_piece())
        elif action == 1:  # Left
            self.info["board"], self.info["col"] = self.left(
                self.info["board"],
                self.info["piece"],
                self.info["row"],
                self.info["col"],
                self.info["piece_num"],
            )

        elif action == 2:  # Right
            self.info["board"], self.info["col"] = self.right(
                self.info["board"],
                self.info["piece"],
                self.info["row"],
                self.info["col"],
                self.info["piece_num"],
            )

        elif action == 3:  # Hard Drop
            settled = False
            while not settled:
                self.info["board"], self.info["row"], settled = self.soft_drop(
                    self.info["board"],
                    self.info["piece"],
                    self.info["row"],
                    self.info["col"],
                    self.info["piece_num"],
                )
            self.info["piece_num"] = 0
            self.info["board"] = self.clear_lines(self.info["board"])
            self.info["can_hold"] = True
            return (self.info, self.gen_new_piece())

        elif action == 4:  # Left Spin
            (
                self.info["board"],
                self.info["row"],
                self.info["col"],
                self.info["rotation"],
                self.info["piece"],
            ) = self.left_spin(
                self.info["board"],
                self.info["piece"],
                self.info["rotation"],
                self.info["row"],
                self.info["col"],
                self.info["piece_num"],
            )

        elif action == 5:  # Right Spin
            (
                self.info["board"],
                self.info["row"],
                self.info["col"],
                self.info["rotation"],
                self.info["piece"],
            ) = self.right_spin(
                self.info["board"],
                self.info["piece"],
                self.info["rotation"],
                self.info["row"],
                self.info["col"],
                self.info["piece_num"],
            )

        elif action == 6:  # Hold
            if self.info["can_hold"]:
                if self.info["held"] == 0:
                    for r, c in self.info["piece"]:
                        self.info["board"][self.info["row"] + r][
                            self.info["col"] + c
                        ] = 0

                    self.info["held"] = self.info["piece_num"]
                    self.gen_new_piece()
                else:
                    for r, c in self.info["piece"]:
                        self.info["board"][self.info["row"] + r][
                            self.info["col"] + c
                        ] = 0
                    temp = self.info["held"]
                    self.info["held"] = self.info["piece_num"]
                    self.info["piece_num"] = temp
                    self.info["col"] = 4
                    self.info["row"] = 1
                    self.info["rotation"] = 0
                    self.info["piece"] = shapes.get(self.info["piece_num"])

                    for row, col in self.info["piece"]:

                        self.info["board"][self.info["row"] + row][
                            self.info["col"] + col
                        ] = self.info["piece_num"]

                self.info["can_hold"] = False
        elif action == 7:  # Hold Left
            temp_col = self.info["col"] + 1
            while temp_col != self.info["col"]:
                temp_col = self.info["col"]
                self.info["board"], self.info["col"] = self.left(
                    self.info["board"],
                    self.info["piece"],
                    self.info["row"],
                    self.info["col"],
                    self.info["piece_num"],
                )
        elif action == 8:  # Hold Right
            temp_col = self.info["col"] - 1
            while temp_col != self.info["col"]:
                temp_col = self.info["col"]
                self.info["board"], self.info["col"] = self.right(
                    self.info["board"],
                    self.info["piece"],
                    self.info["row"],
                    self.info["col"],
                    self.info["piece_num"],
                )
        return (self.info, False)

    def clear_lines(self, board):
        rows, cols = 21, 10

        # A list to store the indices of the rows to be cleared
        rows_to_clear = []

        # Identify all the full rows
        for row in range(rows):
            if all(board[row, col] != 0 for col in range(cols)):
                rows_to_clear.append(row)

        # Clear the rows and count the number of cleared rows
        for row in rows_to_clear:
            # Shift down rows above the current row
            for r in reversed(range(0, row + 1)):
                board[r] = board[r - 1]
            board[0] = np.zeros(cols)  # Reset the top row
            self.info["lines_cleared"] += 1

        return board

    # Returns true if piece can update
    def check_update(self, board, old_piece, new_piece, piece_name):
        # Erases current piece
        for r, c in old_piece:
            board[r][c] = 0
        # Checks for collision with new piece, rewrites old piece if collision
        for row, col in new_piece:
            if col < 0 or col > 9 or row > 20 or row < 0 or board[row][col] != 0:
                for r, c in old_piece:
                    board[r][c] = piece_name
                return False

        # Writes in new piece if no collision
        for r, c in new_piece:
            board[r][c] = piece_name
        return True

    def left_spin(self, board, piece, rotation, row, col, piece_name):
        rot_list = self.get_wall_kick("left", piece_name, rotation)
        # rot_list = [(0,0)]
        if piece_name == 4:
            return board, row, col, rotation, piece
        old_piece = [(row + r, col + c) for r, c in piece]
        for s_c, s_r in rot_list:
            new_piece = [(row - c + s_r, col + r + s_c) for r, c in piece]
            if self.check_update(board, old_piece, new_piece, piece_name):
                return (
                    board,
                    row + s_r,
                    col + s_c,
                    (rotation - 1) % 4,
                    [(-c, r) for r, c in piece],
                )
        return board, row, col, rotation, piece

    def right_spin(self, board, piece, rotation, row, col, piece_name):
        rot_list = self.get_wall_kick("right", piece_name, rotation)
        if piece_name == 4:
            return board, row, col, rotation, piece
        old_piece = [(row + r, col + c) for r, c in piece]
        for s_c, s_r in rot_list:
            new_piece = [(row + c + s_r, col - r + s_c) for r, c in piece]
            if self.check_update(board, old_piece, new_piece, piece_name):
                return (
                    board,
                    row + s_r,
                    col + s_c,
                    (rotation + 1) % 4,
                    [(c, -r) for r, c in piece],
                )
        return board, row, col, rotation, piece

    def left(self, board, piece, row, col, piece_name):
        new_piece = [(row + r, col + c - 1) for r, c in piece]
        old_piece = [(row + r, col + c) for r, c in piece]

        if self.check_update(board, old_piece, new_piece, piece_name):
            return board, col - 1
        else:
            return board, col

    def right(self, board, piece, row, col, piece_name):
        new_piece = [(row + r, col + c + 1) for r, c in piece]
        old_piece = [(row + r, col + c) for r, c in piece]

        if self.check_update(board, old_piece, new_piece, piece_name):
            return board, col + 1
        else:
            return board, col

    def soft_drop(self, board, piece, row, col, piece_name):
        new_piece = [(row + r + 1, col + c) for r, c in piece]
        old_piece = [(row + r, col + c) for r, c in piece]

        if self.check_update(board, old_piece, new_piece, piece_name):
            return board, row + 1, False
        else:
            return board, row, True

    def get_wall_kick(self, rotation, piece, state):
        if piece == 1:
            if rotation == "right":
                if state == 0:
                    return [(0, 0), (-2, 0), (1, 0), (-2, -1), (1, 2)]
                if state == 1:
                    return [(0, 0), (-1, 0), (2, 0), (-1, 2), (2, -1)]
                if state == 2:
                    return [(0, 0), (2, 0), (-1, 0), (2, 1), (-1, -2)]
                if state == 3:
                    return [(0, 0), (1, 0), (-2, 0), (1, -2), (-2, 1)]
            elif rotation == "left":
                if state == 0:
                    return [(0, 0), (2, 0), (-1, 0), (2, 1), (-1, -2)]
                if state == 1:
                    return [(0, 0), (1, 0), (-2, 0), (1, -2), (-2, 1)]
                if state == 2:
                    return [(0, 0), (-2, 0), (1, 0), (-2, -1), (1, 2)]
                if state == 3:
                    return [(0, 0), (-1, 0), (2, 0), (-1, 2), (2, -1)]
        elif piece == 4:
            return [(0, 0)]
        else:
            if rotation == "right":
                if state == 0:
                    return [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)]
                if state == 1:
                    return [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)]
                if state == 2:
                    return [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)]
                if state == 3:
                    return [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)]
            elif rotation == "left":
                if state == 0:
                    return [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)]
                if state == 1:
                    return [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)]
                if state == 2:
                    return [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)]
                if state == 3:
                    return [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)]
