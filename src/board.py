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
        self.move_history = []
        self.redo_stack = []

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
            self.squares[row_pawn][col].piece.position = (row_pawn, col)
        
        # adding knights (white or black)
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][1].piece.position = (row_other, 1)

        self.squares[row_other][6] = Square(row_other, 6, Knight(color))
        self.squares[row_other][6].piece.position = (row_other, 6)
        
        # adding bishops (white or black)
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][2].piece.position = (row_other, 2)

        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))
        self.squares[row_other][5].piece.position = (row_other, 5)
        
        # adding rooks (white or black)
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][0].piece.position = (row_other, 0)

        self.squares[row_other][7] = Square(row_other, 7, Rook(color))
        self.squares[row_other][7].piece.position = (row_other, 7)
        
        # adding queen (white or black)
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))
        self.squares[row_other][3].piece.position = (row_other, 3)

        # adding king (white or black)
        self.squares[row_other][4] = Square(row_other, 4, King(color))
        self.squares[row_other][4].piece.position = (row_other, 4)

    def restart_game(self):
        pass

    def move(self, last_row, last_col, row, col, piece, color):  
        captured_piece = self.squares[row][col].piece # Undo/Redo functionality
        self.move_history.append({
            'from': (last_row, last_col),
            'to': (row, col),
            'piece': piece,
            'captured': captured_piece,
            'moved': piece.moved,
            'player': color
        })
        self.redo_stack.clear()
        
        self.squares[last_row][last_col].piece = None
        self.squares[row][col].piece = piece
        self.squares[row][col].piece.position = (row, col)
        self.squares[row][col].piece.piece_up = False  
        if isinstance(piece, Pawn):                                           
            self.check_pawn_promotion(row, col, piece)
        elif isinstance(piece, King) and not piece.moved:
            self.castling(row, col, piece)        
        self.squares[row][col].piece.moves = []                                                    # Clear moves after moving the piece
        self.squares[row][col].piece.moved = True

    def undo_move(self):
        if not self.move_history:
            return False

        last_move = self.move_history.pop()
        from_row, from_col = last_move['from']
        to_row, to_col = last_move['to']
        piece = last_move['piece']
        captured = last_move['captured']

        self.squares[to_row][to_col].piece = captured
        self.squares[from_row][from_col].piece = piece
        piece.position = (from_row, from_col)
        piece.moved = last_move['moved']
        self.redo_stack.append(last_move)

        return last_move['player']

    def redo_move(self):
        if not self.redo_stack:
            return False

        move = self.redo_stack.pop()
        from_row, from_col = move['from']
        to_row, to_col = move['to']
        piece = move['piece']

        self.squares[from_row][from_col].piece = None
        self.squares[to_row][to_col].piece = piece
        piece.position = (to_row, to_col)
        piece.moved = True
        self.move_history.append(move)

        return 'black' if move['player'] == 'white' else 'white'

    def check_pawn_promotion(self, row, col, piece):
        if isinstance(piece, Pawn):
            if (piece.color == 'white' and row == 0) or (piece.color == 'black' and row == 7):
                self.squares[row][col].piece = Queen(piece.color)

    def castling(self, row, col, piece):
        row_other = 7 if piece.color == 'white' else 0
        if col == 2:
            rook_col = 0
            new_rook_col = 3
        elif col == 6:
            rook_col = 7
            new_rook_col = 5
        else:
            return
        self.squares[row_other][rook_col].piece = None
        self.squares[row_other][new_rook_col].piece = Rook(piece.color)
        self.squares[row_other][new_rook_col].piece.moved = True

    def valid_move(self, curr_row, curr_col, possible_row, possible_col, piece, bool):
        if bool:
            if not self.in_check(curr_row, curr_col, possible_row, possible_col, piece):
                piece.moves.append((possible_row, possible_col))
        else:
            piece.moves.append((possible_row, possible_col))

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

    def is_stalemate(self):
        pass

    def calc_moves(self, row, col, piece, bool=True):
        
        # Calculate all possible moves depending on selected piece

        def pawn_moves():                                                                          # Calculating moves for the pawn                            
            directions = [(piece.dir, 0), (2 * piece.dir, 0), (piece.dir, 1), (piece.dir, -1)]
            for dy, dx in directions:
                y, x = row + dy, col + dx
                if 0 <= x < COLS and 0 <= y < ROWS:
                    target = self.squares[y][x].piece

                    if dx != 0 and target is not None:                                             # Capturing diagonally
                        if target.color != piece.color:
                            self.valid_move(row, col, y, x, piece, bool)

                    elif dy == 2 * piece.dir and piece.moved == False:                             # Moving pawn two squares forward
                        if target is None and self.squares[y - piece.dir][x].piece is None:
                            self.valid_move(row, col, y, x, piece, bool)

                    elif dx == 0 and dy == piece.dir and target is None:                           # Moving pawn one square forward 
                        self.valid_move(row, col, y, x, piece, bool)

        def knight_moves():                                                                        # Calculating moves for the knight
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
                    if target is None or target.color != piece.color:  
                        self.valid_move(row, col, row_k, col_k, piece, bool)

        def moves_appending(directions):                                                           # Calculating moves for bishop, rook and queen
            for dy, dx in directions:
                y, x = row + dy, col + dx
                while 0 <= y < ROWS and 0 <= x < COLS:
                    target = self.squares[y][x].piece
                    if target is None:
                        self.valid_move(row, col, y, x, piece, bool)
                    else:
                        if target.color != piece.color:  
                            self.valid_move(row, col, y, x, piece, bool)
                        break  
                    x += dx
                    y += dy     

        def king_moves():                                                                          # Calculating moves for the king
            possible_moves = [(row, col - 1),                                                                                             
                            (row, col + 1),
                            (row - 1, col),
                            (row + 1, col),
                            (row - 1, col - 1),
                            (row - 1, col + 1),
                            (row + 1, col - 1),
                            (row + 1, col + 1)]
            for moves in possible_moves:
                row_k, col_k = moves
                if row_k >= 0 and row_k < ROWS and col_k >= 0 and col_k < COLS:
                    target = self.squares[row_k][col_k].piece
                    if target is None:
                        self.valid_move(row, col, row_k, col_k, piece, bool)
                    else:
                        if target.color != piece.color:
                            self.valid_move(row, col, row_k, col_k, piece, bool)

            # Castling logic
            row_other = 7 if piece.color == 'white' else 0
            if isinstance(self.squares[row_other][4].piece, King) and not self.squares[row_other][4].piece.moved and not self.in_check(row, col, row_other, 4, piece):
                if isinstance(self.squares[row_other][0].piece, Rook) and not self.squares[row_other][0].piece.moved:
                    if all(self.squares[row_other][i].piece is None for i in range(1, 4)):
                        if not self.in_check(row, col, row_other, 2, piece) and not self.in_check(row, col, row_other, 3, piece):
                            piece.moves.append((row_other, 2))
                    elif all(self.squares[row_other][i].piece is None for i in range(5, 7)):
                        if not self.in_check(row, col, row_other, 6, piece) and not self.in_check(row, col, row_other, 5, piece):
                            piece.moves.append((row_other, 6))

        piece.moves = []  # Clear previous moves

        if isinstance(piece, Pawn):
            pawn_moves()
                
        if isinstance(piece, Knight):
            knight_moves()
                
        if isinstance(piece, Bishop):
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]                                                
            moves_appending(directions) 
                
        if isinstance(piece, Rook):
            directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]                                        
            moves_appending(directions) 
                
        if isinstance(piece, Queen):
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1), (0, -1), (0, 1), (-1, 0), (1, 0)]    
            moves_appending(directions)
                
        if isinstance(piece, King):
            king_moves()

        
                
