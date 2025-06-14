import sys 
import pygame
import time
from pygame.locals import *
from pygame.constants import *
from OpenGL.GL import *
from OpenGL.GLU import *
from const import *
from objloader import *
from game import *
import scene3D
import sound

pygame.init()
view_mode = "3d"
pygame.display.set_caption("Chess 3D")
srf = pygame.display.set_mode(VIEWPORT_3D, OPENGL | DOUBLEBUF | pygame.GL_MULTISAMPLEBUFFERS)  

scene3D.scene_lightning()

rx, ry, rz = (0, -53, 0)                                              # rotation parameters
tx, ty = (0,0)
zpos = 40
rotate_left = False
rotate_right = False
rotate = move = False

clock = pygame.time.Clock()
game = Game(view_mode)
board = game.board

while True:
    clock.tick(60)
    
    if view_mode == '3d':
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        scene3D.rotate(tx, ty, rx, ry, rz, zpos)
        game.drawing_chessboard_3d()
        if game.selected_piece:
            game.show_moves_3d(game.selected_piece, game.selected_piece.position[0], game.selected_piece.position[1])
        game.draw_pieces_3d(game.selected_piece)

    else:
        srf.fill((0, 0, 0))
        game.drawing_chessboard(srf)
        if game.selected_piece:
            game.show_moves(srf, game.selected_piece)
        game.draw_pieces(srf)

    for e in pygame.event.get():                        # INPUT HANDLER
        if e.type == QUIT:
            sys.exit()
        elif e.type == KEYDOWN:

            if e.key == K_ESCAPE:
                sys.exit()
            elif e.key == K_SPACE:                      # choosing game mode (3D or 2D)
                if view_mode == '3d':
                    game.board_3D = None
                    game.pieces_3D = {} 
                    view_mode = '2d'
                    srf = pygame.display.set_mode(VIEWPORT_2D)
                    pygame.display.set_caption("Chess 2D")
                else:
                    view_mode = '3d'
                    rx, ry = 0, 0
                    tx, ty = 0, 0
                    zpos = 40
                    srf = pygame.display.set_mode(VIEWPORT_3D, OPENGL | DOUBLEBUF | pygame.GL_MULTISAMPLEBUFFERS)
                    pygame.display.set_caption("Chess 3D")
                    scene3D.scene_lightning()
                    game.init_3d()

            elif e.key == K_a:               
                rotate_left = True
            elif e.key == K_d:
                rotate_right = True
            elif e.key == K_RIGHT:                      
                next_player = board.redo_move()
                if next_player:
                    game.current_player = next_player
            elif e.key == K_LEFT:                       
                prev_player = board.undo_move()
                if prev_player:
                    game.current_player = prev_player
            elif e.key == K_r:                          # game restart
                game = Game(view_mode)
                board = game.board

        elif e.type == KEYUP:
            if e.key == K_a:
                rotate_left = False
            elif e.key == K_d:
                rotate_right = False

        elif e.type == MOUSEBUTTONDOWN:
            if e.button == 4: zpos = max(1, zpos-1)     # zooming in
            elif e.button == 5: zpos += 1               # zooming out

            elif e.button == 1:                         # choosing piece or making a move by left click
                
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if view_mode == "3d":
                    clicked_row, clicked_col = game.world_to_board_coords(mouse_x, mouse_y)
                else:
                    clicked_col, clicked_row  = mouse_x // SQUARE_SIZE, mouse_y // SQUARE_SIZE
                
                if clicked_row is not None and clicked_col is not None:

                    if board.squares[clicked_row][clicked_col].has_piece() and board.squares[clicked_row][clicked_col].piece.color == game.current_player:
                        piece = board.squares[clicked_row][clicked_col].piece
                        board.calc_moves(clicked_row, clicked_col, piece)
                        game.show_moves_3d(piece, clicked_row, clicked_col) if view_mode == "3d" else game.show_moves(srf, piece) 
                        game.selected_piece = piece
                        last_clicked_row, last_clicked_col = clicked_row, clicked_col

                    elif game.selected_piece is not None and (clicked_row, clicked_col) in game.selected_piece.moves:
                        
                        board.move(last_clicked_row, last_clicked_col, clicked_row, clicked_col, game.selected_piece, game.current_player, True)

                        if board.is_checkmate('black' if game.current_player == 'white' else 'white'):
                            print(f"Checkmate! {game.current_player} wins!")
                            board.sound_type = "game_end"
                            sound.play_sound(board.sound_type)
                        
                        if board.is_stalemate('black' if game.current_player == 'white' else 'white'):
                            print(f"Stalemate! {game.current_player} has no legal moves.")
                            board.sound_type = "stalemate"
                            sound.play_sound(board.sound_type)

                        if view_mode == "3d":
                            for i in range(45):
                                rz += 4
                                glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
                                glLoadIdentity()
                                scene3D.rotate(tx, ty, rx, ry, rz, zpos)
                                game.drawing_chessboard_3d()
                                game.draw_pieces_3d(None)
                                pygame.display.flip()
                                clock.tick(60)
                            
                        game.selected_piece = None
                        game.current_player = 'black' if game.current_player == 'white' else 'white'

                    else:
                        game.selected_piece = None

            elif e.button == 3:                         # right click to rotate the board
                rotate = True
        elif e.type == MOUSEBUTTONUP:                   # if right click is disactive camera will stop to rotate
            if e.button == 3:
                rotate = False
        elif e.type == MOUSEMOTION:                     # rotation cords
            i, j = e.rel
            if rotate:
                rx += i
                ry += j
            if move:
                tx += i
                ty -= j

    if rotate_left:                                     # rotating board around Z axis
        rz += 2
    if rotate_right:
        rz -= 2

    pygame.display.flip()

    
