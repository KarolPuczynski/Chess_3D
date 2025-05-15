import pygame
from const import *
from game import *
from board import *

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Chess fake 3D")

game = Game()
board = Board()

while True:
    
    game.drawing_chessboard(screen)
    game.show_moves(screen)
    game.draw_pieces(screen)
    

    for event in pygame.event.get():

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button 
                mouse_pos = pygame.mouse.get_pos()  
                clicked_col, clicked_row  = mouse_pos[0] // SQUARE_SIZE, mouse_pos[1] // SQUARE_SIZE 
                if board.squares[clicked_row][clicked_col].piece:
                        piece = board.squares[clicked_row][clicked_col].piece
                        if piece.color == game.next_player: 
                             board.calc_moves(clicked_row, clicked_col, piece) 
                             game.show_moves(screen, piece)
        elif event.type == pygame.QUIT:
            pygame.quit()
            exit()
          
     

    pygame.display.update()  # Update the display