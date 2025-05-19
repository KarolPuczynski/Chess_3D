import pygame
from const import *
from game import *
from board import *

# Pygame window initaliation
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Chess fake 3D")

game = Game()
board = Board()

# Game main loop
while True:
    
    game.drawing_chessboard(screen)
    if game.selected_piece:
        game.show_moves(screen, game.selected_piece)
    game.draw_pieces(screen)

    
    

    for event in pygame.event.get():

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button, showing all possible moves for selected piece 
                mouse_pos = pygame.mouse.get_pos()  
                clicked_col, clicked_row  = mouse_pos[0] // SQUARE_SIZE, mouse_pos[1] // SQUARE_SIZE # Finding coordinates of the clicked square based on the click 
                if board.squares[clicked_row][clicked_col].piece:
                        piece = board.squares[clicked_row][clicked_col].piece
                        if piece.color == game.next_player:
                             game.selected_piece = piece 
                             board.calc_moves(clicked_row, clicked_col, piece) 
                             game.show_moves(screen, piece)
                else:
                     game.selected_piece = None             

        elif event.type == pygame.QUIT: # event checking
            pygame.quit()
            exit()
          
     

    pygame.display.update()  # Update the display