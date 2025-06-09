import sys, pygame
from pygame.locals import *
from pygame.constants import *
from OpenGL.GL import *
from OpenGL.GLU import *
from const import *
from objloader import *
from game import *

pygame.init()
viewport = (WINDOW_WIDTH, WINDOW_HEIGHT)
hx = viewport[0] / 2
hy = viewport[1] / 2
pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, 1)
pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLESAMPLES, 8)
srf = pygame.display.set_mode(viewport, OPENGL | DOUBLEBUF | pygame.GL_MULTISAMPLEBUFFERS)
glEnable(GL_MULTISAMPLE)

glClearColor(*BACKGROUND_COLOR_3D)

glLightfv(GL_LIGHT0, GL_POSITION, (-40, 200, 100, 0.0))
glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.4, 0.4, 0.4, 1.0))
glLightfv(GL_LIGHT0, GL_SPECULAR, (0.1, 0.1, 0.1, 1.0))
glMaterialfv(GL_FRONT, GL_SHININESS, 8)

glLightModelfv(GL_LIGHT_MODEL_AMBIENT, (0.1, 0.1, 0.1, 1.0))

glEnable(GL_LIGHT0)
glEnable(GL_LIGHTING)
glEnable(GL_COLOR_MATERIAL)
glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

glEnable(GL_LIGHT1)
glLightfv(GL_LIGHT1, GL_POSITION, (0, 50, 0, 1.0))
glLightfv(GL_LIGHT1, GL_AMBIENT, (0.15, 0.15, 0.15, 1.0))
glLightfv(GL_LIGHT1, GL_DIFFUSE, (0.1, 0.1, 0.1, 1.0))
glLightfv(GL_LIGHT1, GL_SPECULAR, (0, 0, 0, 1.0))
glEnable(GL_LIGHT1)

glEnable(GL_DEPTH_TEST)
glShadeModel(GL_SMOOTH)
glEnable(GL_MULTISAMPLE)
glEnable(GL_NORMALIZE)
glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluPerspective(60.0, WINDOW_WIDTH / float(WINDOW_HEIGHT), 3.0, 100.0)
glMatrixMode(GL_MODELVIEW)

rx, ry = (0,0)                                              # rotation parameters
tx, ty = (0,0)
rz = 0
rotate_left = False
rotate_right = False
zpos = 25
rotate = move = False

clock = pygame.time.Clock()
game = Game()
board = game.board

view_mode = '3d'  

while True:
    clock.tick(70)
    
    if view_mode == '3d':
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        glTranslate(tx / 20., ty / 20., -zpos)
        glRotate(ry, 1, 0, 0)
        glRotate(rx, 0, 1, 0)
        glRotate(rz, 0, 0, 1)
        game.drawing_chessboard_3d(srf)
        game.draw_pieces_3d(game.selected_piece)
        if game.selected_piece:
            game.show_moves_3d(game.selected_piece, game.selected_piece.position[0], game.selected_piece.position[1])
        pygame.display.flip()

    else:
        srf.fill((0, 0, 0))
        game.drawing_chessboard(srf)
        if game.selected_piece:
            game.show_moves(srf, game.selected_piece)
        game.draw_pieces(srf)
        pygame.display.flip()

    for e in pygame.event.get():                        # INPUT HANDLER
        if e.type == QUIT:
            sys.exit()
        elif e.type == KEYDOWN:

            if e.key == K_ESCAPE:
                sys.exit()
            elif e.key == K_SPACE:                      # choosing game mode (3D or 2D)
                if view_mode == '3d':
                    view_mode = '2d'
                    srf = pygame.display.set_mode(viewport)
                else:
                    view_mode = '3d'
                    rx, ry = 0, 0
                    tx, ty = 0, 0
                    zpos = 5
                    srf = pygame.display.set_mode(viewport, OPENGL | DOUBLEBUF)

                    glClearColor(0.7, 1.0, 0.7, 1.0)
                    glEnable(GL_DEPTH_TEST)
                    glMatrixMode(GL_PROJECTION)
                    glLoadIdentity()
                    gluPerspective(90.0, viewport[0]/float(viewport[1]), 1, 100.0)
                    glMatrixMode(GL_MODELVIEW)

            elif e.key == K_a:
                rotate_left = True
            elif e.key == K_d:
                rotate_right = True
            elif e.key == K_n:
                board.redo_move()
            elif e.key == K_m:
                board.undo_move()
            elif e.key == K_r:
                board.restart_game()

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
                        if view_mode == "3d":
                            game.show_moves_3d(piece, clicked_row, clicked_col)
                        else:
                            game.show_moves(srf, piece)
                        game.selected_piece = piece
                        last_clicked_row, last_clicked_col = clicked_row, clicked_col

                    elif game.selected_piece is not None and (clicked_row, clicked_col) in game.selected_piece.moves:
                        board.move(last_clicked_row, last_clicked_col, clicked_row, clicked_col, game.selected_piece, game.current_player)
                        if board.is_checkmate('black' if game.current_player == 'white' else 'white'):
                            print(f"Checkmate! {game.current_player} wins!")
                            sys.exit()
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

    