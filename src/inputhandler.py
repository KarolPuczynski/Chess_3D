from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from camera import Camera
from chesslogic import ChessLogic

class InputHandler:
    def __init__(self, camera, chess_logic):
        self.camera = camera
        self.chess_logic = chess_logic

    def mouse(self, button, state, x, y):
        self.camera.handle_mouse(button, state, x, y)
        
        if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
            viewport = glGetIntegerv(GL_VIEWPORT)
            modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
            projection = glGetDoublev(GL_PROJECTION_MATRIX)
            
            y = viewport[3] - y
            z = glReadPixels(x, y, 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT)
            
            if z[0][0] < 1.0:
                world_coords = gluUnProject(x, y, z[0][0], modelview, projection, viewport)
                self.chess_logic.handle_click(world_coords[0], world_coords[1])

    def motion(self, x, y):
        if self.camera.handle_motion(x, y):
            glutPostRedisplay()

    def keyboard(self, key, x, y):
        key = key.decode('utf-8')
        if key == 'q':
            exit(0)
        elif self.camera.handle_keyboard(key):
            glutPostRedisplay()