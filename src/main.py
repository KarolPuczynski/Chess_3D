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

            if event.button == 1:  # Left mouse button
                mouse_pos = pygame.mouse.get_pos()  
                clicked_col, clicked_row  = mouse_pos[0] // SQUARE_SIZE, mouse_pos[1] // SQUARE_SIZE # Finding coordinates of the clicked square based on the click
                
                if board.squares[clicked_row][clicked_col].has_piece() and board.squares[clicked_row][clicked_col].piece.color == game.current_player:  # Showing possible moves for the selected piece 
                        piece = board.squares[clicked_row][clicked_col].piece
                        board.calc_moves(clicked_row, clicked_col, piece) 
                        game.show_moves(screen, piece)
                        game.selected_piece = piece
                        print(f"Clicked square: ({clicked_row}, {clicked_col} and moves {game.selected_piece.moves}")  # showing clicked square and game selected piece moves
                        last_clicked_row, last_clicked_col = clicked_row, clicked_col

                elif game.selected_piece != None and (clicked_row, clicked_col) in game.selected_piece.moves:     # Making a move 
                    board.move(last_clicked_row, last_clicked_col ,clicked_row, clicked_col, game.selected_piece, game.current_player) 
                    if board.is_checkmate('black' if game.current_player == 'white' else 'white'):
                        print(f"Checkmate! {game.current_player} wins!")
                        break
                    
                    game.selected_piece = None
                    game.current_player = 'black' if game.current_player == 'white' else 'white'

                else:
                     game.selected_piece = None                                                                   # If the clicked square is empty and is not in the list of possible moves
                    
        elif event.type == pygame.QUIT: # event checking
            pygame.quit()
            exit()
          
    pygame.display.update()  # Update the display