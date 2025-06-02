import pygame
from const import *
from board import Board
from piece import Piece

class Game():

    def __init__(self):
        self.current_player = 'white'
        self.board = Board()
        self.selected_piece = None

    def drawing_chessboard(self, screen):      
        for row in range(ROWS):
            for col in range(COLS):
                if (row + col) % 2 == 0:
                    color = 'white'
                else:
                    color = 'darkgrey'
                pygame.draw.rect(screen, color, (col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def draw_pieces(self, screen):
        for row in range(ROWS):
            for col in range(COLS):
                if self.board.squares[row][col].piece:
                    piece = self.board.squares[row][col].piece
                    image_path = f'assets/images/{piece.color}_{piece.name}.png'
                    image = pygame.transform.scale(pygame.image.load(image_path), (100, 100))
                    screen.blit(image, (col*SQUARE_SIZE, row*SQUARE_SIZE))

    def show_moves(self, screen, piece):
        for moves in piece.moves: 
            row, col = moves
            rect = pygame.Rect(col*SQUARE_SIZE , row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(screen, 'blue', rect)