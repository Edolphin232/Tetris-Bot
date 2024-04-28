import numpy as np
import random

shapes = {
    "T": [(0, 0), (0, -1), (0, 1), (-1, 0)],
    "J": [(0, 0), (0, -1), (-1, -1), (0, 1)],
    "L": [(0, 0), (0, 1), (0, -1), (-1, 1)],
    "Z": [(0, 0), (-1, -1), (-1, 0), (0, 1)],
    "S": [(0, 0), (0, -1), (-1, 0), (-1, 1)],
    "I": [(0, 0), (0, -1), (0, 1), (0, 2)],
    "O": [(0, 0), (-1, 0), (0, 1), (-1, 1)],
}



piece_nums = {
        "T": 6,
        "J": 2,
        "L": 3,
        "Z": 7,
        "S": 5,
        "I": 1,
        "O": 4,
}

pieces = ['T', 'J', 'L', 'Z', 'S', 'I', 'O']

class PlayGame:
    def __init__(self):
        self.bag = []
        self.piece = None
        self.piece_row = 1
        self.piece_col = 4
        self.piece_rot = 0
        self.piece_name = None
        

    def get_pieces():
        return 

    def update(self, board, action):
        if self.piece_name == None:
            if board[1][4] != 0:
                return board, True
                
            else:
                if len(self.bag) == 0:
                    self.bag = pieces.copy()
                self.piece_name = random.choice(self.bag)
                self.bag.remove(self.piece_name)
                self.piece_col = 4
                self.piece_row = 1
                self.piece_rot = 0
                self.piece = shapes.get(self.piece_name)
        
    
        for row, col in self.piece:

            board[self.piece_row + row][self.piece_col + col] = piece_nums[self.piece_name]

        if action == 0: # Soft Drop
            board, self.piece_row, settled = self.soft_drop(board, self.piece, self.piece_row, self.piece_col, self.piece_name)
            if settled:
                self.piece_name = None
                board, cleared = self.clear_lines(board)
                return board, False
        elif action == 1: # Left
            board, self.piece_col = self.left(board, self.piece, self.piece_row, self.piece_col, self.piece_name)

        elif action == 2: # Right
            board, self.piece_col = self.right(board, self.piece, self.piece_row, self.piece_col, self.piece_name)

        elif action == 3: # Hard Drop
            settled = False
            while not settled:
                board, self.piece_row, settled = self.soft_drop(board, self.piece, self.piece_row, self.piece_col, self.piece_name)
            self.piece_name = None
            board, cleared = self.clear_lines(board)
            return board, False
        
        elif action == 4: # Left Spin
            board, self.piece_row, self.piece_col, self.piece_rot, self.piece = self.left_spin(
                board, self.piece, self.piece_rot, self.piece_row, self.piece_col, self.piece_name)
            
        elif action == 5: # Right Spin
            board, self.piece_row, self.piece_col, self.piece_rot, self.piece = self.right_spin(
                board, self.piece, self.piece_rot, self.piece_row, self.piece_col, self.piece_name)

        board, cleared = self.clear_lines(board)
        return board, False
    
    def clear_lines(self, board):
        rows, cols = board.shape
        cleared = 0

        # A list to store the indices of the rows to be cleared
        rows_to_clear = []

        # Identify all the full rows
        for row in range(rows):
            if all(board[row, col] != 0 for col in range(cols)):
                rows_to_clear.append(row)

        # Clear the rows and count the number of cleared rows
        for row in rows_to_clear:
            # Shift down rows above the current row
            for r in range(row - cleared, 0, -1):
                board[r] = board[r - 1]
            board[0] = np.zeros(cols)  # Reset the top row
            cleared += 1
            
        return board, cleared
    
    # Returns true if piece can update
    def check_update(self, board, old_piece, new_piece, piece_name):
        #Erases current piece
        for r, c in old_piece:
            board[r][c] = 0
        #Checks for collision with new piece, rewrites old piece if collision
        for row, col in new_piece:
            if col < 0 or col > 9 or row > 20 or row < 0 or board[row][col] != 0:
                for r, c in old_piece:
                    board[r][c] = piece_nums[piece_name]
                return False

        # Writes in new piece if no collision
        for r, c in new_piece:
            board[r][c] = piece_nums[piece_name]
        return True
    
    def left_spin(self, board, piece, rotation, row, col, piece_name):
        rot_list = self.get_wall_kick('left', piece_name, rotation)
        # rot_list = [(0,0)]
        if piece_name == 'O':
            return board, row, col, rotation, piece
        old_piece = [(row+r, col+c) for r,c in piece]
        for s_r, s_c in rot_list:
            new_piece = [(row-c+s_r, col+r+s_c) for r,c in piece]
            if self.check_update(board, old_piece, new_piece, piece_name):
                return board, row+s_r, col+s_c, (rotation-1)%4, [(-c, r) for r, c in piece]
        return board, row, col, rotation, piece
    
    def right_spin(self, board, piece, rotation, row, col, piece_name):
        rot_list = self.get_wall_kick('right', piece_name, rotation)
        if piece_name == 'O':
            return board, row, col, rotation, piece
        old_piece = [(row+r, col+c) for r,c in piece]
        for s_r, s_c in rot_list:
            new_piece = [(row+c+s_r, col-r+s_c) for r,c in piece]
            if self.check_update(board, old_piece, new_piece, piece_name):
                return board, row+s_r, col+s_c, (rotation-1)%4, [(c, -r) for r, c in piece]
        return board, row, col, rotation, piece
        
    def left(self, board, piece, row, col, piece_name):
        new_piece = [(row+r, col+c-1) for r,c in piece]
        old_piece = [(row+r, col+c) for r,c in piece]
        
        if self.check_update(board, old_piece, new_piece, piece_name):
            return board, col-1
        else:
            return board, col
        
    def right(self, board, piece, row, col, piece_name):
        new_piece = [(row+r, col+c+1) for r,c in piece]
        old_piece = [(row+r, col+c) for r,c in piece]
        
        if self.check_update(board, old_piece, new_piece, piece_name):
            return board, col+1
        else:
            return board, col  
    
    def soft_drop(self, board, piece, row, col, piece_name):
        new_piece = [(row+r+1, col+c) for r,c in piece]
        old_piece = [(row+r, col+c) for r,c in piece]
        
        if self.check_update(board, old_piece, new_piece, piece_name):
            return board, row+1, False
        else:
            return board, row, True

    
    def get_wall_kick(self, rotation, piece, state):
        if piece == "I":
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
        elif piece == "O":
            return [(0,0)]
        else:
            if rotation == "right":
                if state == 0:
                    return [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)]
                if state == 1:
                    return [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)]
                if state == 2:
                    return [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)]
                if state == 3:
                    return [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)]
            elif rotation == "left":
                if state == 0:
                    return [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)]
                if state == 1:
                    return [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)]
                if state == 2:
                    return [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)]
                if state == 3:
                    return [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)]


    