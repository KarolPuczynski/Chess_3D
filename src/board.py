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
            if piece.moved != False:
                target = self.squares[row + piece.dir][col].piece
                if target is None:
                    piece.moves.append((row + piece.dir, col))
            else:
                target1 = self.squares[row + piece.dir][col].piece
                target2 = self.squares[row + 2 * piece.dir][col].piece
                if target2 is None and target1 is None:
                    piece.moves.append((row + piece.dir, col))
                    piece.moves.append((row + 2 * piece.dir, col))
                elif target1 is None:
                    piece.moves.append((row + piece.dir, col))

            # directions = [(piece.dir, 0), (2 * piece.dir, 0), (piece.dir, 1), (piece.dir, -1)]
            # for dy, dx in directions:
            #     y, x = row + dy, col + dx
            #     target = self.squares[y][x].piece
            #     if target is not None:
            #         if dx != 0:
            #             if target.color != piece.color:
            #                 piece.moves.append((y, x))
            #         elif dy == 2 * piece.dir and piece.moved == False:
            #             piece.moves.append((y, x))
            #         else:
            #             piece.moves.append((y, x))


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
                    target = self.squares[row_k][col_k].piece
                    if target is None:
                        piece.moves.append(moves)
                    else:
                        if target.color != piece.color:
                            piece.moves.append(moves)
            

        def bishop_moves():
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)] # Down left, Down right, Up left, Up right
            for dy, dx in directions:
                y, x = row + dy, col + dx
                while 0 <= y < ROWS and 0 <= x < COLS:
                    target = self.squares[y][x].piece
                    if target is None:
                        piece.moves.append((y, x))
                    else:
                        if target.color != piece.color:  
                            piece.moves.append((y, x))
                        break  
                    x += dx
                    y += dy            

        def rook_moves():
            directions = [(0, -1), (0, 1), (-1, 0), (1, 0)] # Left, Right, Up, Down
            for dy, dx in directions:
                y, x = row + dy, col + dx
                while 0 <= y < ROWS and 0 <= x < COLS:
                    target = self.squares[y][x].piece
                    if target is None:
                        piece.moves.append((y, x))
                    else:
                        if target.color != piece.color:
                            piece.moves.append((y, x))
                        break
                    x += dx
                    y += dy

        def queen_moves():
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1), (0, -1), (0, 1), (-1, 0), (1, 0)] # All possible directions for the queen
            for dy, dx in directions:
                y, x = row + dy, col + dx
                while 0 <= y < ROWS and 0 <= x < COLS:
                    target = self.squares[y][x].piece
                    if target is None:
                        piece.moves.append((y, x))
                    else:
                        if target.color != piece.color:
                            piece.moves.append((y, x))
                        break
                    x += dx
                    y += dy

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
                    target = self.squares[row_k][col_k].piece
                    if target is None:
                        piece.moves.append(moves)
                    else:
                        if target.color != piece.color:
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
        self.squares[row][col].piece.moved = True
        
                