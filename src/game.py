import pygame
from const import *
from board import Board
from piece import Piece
from OpenGL.GL import *
from OpenGL.GLU import *

from objloader import *

class Game():

    def __init__(self):
        self.current_player = 'white'
        self.board = Board()
        self.selected_piece = None
        self.board_3D = OBJ('assets/models/chess_board_wood.obj', swapyz=True)
        self.pieces_3D = {}
        self.load_pieces_3d()
        self.board_start_x_3D = -16.8
        self.board_start_y_3D = -16.8
        self.square_size_3D = 4.8


    def world_to_board_coords(self, mouse_x, mouse_y):
        board_size = 8

        viewport = glGetIntegerv(GL_VIEWPORT)
        modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
        projection = glGetDoublev(GL_PROJECTION_MATRIX)
        real_y = viewport[3] - mouse_y  # odwróć Y, bo OpenGL i Pygame mają inne układy Y

        # Obliczamy promień w przestrzeni świata
        near_point = gluUnProject(mouse_x, real_y, 0.0, modelview, projection, viewport)
        far_point = gluUnProject(mouse_x, real_y, 1.0, modelview, projection, viewport)

        ray_dir = [far_point[i] - near_point[i] for i in range(3)]
        if ray_dir[2] == 0:
            return None, None  # linia równoległa do planszy (Z=0)

        # Znajdź przecięcie promienia z płaszczyzną Z=0
        t = -near_point[2] / ray_dir[2]
        if t < 0:
            return None, None  # przecięcie za kamerą

        intersect_x = near_point[0] + t * ray_dir[0]
        intersect_y = near_point[1] + t * ray_dir[1]

        # Zamiana współrzędnych na indeksy pola
        col_f = (intersect_x - self.board_start_x_3D) / self.square_size_3D
        row_f = (intersect_y - self.board_start_y_3D) / self.square_size_3D

        print(f"Debug: intersect_x={intersect_x}, intersect_y={intersect_y}, col_f={col_f}, row_f={row_f}")

        col = round(col_f)
        row = round(row_f)

        if 0 <= col < board_size and 0 <= row < board_size:
            return row, col
        else:
            return None, None

    def drawing_chessboard_3d(self, screen):
        glCallList(self.board_3D.gl_list)

    def draw_circle_3d(self, x, y, z, radius=10.5, segments=32):
        from math import sin, cos, pi

        glColor3f(1, 0, 0)  # niebieski
        glLineWidth(5)
        glBegin(GL_LINE_LOOP)
        for i in range(segments):
            angle = 2 * pi * i / segments
            dx = radius * cos(angle)
            dy = radius * sin(angle)
            glVertex3f(x + 1.3*dx, y + 1.3*dy, z)
        glEnd()

    def load_pieces_3d(self):
        pieces = ['pawn', 'knight', 'bishop', 'rook', 'queen', 'king']
        colors = ['white', 'black']
        for piece in pieces:
            for color in colors:
                object_path = f'assets/models/{piece}_{color}.obj'        
                obj = OBJ(object_path, swapyz=True)
                self.pieces_3D[(piece, color)] = obj

    def draw_pieces_3d(self):
        for row in range(8):
            for col in range(8):
                piece = self.board.squares[row][col].piece 
                if piece is not None:
                    model = self.pieces_3D.get((piece.name, piece.color))  # piece.name = 'pawn', 'knight', etc.
                    if model and piece.piece_up is False:
                        glPushMatrix()
                        glTranslatef(self.board_start_x_3D + col * self.square_size_3D, self.board_start_y_3D + row * self.square_size_3D, 0)
                        glScalef(0.8, 0.8, 0.8)     # dopasuj rozmiar modeli
                        glCallList(model.gl_list)
                        glPopMatrix()

    def show_moves_3d(self, piece, row, col):
        model = self.pieces_3D.get((piece.name, piece.color))
        piece.piece_up = True 
        if model:
            glPushMatrix()
            glTranslatef(self.board_start_x_3D + col * self.square_size_3D, self.board_start_y_3D + row * self.square_size_3D, 2)
            glScalef(0.8, 0.8, 0.8)     # dopasuj rozmiar modeli
            glCallList(model.gl_list)
            glPopMatrix()

        for move in piece.moves:
            row, col = move

            x = self.board_start_x_3D + col * self.square_size_3D
            y = self.board_start_y_3D + row * self.square_size_3D
            z = 0.1  # lekko ponad planszą, by nie mrugało z deską

            self.draw_circle_3d(x, y, z, radius=1.2)

    def drawing_chessboard(self, screen):      
        for row in range(ROWS):
            for col in range(COLS):
                if (row + col) % 2 == 0:
                    color = LIGHT_SQUARE_COLOR
                else:
                    color = DARK_SQUARE_COLOR
                pygame.draw.rect(screen, color, (col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                
    def draw_pieces(self, screen):
        for row in range(ROWS):
            for col in range(COLS):
                if self.board.squares[row][col].piece:
                    piece = self.board.squares[row][col].piece
                    image_path = f'assets/images/{piece.color}_{piece.name}.png'
                    object_path = f'asstets/models/{piece.name}_{piece.color}.obj'
                    
                    image = pygame.transform.scale(pygame.image.load(image_path), (100, 100))
                    screen.blit(image, (col*SQUARE_SIZE, row*SQUARE_SIZE))

    def show_moves(self, screen, piece):
        for moves in piece.moves: 
            row, col = moves
            if (row + col) % 2 == 0:
                color = LIGHT_SQUARE_HIGHLIGHT_COLOR
            else:
                color = DARK_SQUARE_HIGHLIGHT_COLOR
            rect = pygame.Rect(col*SQUARE_SIZE , row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(screen, color, rect)
