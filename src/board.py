import pygame
from const import *
from square import Square
from piece import *

class Board:
    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for cols in range(COLS)]
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')


    def _create(self):
        # Creating 64 objejcts of class Square
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col, None)

    def _add_pieces(self, color):
        row_pawn, row_other = (6, 7) if color == 'white' else (1, 0)

        # adding pawns (white or black)
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))
        # adding knights (white or black)
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))
        # adding bishops (white or black)
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))
        # adding rooks (white or black)
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))
        # adding queen (white or black)
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))
        # adding king (white or black)
        self.squares[row_other][4] = Square(row_other, 4, King(color))

    def calc_moves(self, row, col, piece):
        
        # Calculate all possible moves depending on selected piece

        def pawn_moves():
            if piece.moved:
                piece.moves.append((row + piece.dir, col))
            else:
                piece.moves.append((row + piece.dir, col))
                piece.moves.append((row + 2 * piece.dir, col))

        def knight_moves():
            possible_moves = [(row - 2, col - 1),
                              (row - 2, col + 1),
                              (row + 2, col - 1),
                              (row + 2, col + 1),
                              (row - 1, col - 2),
                              (row - 1, col + 2),
                              (row + 1, col - 2),
                              (row + 1, col + 2),]
            for moves in possible_moves:
                row_k, col_k = moves
                if row_k >= 0 and row_k < ROWS and col_k >= 0 and col_k < COLS:
                    piece.moves.append(moves)
            

        def bishop_moves():
            incr_left = col + 1
            incr_right = COLS - col 
            incr_up = row + 1
            incr_down = ROWS - row 
            possible_moves = [(row - i, col - i) for i in range(1, min(incr_left, incr_up))] + \
                             [(row - i, col + i) for i in range(1, min(incr_right, incr_up))] + \
                             [(row + i, col - i) for i in range(1, min(incr_left, incr_down))] + \
                             [(row + i, col + i) for i in range(1, min(incr_right, incr_down))]
            for moves in possible_moves:
                row_b, col_b = moves
                if row_b >= 0 and row_b < ROWS and col_b >= 0 and col_b < COLS:
                    piece.moves.append(moves)                

        def rook_moves():
            incr_left = col + 1
            incr_right = COLS - col 
            incr_up = row + 1
            incr_down = ROWS - row
            possible_moves = [(row - i, col) for i in range(1, incr_up)] + \
                             [(row + i, col) for i in range(1, incr_down)] + \
                             [(row, col - i) for i in range(1, incr_left)] + \
                             [(row, col + i) for i in range(1, incr_right)]
            for moves in possible_moves:
                row_r, col_r = moves
                if row_r >= 0 and row_r < ROWS and col_r >= 0 and col_r < COLS:
                    piece.moves.append(moves) 

        def queen_moves():
            incr_left = col + 1
            incr_right = COLS - col 
            incr_up = row + 1
            incr_down = ROWS - row 
            
            possible_moves = [(row - i, col - i) for i in range(1, min(incr_left, incr_up))] + \
                [(row - i, col + i) for i in range(1, min(incr_right, incr_up))] + \
                [(row + i, col - i) for i in range(1, min(incr_left, incr_down))] + \
                [(row + i, col + i) for i in range(1, min(incr_right, incr_down))] + \
                [(row - i, col) for i in range(1, incr_up)] + \
                [(row + i, col) for i in range(1, incr_down)] + \
                [(row, col - i) for i in range(1, incr_left)] + \
                [(row, col + i) for i in range(1, incr_right)]

            for moves in possible_moves:
                row_q, col_q = moves
                if row_q >= 0 and row_q < ROWS and col_q >= 0 and col_q < COLS:
                    piece.moves.append(moves)  

        def king_moves():
            possible_moves = [(row, col - 1),
                            (row, col + 1),
                            (row - 1, col),
                            (row + 1, col),
                            (row - 1, col - 1),
                            (row - 1, col + 1),
                            (row + 1, col - 1),
                            (row + 1, col + 1),]
            for moves in possible_moves:
                row_k, col_k = moves
                if row_k >= 0 and row_k < ROWS and col_k >= 0 and col_k < COLS:
                    piece.moves.append(moves)

        if isinstance(piece, Pawn):
            pawn_moves()
                
        if isinstance(piece, Knight):
            knight_moves()
                
        if isinstance(piece, Bishop):
            bishop_moves()
                
        if isinstance(piece, Rook):
            rook_moves()
                
        if isinstance(piece, Queen):
            queen_moves()
                
        if isinstance(piece, King):
            king_moves()



    def move(self, row, col, piece, color):
        self.squares[row][col].piece = piece
        self.squares[row][col].piece.moves = [] # Clear moves after moving the piece
        
                