import pygame
from const import *
from board import Board

def drawing_chessboard(screen):
    for row in range(ROWS):
        for col in range(COLS):
            if (row + col) % 2 == 0:
                color = 'white'
            else:
                color = 'pink'
            pygame.draw.rect(screen, color, (col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_pieces(screen):

    board = Board()
    for row in range(ROWS):
        for col in range(COLS):
            if board.squares[row][col].piece:
                piece = board.squares[row][col].piece
                image_path = f'assets/images/{piece.color}_{piece.name}.png'
                image = pygame.transform.scale(pygame.image.load(image_path), (100, 100))
                screen.blit(image, (col*SQUARE_SIZE, row*SQUARE_SIZE))
