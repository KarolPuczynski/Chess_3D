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
hx = viewport[0]/2
hy = viewport[1]/2
srf = pygame.display.set_mode(viewport, OPENGL | DOUBLEBUF)

glClearColor(0.7, 1.0, 0.7, 1.0)

glLightfv(GL_LIGHT0, GL_POSITION,  (-40, 200, 100, 0.0))
glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
glEnable(GL_LIGHT0)
glEnable(GL_LIGHTING)
glEnable(GL_COLOR_MATERIAL)
glEnable(GL_DEPTH_TEST)
glShadeModel(GL_SMOOTH)           # most obj files expect to be smooth-shaded


clock = pygame.time.Clock()

glMatrixMode(GL_PROJECTION)
glLoadIdentity()
width, height = viewport
gluPerspective(90.0, width/float(height), 1, 100.0)
glMatrixMode(GL_MODELVIEW)

rx, ry = (0,0)
tx, ty = (0,0)
rz = 0
rotate_left = False
rotate_right = False
zpos = 25
rotate = move = False

game = Game()
board = game.board

view_mode = '3d'  # startujemy od 3D, możesz zmienić na '2d'

while True:
    clock.tick(100)
    
    if view_mode == '3d':
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        glTranslate(tx / 20., ty / 20., -zpos)
        glRotate(ry, 1, 0, 0)
        glRotate(rx, 0, 1, 0)
        glRotate(rz, 0, 0, 1)
        game.drawing_chessboard_3d(srf)
        if game.selected_piece:
            game.show_moves_3d(game.selected_piece, game.selected_piece.position[0], game.selected_piece.position[1])
        game.draw_pieces_3d()
        pygame.display.flip()

    else:
        # 2D - rysujemy normalnie Pygame 2D (bez OpenGL)
        srf.fill((0, 0, 0))  # czyścimy ekran na czarno lub inny kolor
        game.drawing_chessboard(srf)
        game.draw_pieces(srf)
        pygame.display.flip()

    for e in pygame.event.get():
        if e.type == QUIT:
            sys.exit()
        elif e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                sys.exit()
            elif e.key == K_SPACE:
                # Przełączanie widoku
                if view_mode == '3d':
                    view_mode = '2d'
                    srf = pygame.display.set_mode(viewport)  # bez OPENGL
                    print("Przełączono na widok: 2d")
                else:
                    view_mode = '3d'
                    rx, ry = 0, 0
                    tx, ty = 0, 0
                    zpos = 5
                    srf = pygame.display.set_mode(viewport, OPENGL | DOUBLEBUF)
                    # Ustawienia OpenGL po przełączeniu
                    glClearColor(0.7, 1.0, 0.7, 1.0)
                    glEnable(GL_DEPTH_TEST)
                    glMatrixMode(GL_PROJECTION)
                    glLoadIdentity()
                    gluPerspective(90.0, viewport[0]/float(viewport[1]), 1, 100.0)
                    glMatrixMode(GL_MODELVIEW)
                    print("Przełączono na widok: 3d")

            elif e.key == K_a:
                rotate_left = True
            elif e.key == K_d:
                rotate_right = True

        elif e.type == KEYUP:
            if e.key == K_a:
                rotate_left = False
            elif e.key == K_d:
                rotate_right = False        

        elif e.type == MOUSEBUTTONDOWN:
            if e.button == 4: zpos = max(1, zpos-1)
            elif e.button == 5: zpos += 1
            elif e.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                clicked_row, clicked_col = game.world_to_board_coords(mouse_x, mouse_y)
                if clicked_row is not None and clicked_col is not None:
                    if board.squares[clicked_row][clicked_col].has_piece() and board.squares[clicked_row][clicked_col].piece.color == game.current_player:
                        piece = board.squares[clicked_row][clicked_col].piece
                        board.calc_moves(clicked_row, clicked_col, piece)
                        game.show_moves_3d(piece, clicked_row, clicked_col)
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

            elif e.button == 3:
                rotate = True
        elif e.type == MOUSEBUTTONUP:
            if e.button == 3:
                rotate = False
        elif e.type == MOUSEMOTION:
            i, j = e.rel
            if rotate:
                rx += i
                ry += j
            if move:
                tx += i
                ty -= j

    if rotate_left:
        rz += 1
    if rotate_right:
        rz -= 1

    