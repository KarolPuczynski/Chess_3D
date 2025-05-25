import pygame
from const import *
from game import *
from board import *

# Pygame window initaliation
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Chess fake 3D")

game = Game()
board = game.board

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
                
                if board.squares[clicked_row][clicked_col].has_piece() and board.squares[clicked_row][clicked_col].piece.color == game.next_player:
                        piece = board.squares[clicked_row][clicked_col].piece
                        board.calc_moves(clicked_row, clicked_col, piece) 
                        game.show_moves(screen, piece)
                        game.selected_piece = piece
                        last_clicked_row, last_clicked_col = clicked_row, clicked_col
                elif game.selected_piece != None and (clicked_row, clicked_col) in game.selected_piece.moves: # If the clicked square is empty and is in the list of possible moves
                    board.squares[last_clicked_row][last_clicked_col].piece = None 
                    board.move(clicked_row, clicked_col, game.selected_piece, game.next_player) 
                    game.selected_piece = None
                    game.next_player = 'black' if game.next_player == 'white' else 'white' 
                else:
                     game.selected_piece = None # If the clicked square is empty and is not in the list of possible moves
                    
                

        elif event.type == pygame.QUIT: # event checking
            pygame.quit()
            exit()
          
     

    pygame.display.update()  # Update the display