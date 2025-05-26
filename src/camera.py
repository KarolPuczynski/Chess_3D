from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import * 

class Camera:
    def __init__(self):
        self.rotation_x = 0
        self.rotation_y = 0
        self.zoom_distance = 80.0
        self.right_mouse_down = False
        self.prev_x = 0
        self.prev_y = 0

    def setup_projection(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, float(width)/float(height), 0.1, 140.0)
        glMatrixMode(GL_MODELVIEW)

    def update_view(self):
        glLoadIdentity()
        gluLookAt(0, 0, self.zoom_distance, 0, 0, 0, 0, 1, 0)
        glRotatef(self.rotation_x, 1, 0, 0)
        glRotatef(self.rotation_y, 0, 1, 0)

    def handle_mouse(self, button, state, x, y):
        if button == GLUT_RIGHT_BUTTON:
            self.right_mouse_down = (state == GLUT_DOWN)
            self.prev_x, self.prev_y = x, y

    def handle_motion(self, x, y):
        if self.right_mouse_down:
            self.rotation_x += (y - self.prev_y) * 0.5
            self.rotation_y += (x - self.prev_x) * 0.5
            self.prev_x, self.prev_y = x, y
            return True
        return False

    def handle_keyboard(self, key):
        key = key.lower()
        if key == '+':
            self.zoom_distance = max(1.0, self.zoom_distance - 1)
            return True
        elif key == '-':
            self.zoom_distance = min(80.0, self.zoom_distance + 1)
            return True
        return False