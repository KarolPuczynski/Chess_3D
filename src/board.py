import pygame
from const import *
from square import Square
from piece import *
import copy

class Board:
    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for cols in range(COLS)]
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')
        self.white_king_position = (7, 4)
        self.black_king_position = (0, 4)


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

    def move(self, last_row, last_col, row, col, piece, color):        
        self.squares[last_row][last_col].piece = None
        self.squares[row][col].piece = piece
        # if isinstance(piece, King):
        #     if color == 'white':
        #         self.white_king_position = (row, col)
        #     else:
        #         self.black_king_position = (row, col)
        # self.in_check() 
        self.squares[row][col].piece.moves = []                                                    # Clear moves after moving the piece
        self.squares[row][col].piece.moved = True

    def in_check(self, curr_row, curr_col, possible_row, possible_col, piece):
        temp_piece = copy.deepcopy(piece)
        temp_board = copy.deepcopy(self)

        temp_board.move(curr_row, curr_col, possible_row, possible_col, temp_piece, piece.color)

        for r in range(ROWS):
            for c in range(COLS):
                p = temp_board.squares[r][c].piece
                if p is not None and p.color != piece.color:
                    temp_board.calc_moves(r, c, p, bool=False)
                    for move in p.moves:
                        if isinstance(temp_board.squares[move[0]][move[1]].piece, King):
                            return True
        return False
    
    def is_checkmate(self, color):
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.squares[row][col].piece
                if piece is not None and piece.color == color:
                    self.calc_moves(row, col, piece)
                    if piece.moves:
                        return False  

        king_position = None
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.squares[row][col].piece
                if isinstance(piece, King) and piece.color == color:
                    king_position = (row, col)
                    break

        if king_position:
            king_row, king_col = king_position
            king = self.squares[king_row][king_col].piece
            self.calc_moves(king_row, king_col, king)
            if not king.moves:
                return self.in_check(king_row, king_col, king_row, king_col, king)

        return False 
     
    def calc_moves(self, row, col, piece, bool=True):
        
        # Calculate all possible moves depending on selected piece

        def pawn_moves():
            directions = [(piece.dir, 0), (2 * piece.dir, 0), (piece.dir, 1), (piece.dir, -1)]
            for dy, dx in directions:
                y, x = row + dy, col + dx
                if 0 <= x < COLS and 0 <= y < ROWS:
                    target = self.squares[y][x].piece

                    if dx != 0 and target is not None:                                             # Capturing diagonally
                        if target.color != piece.color:
                            if bool:
                                if not self.in_check(row, col, y, x, piece): 
                                    piece.moves.append((y, x))
                            else:
                                piece.moves.append((y, x))

                    elif dy == 2 * piece.dir and piece.moved == False:                             # Moving pawn two squares forward
                        if target is None and self.squares[y - piece.dir][x].piece is None:
                            if bool:
                                if not self.in_check(row, col, y, x, piece): 
                                    piece.moves.append((y, x))
                            else:
                                piece.moves.append((y, x))

                    elif dx == 0 and dy == piece.dir and target is None:                           # Moving pawn one square forward 
                        if bool:
                            if not self.in_check(row, col, y, x, piece): 
                                piece.moves.append((y, x))
                        else:
                            piece.moves.append((y, x))

        def knight_moves():
            possible_moves = [(row - 2, col - 1),                                                  # All possible moves for the knight
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
                    target = self.squares[row_k][col_k].piece
                    if target is None or target.color != piece.color:  
                        if bool:
                            if not self.in_check(row, col, row_k, col_k, piece): 
                                piece.moves.append(moves)
                        else:
                            piece.moves.append(moves)

        def moves_appending(directions, row, col, piece):
            for dy, dx in directions:
                y, x = row + dy, col + dx
                while 0 <= y < ROWS and 0 <= x < COLS:
                    target = self.squares[y][x].piece
                    if target is None:
                        if bool:
                            if not self.in_check(row, col, y, x, piece): 
                                piece.moves.append((y, x))
                        else:
                            piece.moves.append((y, x))
                    else:
                        if target.color != piece.color:  
                            if bool:
                                if not self.in_check(row, col, y, x, piece): 
                                    piece.moves.append((y, x))
                            else:
                                piece.moves.append((y, x))
                        break  
                    x += dx
                    y += dy     

        def king_moves():   
            possible_moves = [(row, col - 1),                                                      # All possible moves for the king                                       
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
                    target = self.squares[row_k][col_k].piece
                    if target is None:
                        if bool:
                            if not self.in_check(row, col, row_k, col_k, piece): 
                                piece.moves.append(moves)
                        else:
                            piece.moves.append(moves)
                    else:
                        if target.color != piece.color:
                            if bool:
                                if not self.in_check(row, col, row_k, col_k, piece): 
                                    piece.moves.append(moves)
                            else:
                                piece.moves.append(moves)

        piece.moves = []  # Clear previous moves

        if isinstance(piece, Pawn):
            pawn_moves()
                
        if isinstance(piece, Knight):
            knight_moves()
                
        if isinstance(piece, Bishop):
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]                                                
            moves_appending(directions, row, col, piece) 
                
        if isinstance(piece, Rook):
            directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]                                        
            moves_appending(directions, row, col, piece) 
                
        if isinstance(piece, Queen):
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1), (0, -1), (0, 1), (-1, 0), (1, 0)]    
            moves_appending(directions, row, col, piece)
                
        if isinstance(piece, King):
            king_moves()

        
                